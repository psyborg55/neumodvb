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
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> //for std::optional
#include <pybind11/stl_bind.h>
#include "spectrum_algo.h"

namespace py = pybind11;


static float windowed_max(float* p, int starti, int endi) {
	auto res = std::numeric_limits<float>::lowest();
	for (int i = starti; i < endi; ++i)
		res = std::max(res, p[i]);
	return res;
}

/*
	overlapping when both left aligned


    +------------+
		|     2      |
 		+------------+ y2
		x2           |
		             |
  +------------+ |
	|     1      |
	+------------+ y1
  x1           |
               |+------------+ y2+h
               ||     2      |
				       |+------------+ y2
				       |x2           |
				                     |
				                     |
                             x2+w

*/

/*

overlapping when left + right aligned


   +------------+
   |     1      |
 	 +------------+ y1
   |     +------------+
   |     |     2      |
	 x1    +------------+ y2
                      |
                      |


  x1           |
               |+------------+ y2+h
               ||     2      |
				       |+------------+ y2
				       |x2           |
				                     |
				                     |
                             x2+w

 */


static bool overlapping(int x1, float y1, int x2, float y2, int w1, int h1, int w2, int h2) {
	if(x2< x1) {
		std::swap(x1, x2);
		std::swap(w1, w2);
	}
	if(y2< y1) {
		std::swap(y1, y2);
		std::swap(h1, h2);
	}
	if (x2 >= x1 + w1)
		return false;
	assert(x2 >= x1);
	if (y2 > y1 + h1)
		return false;
	if (y2 +h2 < y1)
		return false;
	return true;
}


static bool horizontally_overlapping(int x1, int x2, int w1, int w2) {
	if(x2< x1) {
		std::swap(x1, x2);
		std::swap(w1, w2);
	}
	if (x2 >= x1 + w1)
		return false;
	return true;
}

enum {
	STICK_OUT_RIGHT = 0,
	STICK_OUT_LEFT = 1,
	STICK_OUT_MASK = 1,
	DOUBLE_LINE = 0,
	SINGLE_LINE = 2,
	LINE_MASK = 2,
} annot_flags_t;



/*
	sig: spectrum signal
	annotx: list of annotation  x coordinates
	w/h=width/height of annotation box
	offset = vertical offset of annotation box
*/
static py::object find_annot_locations(py::array_t<float> sig, py::array_t<int> annotx, int w, float h, float offset) {
	py::buffer_info infosig = sig.request();
	if (infosig.ndim != 1)
		throw std::runtime_error("Bad number of dimensions");
	auto* psig = (float*)infosig.ptr;
	int stridesig = infosig.strides[0] / sizeof(int);
	int w2 = w*2;
	int h2 = h/2*1.2;
	py::buffer_info infoannotx = annotx.request();
	if (infoannotx.ndim != 1)
		throw std::runtime_error("Bad number of dimensions");
	int* px = (int*)infoannotx.ptr;
	int stridex = infoannotx.strides[0] / sizeof(int);
	int nx = infoannotx.shape[0];

	py::array_t<float, py::array::f_style> annoty(infoannotx.shape);
	py::buffer_info infoannoty = annoty.request();
	int strideannoty = infoannoty.strides[0] / sizeof(float);
	auto* py = (float*)infoannoty.ptr;

	py::array_t<uint8_t, py::array::f_style> leftrightflag(infoannotx.shape);
	py::buffer_info infoleftrightflag = leftrightflag.request();
	// int strideannoty = infoannoty.strides[0]/sizeof(int);
	auto* plr = (uint8_t*)infoleftrightflag.ptr;
	int n = infosig.shape[0];
	int na = infoannotx.shape[0];
	auto plr_left = std::vector<uint8_t>(na, 0);
	auto plr_right = std::vector<uint8_t>(na, 0);

	std::vector<float> lefty;
	std::vector<float> righty;
	lefty.resize(na);	 /* labels right aligned, vertical position increases from left to right
												lefty[i] is the height of the label whose right side has x-coordinate px[i]
										 */
	righty.resize(na); /* labels left aligned, vertical position increases from right to left
												lefty[i] is the height of the label whose left side has x-coordinate px[i]
										 */
	float initial_maxy = std::numeric_limits<float>::lowest();
	float initial_miny = std::numeric_limits<float>::max();
	for (int i = 0; i < n; ++i) {
		initial_maxy = std::max(initial_maxy, psig[i]);
		initial_miny = std::min(initial_miny, psig[i]);
	}

	auto left_overlapping = [&](int i) ->std::tuple<bool, float> {
		float worst;
		bool overlap =false;
		for (int j=i-1; j>=0 ; --j) {
			if (px[j] <= px[i] - w2) {
				//no overlap possible
				return {overlap, worst};
			}
			int wj = (plr_left[j] & SINGLE_LINE) ? w2 : w;
			int wi = (plr_left[i] & SINGLE_LINE) ? w2 : w;
			if (horizontally_overlapping(px[j] -wj ,  px[i] -wi , wj, wi)) {
				if(overlap)
					worst = std::max(worst, lefty[j]);
				else
					worst = lefty[j];
				overlap = true;
			}
		}
			return {overlap, worst};
	};

	for (int i = 0; i < na; ++i) {
		auto x = px[i];
		assert(x < n);
		if (i > 0) {
			auto [overlap, worst ] = left_overlapping(i);
			if(overlap) {
				lefty[i] = windowed_max(psig, std::max(0, x + 1 - w2), x+1) + offset;
				lefty[i] = std::max(lefty[i], worst) +
					((plr_left[i-1] & SINGLE_LINE) ? h : h)*1.5;
			} else {
				lefty[i] = windowed_max(psig, std::max(0, x + 1 - w), x+1) + offset;
			}
			plr_left[i] = (overlap ? SINGLE_LINE : DOUBLE_LINE) | STICK_OUT_LEFT;
		} else {
			lefty[i] = windowed_max(psig, std::max(0, x + 1 - w), x+1) + offset;
			plr_left[i] = DOUBLE_LINE | STICK_OUT_LEFT;
		}
	}


	auto right_overlapping = [&](int i) ->std::tuple<bool, float> {
		float worst;
		bool overlap =false;
		for (int j=i+1; j<na ; ++j) {
			if (px[j] >= px[i] + w2) {
				//no overlap possible
				return {overlap, worst};
			}
			int wj = (plr_right[j] & SINGLE_LINE) ? w2 : w;
			int wi = (plr_right[i] & SINGLE_LINE) ? w2 : w;

			if (horizontally_overlapping(px[j], px[i], wj, wi)) {
				if (overlap)
					worst = std::max(worst, righty[j]);
				else
					worst = righty[j];
				overlap = true;
			}
		}
			return {overlap, worst};
	};


	for (int i = na - 1; i >= 0; --i) {
		auto x = px[i];

		assert(x < n);
		if (i < na - 1) {
			auto [overlap, worst ] = right_overlapping(i);
			if(overlap) {
				righty[i] = windowed_max(psig, x, std::min(n, x + w2)) + offset;
				righty[i] = std::max(righty[i], worst) +
					((plr_right[i+1] & SINGLE_LINE) ? h2 : h)*1.5;
			} else {
				righty[i] = windowed_max(psig, x, std::min(n, x + w)) + offset;
			}
			plr_right[i] = (overlap ? SINGLE_LINE : DOUBLE_LINE) | STICK_OUT_RIGHT;
		} else {
			righty[i] = windowed_max(psig, x, std::min(n, x + w)) + offset;
			plr_right[i] = DOUBLE_LINE | STICK_OUT_RIGHT;
		}
	}

	float maxy = std::numeric_limits<float>::lowest();
	for (int i = 0; i < na; ++i) {
		auto y1 = lefty[i];
		auto y2 = righty[i];
			if ( i==0) {
				plr[i] = plr_left[i]; //make i stick out to the left
				py[i] = y1;
			} else {
				auto left_overlapping = [&]() {
					for (int j=i-1; j>=0 ; --j) {
						if (px[j]+w2 <= px[i] -w2) {
							//no overlap possible
							return false;
						}
						if ((plr[j] & STICK_OUT_MASK) == STICK_OUT_RIGHT) {
							//j sticks out to the right and is left aligned
							bool j_is_one_line = (plr_right[j] & LINE_MASK) == SINGLE_LINE;
							bool i_is_one_line = (plr_left[j] & LINE_MASK) == SINGLE_LINE;
							int wj = j_is_one_line ? w2: w;
							int hj = j_is_one_line ? h2: h;
							hj=h*1.5;
							int wi = i_is_one_line ? w2: w;
							wi =w2;

							int hi = i_is_one_line ? h2: h;
							hi=h*1.5;
							if (overlapping(px[j], py[j], px[i] -wi, y1, wj, hj, wi, hi))
								return true;
						} else {
							//j sticks out to the left and is right aligned
							bool j_is_one_line = (plr_left[j] & LINE_MASK) == SINGLE_LINE;
							bool i_is_one_line = (plr_left[j] & LINE_MASK) == SINGLE_LINE;
							int wj = j_is_one_line ? w2: w;
							int hj = j_is_one_line ? h2: h;
							hj=h;
							int wi = i_is_one_line ? w2: w;
							int hi = i_is_one_line ? h2: h;
							hi=h;
							if (overlapping(px[j] -wj, py[j], px[i] -wi, y1, wj, hj, wi, hi))
								return true;
						}
					}
					return false;
				};
				if((plr[i - 1] & STICK_OUT_MASK) == STICK_OUT_RIGHT) {
					/*i-1 sticks out to the right and is left aligned
						we decide if we continue like that for i (which means we follow the increasing trend),
						or rather make i stick out to the left.
						The latter is useful only if y1 < y2 - h
						It is possible only if there is no overlap between i pointing to the left and
						any i-j sticking out to the right
					*/

					if (y1 < y2 - h && ! left_overlapping()) {
						plr[i] = plr_left[i]; //make i stick out to the left
						py[i] = y1;
						//+ (((plr_left[i] & LINE_MASK) == SINGLE_LINE)? h2:h);

					} else {
						//continue sticking out to the right
						plr[i] = plr_right[i];
						py[i] = y2;
					}
				} else {
					/*i-1 sticks out to the left and is right aligned
						we decide if we continue like that for i, or rather make i stick out to the right.
						The latter is useful only if y2 < y1 - h
					*/
					if (y2 < y1 - h  || left_overlapping()) {
						plr[i] = plr_right[i]; //make i stick out to the right
						py[i] = y2;
					} else {
						//continue sticking out to the left
						plr[i] = plr_left[i];
						py[i] = y1;
					}
				}
			}
			maxy = std::max(py[i], maxy);
			auto increase = py[i] - psig[px[i]];
	}

	return py::make_tuple(annoty, leftrightflag);
}



PYBIND11_MODULE(pyspectrum, m) {
	m.doc() = R"pbdoc(

	)pbdoc";
	;
	m
		.def("find_annot_locations", &find_annot_locations)
		;
}
