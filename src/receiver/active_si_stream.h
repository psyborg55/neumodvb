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

#pragma once
#include "stackstring.h"
#include "active_stream.h"
#include "receiver.h"
#include "scan.h"

#include <functional>
#include <map>


using namespace dtdemux;



struct pat_service_t {
	int service_id{-1};
	uint16_t pmt_pid{0x1fff};
	bool pmt_analysis_started{false};
	bool pmt_analysis_finished{false};
	pat_service_t(int service_id, int pmt_pid):
		service_id(service_id), pmt_pid(pmt_pid) {
	}
	std::shared_ptr<pmt_parser_t> parser;

};


struct pmt_data_t {
	std::map<uint16_t, pat_service_t> by_service_id; //services in pat indexed by service_id
	void pmt_section_cb(const pmt_info_t& pmt, bool isnext);

};

struct pat_data_t {

	struct pat_table_t : public pat_services_t {
		int num_sections_processed{0};
		ss::vector<pat_entry_t> last_entries; //from the previous complete PAT
		subtable_info_t subtable_info;
		void reset() {
			*this = pat_table_t();
		}

	};



	std::map<uint16_t, pat_table_t> by_ts_id; //indexed by ts_id

	inline bool has_ts_id(uint16_t ts_id) const {
		assert(by_ts_id.size()>0); //require pat to be received
		return by_ts_id.find(ts_id) != by_ts_id.end();
	}


	bool stable_pat_{false};
	constexpr static  std::chrono::duration pat_change_timeout = 5000ms; //in ms
	steady_time_t last_pat_change_time{};

	void reset() {
		*this = pat_data_t();
	}


	/*
		pat has been the same for stable_pat_timeout seconds

		If no pat is present, this is also considered a stable situation
		Note that "tuner not locked" will be handled higher up

	*/
	bool stable_pat(uint16_t ts_id);
	// check all pat tables
	bool stable_pat();


};


struct mux_presence_t {
	bool in_nit{false};
	bool in_sdt{false};
	bool sdt_completed{false};
};

struct network_data_t {
	uint16_t network_id{0xffff};
	bool is_actual{false};
	int num_muxes{0};
	subtable_info_t subtable_info{};
	int num_sections_processed{0};
	network_data_t(uint16_t network_id)
		: network_id(network_id)
		{}

	inline void reset() {
		*this = network_data_t(network_id);
	}
};


struct onid_data_t {
	int sdt_num_muxes_completed{0}; //number marked completed by sdt
	int sdt_num_muxes_present{0}; //number retrieved by sdt
	int nit_num_muxes_present{0}; //number found in NIT table
	uint16_t original_network_id;

	std::map<uint16_t, mux_presence_t> mux_presence;

	mux_presence_t& add_mux(int ts_id, bool from_sdt) {
		auto[it, inserted] = mux_presence.emplace(ts_id, mux_presence_t{});
		auto& p = it->second;
		if(from_sdt) {
			sdt_num_muxes_present += !p.in_sdt;
			p.in_sdt = true;
		} else {
			nit_num_muxes_present += !p.in_nit;
			p.in_nit = true;
		}
		return p;
	}

	inline bool set_sdt_completed(int ts_id) {
		auto &p = mux_presence[ts_id];
		assert(p.in_sdt);
		bool ret = p.sdt_completed;
		p.sdt_completed = true;
		sdt_num_muxes_completed += !ret;
		if(ret) {
			dtdebugx("sdt: ts_id=%d completed multiple times", ts_id);
		}
		return ret;
	}


#ifndef NDEBUG
	inline bool completed_() const {
		for(const auto& [ts_id, p]: mux_presence) {
			if(!p.in_sdt || !p.in_nit || !p.sdt_completed)
				return false;
		}
		return true;
	}
#endif

	inline bool completed() const {
		auto ret = sdt_num_muxes_present == (int)mux_presence.size() &&
			sdt_num_muxes_completed == (int)mux_presence.size() &&
			nit_num_muxes_present == (int)mux_presence.size();
#ifndef NDEBUG
		auto tst = completed_();
		assert(tst==ret);
#endif
		return ret;
	}


//	subtable_info_t subtable_info;
//	int num_sections_processed{0};
	onid_data_t(uint16_t original_network_id)
		: original_network_id(original_network_id)
		{}
};

struct mux_sdt_data_t {
	subtable_info_t subtable_info;
	int num_sections_processed{0};
};

struct mux_data_t  {

	enum source_t {
		NIT,
		SDT,
		NONE, //can only happen for current mux; any other lookup is initiated from sdt or nit
	};

	//data maintained by nit section code
	source_t source {NONE}; //set to true if from database
	chdb::mux_key_t mux_key{}; //we also need extra_id
	ss::string<32> mux_desc;
	bool is_tuned_mux{false};
	bool is_tuned_freq{false};
	//data maintained by sdt section code
	bool has_freesat_home_epg{false};
	bool has_opentv_epg{false};

	mux_sdt_data_t sdt[2]{{}}; //indexed by nit_actual
	subtable_info_t sdt_actual_subtable_info;
	//int sdt_actual_num_sections_processed{0};

	ss::vector<uint16_t, 32> service_ids; //service ids seen


	mux_data_t(const chdb::mux_key_t& mux_key, const ss::string_&  mux_desc)
		: mux_key(mux_key)
		, mux_desc(mux_desc)
		{}
};

struct sdt_data_t {
	int actual_network_id{-1};
	int actual_ts_id{-1};
	void reset() {
		*this = sdt_data_t();
	}
};

struct active_si_data_t;

struct nit_data_t {

	std::map <std::pair<uint16_t,uint16_t>, mux_data_t> by_network_id_ts_id;
	ss::vector<int16_t, 4> nit_actual_sat_positions; //sat_positions encountered in any mux listed in nit_actual
	//mux_data_t * tuned_mux_data{nullptr};

	/*
		for each network: record how many muxes sdt should process, and how many
		it has processed.
	 */
	std::map<uint16_t, onid_data_t> by_onid; //indexed by original_network_id
	std::map<uint16_t, network_data_t> by_network_id; //indexed by network_id

	inline onid_data_t& get_original_network(uint16_t network_id) {
		auto [it, inserted] = by_onid.try_emplace(network_id, onid_data_t{network_id});
		return it->second;
	}

	inline network_data_t& get_network(uint16_t network_id) {
		auto [it, inserted] = by_network_id.try_emplace(network_id, network_data_t{network_id});
		return it->second;
	}


	//mux_data_t* tuned_nit_data(const chdb::any_mux_t& tuned_mux);
	//int count_completed();
	void reset() {
		*this = nit_data_t();
	}
	bool update_sdt_completion(scan_state_t& scan_state, const subtable_info_t&info,
														 mux_data_t& mux_data, bool reset=false);

	void reset_sdt_completion(scan_state_t& scan_state, const subtable_info_t&info, mux_data_t& mux_data) {
		auto& sdt = mux_data.sdt[info.is_actual];
		if(sdt.subtable_info.version_number >= 0) //otherwise we have an init
			update_sdt_completion(scan_state, info, mux_data, true);
	}

	bool update_nit_completion(scan_state_t& scan_state, const subtable_info_t&info,
														 network_data_t& network_data, bool reset=false);

};



struct eit_data_t {
	int eit_actual_updated_records{0};
	int eit_actual_existing_records{0};
	int eit_other_updated_records{0};
	int eit_other_existing_records{0};

	struct subtable_count_t {
		int num_known{0};
		int num_completed{0};
	};

	std::map<uint16_t, subtable_count_t> subtable_counts; //indexed by pid

	std::map<std::tuple<uint16_t, uint16_t>,
					 std::tuple<time_t, time_t>> otv_times_for_event_id; //start and end time indexed by channel_id, event_id

	std::map<std::tuple<uint32_t>,
					 std::tuple<epgdb::epg_service_t, time_t, time_t>> mhw2_key_for_event_id; //key and start/end time indexed by summary_id


	void reset() {
		*this = eit_data_t();
	}

};


struct bat_data_t {
	struct bouquet_data_t  {
		int db_num_channels{0}; //nunmber of services stored in db
		ss::vector<uint16_t, 256> channel_ids; //service ids seen on sreen

		//data used by bat
		subtable_info_t subtable_info;
		int num_sections_processed{0};

		bouquet_data_t(int db_num_channels)
			: db_num_channels(db_num_channels)
			{}
	};

	///////////data

	std::map <uint16_t, bouquet_data_t> by_bouquet_id;
	std::map<uint16_t, chdb::service_key_t> opentv_service_keys; //indexed by channel_id


	bouquet_data_t& get_bouquet(const chdb::chg_t& chg) {
		auto [it, found] = by_bouquet_id.try_emplace(chg.k.bouquet_id,
																								 bouquet_data_t{chg.num_channels});
		return it->second;
	}

	inline void reset_bouquet(int bouquet_id) {
		by_bouquet_id.erase(bouquet_id);
	}


	chdb::service_key_t* lookup_opentv_channel(uint16_t channel_id) {
		auto[it, found] = find_in_map(opentv_service_keys, channel_id);
		return found ? &it->second : nullptr;
	}


	void reset() {
		*this = bat_data_t();
	}
};



struct active_si_data_t {

////////data
	//int read_pointer{0};
	tune_confirmation_t tune_confirmation;

	pat_data_t pat_data;
	pmt_data_t pmt_data;
	nit_data_t nit_data;
	sdt_data_t sdt_data;
	bat_data_t bat_data;
	eit_data_t eit_data;
	//secondary cache for eit and bat
	std::map <std::pair<uint16_t,uint16_t>, chdb::mux_key_t> mux_key_by_network_id_ts_id;

	bool is_embedded_si{false};
	system_time_t tune_start_time{};

	scan_state_t scan_state;
	bool scan_in_progress{false};
	active_si_data_t(bool is_embedded_si)
		: is_embedded_si(is_embedded_si)
		{}

	void reset() {
		*this = active_si_data_t(is_embedded_si);
	}


	/*
		done means: timedout or completed
		completed means: we have retrieved all available info
	*/
	bool pat_done() const {
		return scan_state.done(scan_state_t::completion_index_t::PAT);
	}

	bool nit_actual_done() const {
		return scan_state.done(scan_state_t::completion_index_t::NIT_ACTUAL);
	}

	bool nit_other_done() const {
		return scan_state.done(scan_state_t::completion_index_t::NIT_OTHER);
	}

	bool sdt_actual_done() const {
		return scan_state.done(scan_state_t::completion_index_t::SDT_ACTUAL);
	}

	bool sdt_other_done() const {
		return scan_state.done(scan_state_t::completion_index_t::SDT_OTHER);
	}

	bool bat_done() const {
		return scan_state.done(scan_state_t::completion_index_t::BAT);
	}

	bool pat_completed() const {
		return scan_state.completed(scan_state_t::completion_index_t::PAT);
	}

	bool nit_actual_completed() const {
		return scan_state.completed(scan_state_t::completion_index_t::NIT_ACTUAL);
	}

	bool nit_actual_notpresent() const {
		return scan_state.notpresent(scan_state_t::completion_index_t::NIT_ACTUAL);
	}

	bool nit_other_completed() const {
		return scan_state.completed(scan_state_t::completion_index_t::NIT_OTHER);
	}

	bool sdt_actual_completed() const {
		return scan_state.completed(scan_state_t::completion_index_t::SDT_ACTUAL);
	}

	bool sdt_other_completed() const {
		return scan_state.completed(scan_state_t::completion_index_t::SDT_OTHER);
	}

	bool bat_completed() const {
		return scan_state.completed(scan_state_t::completion_index_t::BAT);
	}

	/*
		sdt has foiund complete service data for the same number of muxes
		as were discovered in nit_actual
	 */
	bool network_sdt_completed(uint16_t network_id) const {
		if(!nit_actual_done()) //Note: done() instead of completed()
			return false; //more muxes may be discored in nit; we do not care about nit_other
		auto [it, found] = find_in_map(nit_data.by_onid, network_id);
		if(found) {
			return it->second.completed();
		}
		return false;
	}

	/*
		either we have all nit and sdt info for this network, or it is no longer possible
		that we will receive it because nit_actual has done (completed ot not)
		and sdt is still not done
	 */
	bool network_done(uint16_t original_network_id) const {
		auto [it, found] = find_in_map(nit_data.by_onid, original_network_id);
		if(found)
			return it->second.completed() || nit_actual_done();

		/*
			if nit_actual_done() and nit knows the network, then found should have been true
		 */
		return nit_actual_done();
	}

	bool bouquet_done(uint16_t bouquet_id) const {
		auto [it, found] = find_in_map(bat_data.by_bouquet_id, bouquet_id);
		if(found)
			return it->second.num_sections_processed == it->second.subtable_info.num_sections_present;
		return bat_done();
	}


	bool nit_other_all_networks_completed() const {
		/*@todo: this includes also nit_actual, which is incorrect.

			instead we may have to mainat a per network_id (instead of per onid)
			datastructure and record how many sections we have loaded (and if more could follow)
		 */
		for(auto& [network_id, n]: nit_data.by_network_id) {
			if (!n.is_actual && n.num_sections_processed != n.subtable_info.num_sections_present)
				return false;
		}
		return true;
	}

	bool bat_all_bouquets_completed() const {
		for(auto& [bouquet_id, b]: bat_data.by_bouquet_id) {
			if(b.num_sections_processed != b.subtable_info.num_sections_present)
				return false;
		}
		return true;
	}

	/*
		Usually a mux is only has entries in either SDT_actual or sdt_other,
		but sometimes it is present in both; so we employ checking subtable_info.num_sections_present>0
		as a heuristic to choose between sdt_actual and sdt_other, with a preference for sdt_actual
		in case of doubt.

		This function is oly used in bat processing
	 */
	bool mux_sdt_done(uint16_t network_id, uint16_t ts_id) const {
		auto [it, found] = find_in_map(nit_data.by_network_id_ts_id, std::make_pair(network_id, ts_id));
		if(found) {
			int result_for_actual= -1;
			for(auto& sdt: it->second.sdt) {
				if (result_for_actual <0)
					result_for_actual = (sdt.num_sections_processed == sdt.subtable_info.num_sections_present);
				if(sdt.subtable_info.num_sections_present>0) {
					return sdt.num_sections_processed == sdt.subtable_info.num_sections_present;
				}
			}
			return result_for_actual;
		}
		return nit_actual_done();
	}

	bool all_known_muxes_completed() const {
		for(auto& [nit_tid, m]: nit_data.by_network_id_ts_id) {
			for(const auto& sdt: m.sdt) {
			if (sdt.num_sections_processed != sdt.subtable_info.num_sections_present)
				return false;
			}
		}
		return true;
	}


};



class active_si_stream_t final : /*public std::enable_shared_from_this<active_stream_t>,*/
	public active_stream_t, active_si_data_t
{
	friend class active_adapter_t;


	friend class tuner_thread_t;

	chdb::chdb_t& chdb;
	epgdb::epgdb_t& epgdb;

	std::optional<db_txn> epgdb_txn_;
	std::optional<db_txn> chdb_txn_;

	inline db_txn epgdb_txn() {
		if(!epgdb_txn_)
			epgdb_txn_.emplace(epgdb.wtxn());
		return epgdb_txn_->child_txn();
	}

	inline db_txn chdb_txn() {
		if(!chdb_txn_)
			chdb_txn_.emplace(chdb.wtxn());
		return chdb_txn_->child_txn();
	}

	dtdemux::ts_stream_t stream_parser;
	scan_target_t scan_target; //which SI tables should be scanned?
	bool scan_done{false};

	/*we need one parser per pid; within each pid multiple tables may exist
		but those are transmitted sequentially. Between pids, they are not
		"""Within TS packets of any single PID value, one section is finished before the next one is allowed to be started,
		"""
	*/
	std::vector<std::shared_ptr<dtdemux::psi_parser_t>>  parsers;

	void update_tuned_mux(db_txn& wxtn, chdb::any_mux_t& mux, bool may_change_sat_pos,
												bool may_change_nit_tid, bool from_sdt);

	dtdemux::reset_type_t pat_section_cb(const pat_services_t& pat_services, const subtable_info_t& i);
	void pmt_section_cb(const pmt_info_t& pmt, bool isnext);

	dtdemux::reset_type_t nit_section_cb_(nit_network_t& network, const subtable_info_t& i);
	dtdemux::reset_type_t nit_section_cb(nit_network_t& network, const subtable_info_t& i);

	void add_pmt(uint16_t service_id, uint16_t pmt_pid);
	bool sdt_actual_check_confirmation(bool mux_key_changed, int db_corrrect,mux_data_t* p_mux_data);

	dtdemux::reset_type_t
		nit_actual_update_tune_confirmation(db_txn& txn, chdb::any_mux_t& mux, bool is_tuned_mux);

	dtdemux::reset_type_t on_nit_completion(db_txn& wtxn, network_data_t& network_data,
																					dtdemux::reset_type_t ret, bool is_actual,
																					bool on_wrong_sat, bool done);

	std::tuple<bool, bool>
	sdt_process_service(db_txn& wtxn, const chdb::service_t& service, mux_data_t* p_mux_data, bool donotsave);

	dtdemux::reset_type_t sdt_section_cb_(db_txn& txn, const sdt_services_t&services, const subtable_info_t& i,
														 mux_data_t* p_mux_data);
	dtdemux::reset_type_t sdt_section_cb(const sdt_services_t&services, const subtable_info_t& i);

	dtdemux::reset_type_t bat_section_cb(const bouquet_t& bouquet, const subtable_info_t& i);

	dtdemux::reset_type_t eit_section_cb_(epg_t& epg, const subtable_info_t& i);

	dtdemux::reset_type_t eit_section_cb(epg_t& epg, const subtable_info_t& i);

	mux_data_t* lookup_nit_from_sdt(db_txn& txn, uint16_t network_id, uint16_t ts_id);

	std::optional<chdb::mux_key_t>
	lookup_nit_key(db_txn& txn, uint16_t network_id, uint16_t ts_id);

	mux_data_t* add_fake_nit(db_txn& txn, uint16_t network_id, uint16_t ts_id, int16_t expected_sat_pos, bool from_sdt	);

	int deactivate();
	//int open();
	bool read_and_process_data_for_fd(int fd);

	void process_si_data();
	bool abort_on_wrong_sat() const;

	void load_movistar_bouquet();
	void load_skyuk_bouquet();

	void on_wrong_sat();
#if 0
/*
	confirm that the current mux is indeed on the right sat, to detect
	errors temporary errors due to dish rotationm and permanent errors due to diseqs
*/
	bool confirm_tuned_dvbs_mux(db_txn& wtxn,
															const chdb::dvbs_mux_t& si_mux, confirmed_by_t confirmer);
#endif

/*
	returns 1 if network  name matches database, 0 if no record was present and -1 if no match
*/
	int save_network(db_txn& txn, const nit_network_t& network, int sat_pos);


	bool check_tuned_mux_key(db_txn& txn, const chdb::mux_key_t& si_key);

	void add_sat(db_txn& txn, int16_t sat_pos);

	void init_scanning(scan_target_t scan_target_);
	void init(scan_target_t scan_target_);

	template<typename parser_t, typename... Args>
	auto add_parser(int pid, Args... args) {
		auto parser = stream_parser.register_pid<parser_t>(pid, args...);
		parsers.push_back(parser);
		if(pid!=dtdemux::ts_stream_t::PAT_PID)
			add_pid(pid);
		return parser;
	}

	void add_mux_from_nit(db_txn& wtxn, chdb::any_mux_t& mux, bool is_actual, bool is_tuned_mux,
		bool is_tuned_freq);

	void process_removed_services(db_txn& txn, chdb::mux_key_t& mux_key, ss::vector_<uint16_t>& service_ids);

	//for bouquets
	void process_removed_channels(db_txn& txn, const chdb::chg_key_t& chg_key, ss::vector_<uint16_t>& channel_ids);

	void check_timeouts();

	void scan_report();

	bool wrong_sat_detected() const {
		return tune_confirmation.on_wrong_sat;
	}

	bool unstable_sat_detected() const {
		return tune_confirmation.unstable_sat;
	}

	bool fix_mux(chdb::any_mux_t& mux);
	bool is_tuned_mux(const chdb::any_mux_t& mux);
	bool 	update_template_mux_parameters_from_frontend(chdb::any_mux_t& mux);
	chdb::update_mux_ret_t update_mux(db_txn& txn, chdb::any_mux_t& mux, system_time_t now,
																		chdb::update_mux_preserve_t::flags preserve,
																		bool tuned_mux, bool from_sdt);

	chdb::any_mux_t add_new_mux(db_txn& txn, chdb::any_mux_t& mux, system_time_t now);
	void fix_tune_mux_template();
	void handle_mux_change(db_txn& wtxn, chdb::any_mux_t& old_mux, chdb::any_mux_t& new_nux, bool is_tuned_mux);
	void finalize_scan(bool done);
	mux_data_t* tuned_mux_in_nit();

public:
	void reset(bool is_retune);

	//void process_psi(int pid, unsigned char* payload, int payload_size);
	active_si_stream_t(receiver_t& receiver,
										 const std::shared_ptr<stream_reader_t>& reader, bool is_embedded_si,
										 ssize_t dmx_buffer_size_=32*1024L*1024);
public:
		virtual ~active_si_stream_t();

};
