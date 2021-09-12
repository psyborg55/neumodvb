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
namespace ss {
	template<typename T>
	struct header_t;

};

template<typename T>
struct ss::header_t {

	class allocated_layout;
	template<int N> class extended_inline_layout;
	class view_layout;

	class PACKED extended_inline_sub_header_t {
		template<int N> friend class extended_inline_layout;
		const uint32_t  capacity_        : 24;  //total amount of space available for storage in extended_inline case
		uint32_t size_ = 0;                 //size of stored string, excluding the zero character,

	public:
		extended_inline_sub_header_t(int capacity_)
		: capacity_(capacity_)
		{}

	};


	class PACKED allocated_sub_header_t {
		friend class allocated_layout;
		const uint32_t  capacity_        : 24;  //total amount of space available for storage in extended_inline case
		uint32_t size_ = 0;             //size of stored string, excluding the zero character,
		//if extended_inline_= 0 and allocated_=0
		void* allocated_buffer_ = 0;
	allocated_sub_header_t() = delete;

	};


	class PACKED view_sub_header_t {
		friend class view_layout;
		const uint32_t  capacity_        : 24;  //total amount of space available for storage in view
		uint32_t size_ = 0;             //size of stored string, excluding the zero character,
		//if extended_inline_= 0 and allocated_=0
		void* buffer_ = 0;
	public:
		view_sub_header_t(int capacity_)
		: capacity_(capacity_)
		{}



	};


	struct PACKED header_byte_t {
		const bool extended_inline_       : 1; // value=0:  after the 16 byte header there is no
		//additional space to store inline data (constant)
		bool allocated_             : 1; //value=0: data stored inline
		//value=1: allocated using new
		const bool view_                  : 1; //value=1: this is a view, referencing externa data
		unsigned int  size_       : 4;  //size of stored string, excluding the zero character,
		//only for NON extended inline.
		bool inited  :1;

		header_byte_t(bool has_extended_inline, bool is_view)
		: extended_inline_(has_extended_inline)
		, allocated_(false)
		, view_(is_view)
		, size_(0)
		, inited(true)
		{}
	};

	template<int N>
	class PACKED inline_layout {
		header_byte_t h;
		typename std::aligned_storage<sizeof(T), alignof(T)>::type data[N];
	public:

	inline const T* get_buffer() const {
		return &reinterpret_cast<const T&>(data[0]);
	}

	inline T* get_buffer() {
		return &reinterpret_cast<T&>(data[0]);
	}

	};

	template<int N>
	class PACKED extended_inline_layout {
		header_byte_t h;
		extended_inline_sub_header_t ei; //7 bytes
		typename std::aligned_storage<sizeof(T), alignof(T)>::type data[N];
	public:

	inline void set_size (int size) {
		assert(size <= ei.capacity_);
		ei.size_ = size;
	}

	inline int get_size () const {
		return ei.size_;
	}

	inline int get_capacity () const {
		return ei.capacity_;
	}

	inline const T* get_buffer() const {
		return &reinterpret_cast<const T&>(data[0]);
	}

	inline T* get_buffer() {
		return &reinterpret_cast<T&>(data[0]);
	}


	};

	template<int N>
	struct PACKED data_with_capacity {
		uint32_t capacity_{0};
		typename std::aligned_storage<sizeof(T), alignof(T)>::type data_[N];

		T* data() {
			return reinterpret_cast<T*>(&data_[0]);
		}
		};


	class PACKED allocated_layout {
		header_byte_t h;
		allocated_sub_header_t a; //4 bytes
		allocated_layout() = delete;

	public:
	using data_with_capacity_t = data_with_capacity<1>;

	inline const data_with_capacity_t* allocated_buffer() const  {
		return (const data_with_capacity_t*)(((const allocated_layout*)this)->a.allocated_buffer_);
	}

	inline data_with_capacity_t* allocated_buffer()  {
		return (data_with_capacity_t*)(((allocated_layout*)this)->a.allocated_buffer_);
	}

	inline void set_allocated_buffer(data_with_capacity_t* d) {
		a.allocated_buffer_ = d;
	}

	T* buffer() {
		return &allocated_buffer()->data[0];
	}

	inline int get_capacity () const {
		return allocated_buffer()->capacity_;
	}

	inline void set_capacity (int capacity) const {
		return allocated_buffer()->capacity_ = capacity;
	}

	inline void set_size (int size) {
		assert((!allocated_buffer() && size ==0) || size <= get_capacity());
		a.size_ = size;
	}

	inline int get_size () const {
		return a.size_;
	}


	};

	class PACKED view_layout {
		header_byte_t h;
		view_sub_header_t v; //4 bytes
		view_layout() = delete;

	public:
	inline void set_size (int size) {
		assert(size <= v.capacity_);
		v.size_ = size;
	}

	inline int get_size () const {
		return v.size_;
	}

	inline int get_capacity () const {
		return v.capacity_;
	}

	inline const T* get_buffer() const {
		return (const T*) v.buffer_;
	}

	inline T* get_buffer() {
		return (T*) v.buffer_;
	}


	inline void set_buffer(T* view_buffer, int view_size) {
		set_size(view_size);
		v.buffer_ = view_buffer;
	}

	};

	/////static members ///////////////////////

  //number of elements which can be stored in 16 bytes, which is the minimum we reserv
	constexpr static int inline_capacity() {
		if(sizeof(inline_layout<1>) > 16)
			return 0; // 15 bytes will be lost
		auto s2 = sizeof(inline_layout<2>);
		auto s1 = sizeof(inline_layout<1>);
		return (16-s1)/(s2-s1)+1; // (16-s1) = bytes left for more than 1 element;  (16-s1)/(s2-s1) = number of extra elements after the first 1
	}


	//how many extra elements to reserve to end up with the right number of entries
	template<int num_entries>
	constexpr static int extended_inline_to_reserve() {
		if (num_entries<= inline_capacity())
			return 0;
		return sizeof(extended_inline_layout<num_entries>)- sizeof(ss::header_t<T>);
	}



	////data/////////////////////////////
	header_byte_t h;
	union {
		extended_inline_sub_header_t ei;//when created with a size template argument
		char none;                      //when created without a size template argument
		allocated_sub_header_t a;       //should never be creted
		view_sub_header_t v;
	} u{{0}};



	/*
		buffer_size: number of elements our caller will ensure space for after the header
		Depending on the value of buffer size, the header may be of size 1 byte, or size 4:
		buffer_size=0: header will consist only of header_byte_t (1 byte); inline capacity =0
		buffer_size>0: header will consist only of header_byte_t (1 byte); inline capacity = buffer_size if all of this fits in 16 bytes,
		otherwise, header will consist of  extended_inline_sub_header_t (4 bytes); inline capacity = buffer_size
		is_view-1 indicates that the header is used as a view to non-ownded data. This should always have buffer_size=0
	*/
	header_t(int buffer_size, bool is_view) :
		h(!is_view && (buffer_size > inline_capacity()), is_view) {
		static_assert(sizeof(*this)==16);
		if(h.extended_inline_)
			new(&u.ei) extended_inline_sub_header_t(buffer_size);
		else if(h.view_)
			new(&u.ei) view_sub_header_t(buffer_size);
	}

	inline bool is_allocated() const {
		return h.allocated_;
	}

	inline bool is_view() const {
		return h.view_;
	}

	/*
		buffer pointing to a data structure containing a 4 byte header (to store allocated size)
		and memory for allocated objects
	*/
	data_with_capacity<1>* allocated_buffer() const {
		assert(h.inited);
		if(h.allocated_) {
			assert(!h.view_);
			return ((allocated_layout*)this)->allocated_buffer();
		}
		return nullptr;
	};

	inline const T* buffer() const {
		assert(h.inited);
		if(h.allocated_)
			return &allocated_buffer()->data()[0];
		else if (h.view_) {
			return ((view_layout*)this)->get_buffer();
		} else if(h.extended_inline_) {
			return ((extended_inline_layout<1>*)this)->get_buffer();
		}
		return ((inline_layout<1>*)this)->get_buffer();
	}


	T* buffer()  {
		return const_cast<T*>(const_cast<const header_t*>(this)->buffer());
	}


	data_with_capacity<1>* steal_allocated_buffer() {
		assert(h.inited);
		assert(h.allocated_);
		auto ret = allocated_buffer();
		h.allocated_ = false;
		assert(!h.view_);
		((allocated_layout*)this)->set_allocated_buffer(nullptr);
		h.allocated_=false;
		return ret;
	}

	void set_size(int size) {
		assert(h.inited);
		if(h.allocated_)
			((allocated_layout*)this)->set_size(size);
		else if(h.view_)
			((view_layout*)this)->set_size(size);
		else if(h.extended_inline_) {
			((extended_inline_layout<1>*)this)->set_size(size);
		} else {
			assert(size <= (int) inline_capacity());
			h.size_ = size;
		}
	}

	inline int size() const {
		assert(h.inited);
		if(h.allocated_)
			return ((allocated_layout*)this)->get_size();
		else if(h.view_)
			return ((view_layout*)this)->get_size();
		else if(h.extended_inline_)
			return ((extended_inline_layout<1>*)this)->get_size();
		else
			return h.size_;
	}


	inline int capacity() const {
		assert(h.inited);
		if(h.view_)
			return ((view_layout*)this)->get_capacity();
		else if(h.allocated_)
			return ((allocated_layout*)this)->get_capacity();
		else if (h.extended_inline_)
			return ((extended_inline_layout<1>*)this)->get_capacity();
		else
			return inline_capacity();
	}


	void set_inline_buffer() {
		assert(h.inited);
		assert(!h.view_);
		h.allocated_ = false;
		h.size_ = 0; //DANGEROUS
		if(h.extended_inline_) {
			((extended_inline_layout<1>*)this)->set_size(0); //DANGOROUS
		}
	}

	void set_external_buffer(data_with_capacity<1>* ext_buffer) {
		assert(h.inited);
		h.allocated_ = true;
		assert(!h.view_);
		auto* pa = (allocated_layout*)this;
		pa->set_allocated_buffer(ext_buffer);
		set_size(0);
	}


	void set_view_buffer(T* view, int view_size) {
		assert(h.inited);
		h.allocated_ = false;
		assert(h.view_);
		h.size_ = 0; //DANGEROUS
		auto* pa = (view_layout*)this;
		pa->set_buffer(view, view_size);
	}



};
