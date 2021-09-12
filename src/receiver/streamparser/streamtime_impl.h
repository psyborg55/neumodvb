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

#define PACKED __attribute__((packed))
#include <iostream>
#include <iomanip>



namespace dtdemux {
	std::ostream& operator<<(std::ostream& os, const pts_dts_t& a);

	inline std::ostream& operator<<(std::ostream& os, const data_range_t& r) {
		int packet = (r.start_bytepos())/188;
		int64_t offset = r.start_bytepos() -packet*(int64_t)188;//offset of start in current packet
		//packet[offset of cursor w.r.t. start packet, offset of end w.r.t. start packet
		return  os <<  std::setw(10) << packet << ":[" << (r.start_bytepos()+offset) << ", " << (r.len()+offset) << "]";
	}
}
