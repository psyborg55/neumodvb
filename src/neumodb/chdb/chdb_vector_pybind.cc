/*
 * Neumo dvb (C) 2019-2021 deeptho@gmail.com
 *
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
#include "neumodb/chdb/chdb_extra.h"
#include "stackstring/stackstring_pybind.h"
#include <pybind11/pybind11.h>
#include <stdio.h>

namespace py = pybind11;

void export_chdb_vectors(py::module& m) {
	using namespace chdb;
	export_ss_vector(m, uint32_t);
	export_ss_vector(m, int32_t);
	export_ss_vector(m, uint16_t);
	export_ss_vector(m, int16_t);
	export_ss_vector(m, int8_t);
	export_ss_vector(m, service_t);
	export_ss_vector(m, dvbs_mux_t);
	export_ss_vector(m, dvbc_mux_t);
	export_ss_vector(m, dvbt_mux_t);
	export_ss_vector(m, sat_t);
	export_ss_vector(m, lnb_t);
	export_ss_vector(m, lnb_network_t);
	export_ss_vector(m, fe_delsys_t);
	export_ss_vector(m, epg_type_t);
	export_ss_vector(m, fe_t);
}
