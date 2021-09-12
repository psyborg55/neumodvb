/*
 * Neumo dvb (C) 2019-2021 deeptho@gmail.com
 * Copyright notice:
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 *
 */

#include "si_state.h"
#include "mpeg.h"
#include "neumodb/chdb/chdb_extra.h"
#include "neumodb/epgdb/epgdb_extra.h"
#include "substream.h"
#include <cstdlib>
#include <vector>

#ifndef UNUSED
#define UNUSED __attribute__((unused))
#endif

using namespace dtdemux;

static int default_timeout(uint8_t table_id) {
	// return 100000000;
	switch (table_id) {
	case 0x0:						/*PAT*/
		return 40000;			// 200 ms
	case 0x2:						/*PMT*/
		return 1000;			//???
	case 0x40:					/*NIT ACTUAL*/
	case 0x41:					/*NIT OTHER*/
		return 40000;			// 10000 ms
	case 0x42:					/*SDT ACTUAL*/
		return 20000;			// 2000 ms (10 times higher)
	case 0x46:					/*SDT OTHER*/
		return 40000;			// 10000 ms
	case 0x4a:					/*SDT BAT*/
		return 40000;			// 10000 ms
	case 0x4e:					/*EIT p/f Actual*/
		return 4000;			// 2000 ms
	case 0x4f:					/*EIT p/f Other*/
		return 20000;			// 10000 ms
	case 0x50 ... 0x5f: /*EIT schedule Actual*/
		return 30000;			// 10000 ms (but may be longer)
	case 0x60 ... 0x6f: /*EIT schedule Other*/
		return 300000;		// 30000 ms (but may be longer)
		// mhw2 table ids
	case 0x95: // 149
	case 0x96:
	case 0x97:
	case 0xc8:
	case 0xd2:
	case 0xdc:
	case 0xdd:
	case 0xe6:
	case 0xf0:
	case 0xf2:
	case 0xf3:
	case 0xfa:
		return 300000; // 30000 ms (but may be longer)
		// end mh2 tale ids
	case 0xd1:					/*Freesat EIT*/
	case 0xd5:					/*Freesat EIT*/
		return 300000;		// 30000 ms (but may be longer)
	case 0xa0 ... 0xab: /*SKYUK EPG*/
		return 300000;		// 30000 ms (but may be longer)
	}
	dtdebugx("UNHANDLED timeout 0x%x\n", table_id);
	return 20000;
}

table_timeout_t::table_timeout_t(int table_id)
	: start_time(steady_clock_t::now())
	, timeoutms(default_timeout(table_id))
	, table_id(table_id)
{}

inline bool table_timeout_t::timedout_now() {
	if (!timedout_) {
		auto now = steady_clock_t::now();
		auto delta = now - start_time;
		timedout_ = (delta > timeoutms);
		return timedout_;
	}
	return false; // return timedout only once
}

inline bool table_timeout_t::timedout(steady_time_t last_reset_time) {
	if (timedout_)
		return true;
	if (last_reset_time > start_time) {
		start_time = last_reset_time;
		return false;
	}
	auto now = steady_clock_t::now();
	if ((now - start_time) > timeoutms) {
		timedout_ = true;
		return true;
	}
	return false;
}

inline completion_status_t::completion_status_t(const section_header_t& hdr)
	: version_number(hdr.version_number)
	, last_section_number(hdr.last_section_number)
{
	maxcount = last_section_number +1;
}

inline void completion_status_t::reset(const section_header_t& hdr)
{
	*this = completion_status_t(hdr);
}

inline bool completion_status_t::set_flag(int idx) {
	auto idx2 = idx % 32;
	auto idx1 = (idx - idx2) / 32;
	assert(idx1 < sizeof(section_flags) / sizeof(section_flags[0]));
	auto& v = section_flags[idx1];
	auto mask = 1 << idx2;
	bool exists = v & mask;
	v |= mask;
	return exists;
}

/*
	principle::
	maxcount=exact number of expected sections + those after segment_last_section_number
	we allocate 256 bitflags (more than needed, but ss:vector has enough space anyway
	count only counts really existing sections
	for subtables containing a multiple table_ids (EIT schedule tables),
	unitialised completion_status_t records are inserted when the first record is
	received for any of the tables
*/

inline section_type_t completion_status_t::set_flag(const section_header_t& hdr) {
	if (hdr.section_number > hdr.last_section_number) {
		if (hdr.section_syntax_indicator) {
			dterrorx("section_number=%d > last=%d", hdr.section_number, hdr.last_section_number);
			return section_type_t::NEW;
		}
	}
	assert(!completed);
	bool exists = set_flag(hdr.section_number);
	if (!exists) {
		count++;
		if (hdr.section_syntax_indicator && hdr.section_number == hdr.segment_last_section_number &&
				hdr.segment_last_section_number < hdr.last_section_number) {
			/*33E 12645H contains a specifci subtable (service) with two sections where one states
				segment_last_section_number==0 and the other one  segment_last_section_number==1. This is wrong and can lead to
				"double counting" The following for loop is lower, but more robst to double counting than count +=
				(hdr.section_number + (7 - hdr.section_number%8) Its main downside is for debugging: section_flags now also
				contains obe bits for some non-received sections
			*/
			for (int i = hdr.section_number + 1;
					 i <= hdr.section_number + (7 - hdr.section_number % 8) && i < hdr.last_section_number; ++i) {
				bool exists = set_flag(i);
				count += !exists;
			}
		}
	}
	assert(count <= maxcount);
	completed = (count == maxcount);
#if 0
	dtdebugx("table[0x%x-%d] sec=%d count=%d/%d last=%d/%d exists=%d completed=%d",
					 hdr.table_id, hdr.table_id_extension, hdr.section_number, count, maxcount,
					 hdr.segment_last_section_number, hdr.last_section_number,
					 exists, completed);
#endif
	if (exists)
		return completed ? section_type_t::COMPLETE : section_type_t::DUPLICATE;
	return completed ? section_type_t::LAST : section_type_t::NEW;
}

void parser_status_t::reset() {
	*this = parser_status_t();
}

inline completion_status_t& parser_status_t::completion_status_for_section(const section_header_t& hdr) {
	subtable_key_t k(hdr);
	auto [it, inserted] = cstates.try_emplace(k, hdr);
	if (hdr.table_id >= 0x50 && hdr.table_id <= 0x6F) {
		if (!inserted && it->second.version_number < 0) {
			it->second.reset(hdr);
		}
		if (inserted) {
			int first_table_id = hdr.table_id & ~0xf;
			assert(first_table_id == (hdr.last_table_id & ~0xf));
			for (int table_id = first_table_id; table_id <= hdr.last_table_id; ++table_id) {
				if (table_id != hdr.table_id) {
					subtable_key_t k(hdr, table_id);
					auto [it, inserted] = cstates.try_emplace(k);
				}
			}
		}
	}
	return it->second;
}

/*
	check if a section was already processed.
	Also check if the table has timedout, which is the case if no cc_errors have appeared for
	a certain amount of time
	returns: timedout, new_subtable_version, section_type
*/
std::tuple<bool, bool, section_type_t> parser_status_t::check(const section_header_t& hdr, int cc_error_count) {
	bool timedout_now = false;
	bool newversion = false;
	last_section = steady_clock_t::now();
	if (cc_error_count > last_cc_error_count) {
		last_cc_error_count = cc_error_count;
		last_cc_error_time = steady_clock_t::now();
	}

	auto [it, inserted] = table_timeouts.try_emplace(hdr.table_id, hdr.table_id);
	auto& t = it->second;

	auto& cstate = completion_status_for_section(hdr);
	assert(count_completed <= (int)cstates.size());
	if (cstate.version_number != hdr.version_number) {
		newversion = true;
		timedout_now = false;
#if 0
		dtdebugx("table[0x%x-%d] subtable version changed from %d to %d",
						 hdr.table_id,  hdr.table_id_extension,cstate.version_number, hdr.version_number);
#endif
		if (cstate.completed) {
			assert(count_completed > 0);
			count_completed -= 1;
		}
		cstate.reset(hdr);
		completed = false;
		assert(!cstate.completed);
		t.reset();
	}
	if (cstate.completed) {
		timedout_now = t.timedout_now();
		return {timedout_now, newversion, section_type_t::DUPLICATE};
	}

	auto cstate_status = cstate.set_flag(hdr);
	assert(cstate_status != section_type_t::COMPLETE);

	if (cstate_status == section_type_t::NEW) {
		last_section = steady_clock_t::now();
		last_new_section = last_section;
		return {false, newversion, cstate_status};
	}

	if (cstate_status == section_type_t::DUPLICATE) {
		last_section = steady_clock_t::now();
		//assert(!completed); It is possible that new incomplete subtables have been discovered
		return {false, newversion, cstate_status};
	}

	assert(cstate_status == section_type_t::LAST);
	assert(cstate.completed);
	assert(count_completed < cstates.size());
	count_completed++;
	completed = (count_completed == (int)cstates.size());
	last_section = steady_clock_t::now();
	last_new_section = steady_clock_t::now();
	if (completed)
		return {false, newversion, section_type_t::LAST};
	else
		return {false, newversion, section_type_t::NEW};
}

void parser_status_t::reset(const section_header_t& hdr) {
	// ensure that timeouts  are reset
	last_cc_error_time = steady_clock_t::now();

	auto it = table_timeouts.find(hdr.table_id);
	if (it != table_timeouts.end()) {
		auto& t = it->second;
		t.reset();
	}

	auto& cstate = completion_status_for_section(hdr);
	assert(count_completed <= (int)cstates.size());
	if (cstate.completed) {
		assert(count_completed > 0);
		count_completed -= 1;
	}
	cstate.reset(hdr);
	completed = false;
	assert(!cstate.completed);
}

bool parser_status_t::timedout_now(uint8_t table_id) {
	auto it = table_timeouts.find(table_id);
	if (it != table_timeouts.end()) {
		auto& t = it->second;
		return t.timedout_now();
	}
	return true;
}

#if 0
void parser_status_t::stats() {
	int num = 0;
	for (auto& [k, c] : cstates) {
		if (k.table_id == 0x42 || k.table_id == 0x46) {
			printf("[0x%x] ts_id=%d\n", k.table_id, k.table_id_extension);
			num++;
		}
	}
	printf("TOTAL: %d\n", num);
}
#endif
