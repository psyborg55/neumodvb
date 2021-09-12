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

#define LMDBXX_TXN_ID
#include "lmdb++.h"
#include "stackstring.h"
#include "util/logger.h"
#include "util/util.h"
#include "screen.h"
#ifndef HIDDEN
#define HIDDEN __attribute__((visibility("hidden")))
#endif
#ifndef EXPORT
#define EXPORT __attribute__((visibility("default")))
#endif


#define TEMPLATE_EVENT_ID 0xffffffff
class dbdesc_t;
struct record_desc_t;
struct schema_entry_t;

using all_schemas_t = ss::vector_<schema_entry_t>;

class neumodb_t {
private:
	int load_schema_(db_txn& txn);
	bool is_open_{false};
protected:
	bool autoconvert {false};

	struct db_needs_upgrade_exception : public std::runtime_error {
		using  std::runtime_error::runtime_error;
	};


	neumodb_t(bool readonly=false, bool is_temp=false, bool autoconvert=false);
public:
	int extra_flags{0};
	bool is_open() const {
		return is_open_;
	}
	bool is_temp=false;
	bool use_dynamic_keys = false;
	ss::vector<dynamic_key_t,4> dynamic_keys;

	bool has_temp_db() {
		return true; //todo
	}
	/*Note we cannot remove dynamic_keys or add dynamic keys after we start using the database:
		we would have to reload all records for that
	*/
	template<typename T>
	int add_dynamic_key(std::initializer_list<T> args) {
		use_dynamic_keys = true;
		int idx= dynamic_keys.size();
		dynamic_keys.push_back(dynamic_key_t(args));
		return idx;
	}

	int add_dynamic_key(const dynamic_key_t& k) {
		use_dynamic_keys = true;
		int idx= dynamic_keys.size();
		dynamic_keys.push_back(k);
		return idx;
	}

	bool readonly = false;
	bool use_log = false;
	int last_txn_id = -1;
	std::condition_variable activity_cv;
	std::mutex activity_mutex; //used to protect last_txn_id and monitors

	std::shared_ptr<lmdb::env> envp;
	ss::string<16> db_type;
	bool schema_is_current = true; //true if the schema stored in the database equals that of the code
	std::shared_ptr<dbdesc_t> dbdesc;
	//dbdesc_t dbdesc

	lmdb::dbi dbi{0}; //dangerous but convenient; could lead to errors if open is not called
	lmdb::dbi dbi_index{0}; //dangerous but convenient; could lead to errors if open is not called

	lmdb::dbi dbi_log{0}; //dangerous but convenient; could lead to errors if open is not called

	int wait_for_activity(int old_txnid);

	neumodb_t(const neumodb_t& main);

	neumodb_t& operator = (const neumodb_t& other);
  void init(const all_schemas_t& current_schema);

	int load_and_check_schema();


	void clean_stale_readers(const char* dbpath) {
		int dead=0;
		int rc= mdb_reader_check(*envp, &dead);
		if(rc) {

			LOG4CXX_FATAL(logger, "lmdb error db="<< dbpath << " err=" <<  mdb_strerror(rc));

		} else if (rc>0) {

		LOG4CXX_DEBUG(logger, "Cleaned " <<  dead << " stale readers for db=" << dbpath);

		}
	}


	/*!
		TODO: replace open with a combination of
		1. 	void env_open(const char* dbpath, size_t mapsize = 128*1024u*1024u)
		2. void open(const char* dbpath, const char*prefix, size_t mapsize = 128*1024u*1024u)
       void open(neumodb_t & other, const char*prefix)
			 This allows opening the same file twcie but with different databases
			 It also requires that env be replaced with a shared pointer
    Remaning porblem:
		put_record(txn...) and find functions rely on txn.db to find the proper dbi for inserting/finding a record,
		so there would need to
		be distinction between txn and some newly defined database handle type. Alternatively, dbi must be derived from
		the record type (poor solution)

		Possible solution? Use child transaction?
		Note: A parent transaction and its cursors may not issue any other operations than mdb_txn_commit and mdb_txn_abort while it has active child transactions.
=> Perhaps we store a singleton transaction in an  environment specific structure and handle everything with child transactions?
	 */
	void open(const char* dbpath, bool allow_degraded_mode = false,
						const char* table_name = NULL, bool use_log =true, size_t mapsize = 256*1024u*1024u);

	void open_without_log(const char* dbpath, bool allow_degraded_mode = false,
												const char* table_name = NULL, size_t mapsize = 256*1024u*1024u)
		{
			bool use_log =false;
			open(dbpath, allow_degraded_mode, table_name, use_log, mapsize);
		}

	void open_temp(const char* where, bool allow_degraded_mode = false,
						const char* table_name = NULL, size_t mapsize = 128*1024u*1024u);

	void open_secondary(const char * table_name, bool allow_degraded_mode=false);
	void drop_table(bool dodel);

	void close();

	template<class data_t>
	auto tcursor(db_txn& txn) {
		return  db_tcursor<data_t>(txn, this->dbi/*, find_type*/);
	}


	template<class data_t>
	auto tcursor(db_txn& txn, const ss::bytebuffer_& key_prefix) {
		return  db_tcursor<data_t>(txn, dbi, key_prefix);
	}


	auto generic_cursor(db_txn& txn) {
		return  db_cursor(txn, dbi);
	}


	/*
		gets the very first record in the database
	 */
	auto generic_get_first(db_txn&txn) {
		lmdb::val k{};
		auto c = generic_cursor(txn);
		c.get(k, nullptr, MDB_FIRST);
		return c;
	}

	/*
		for an index cursor we need to know the index type of the secondary key;
		However, if no iteration is performed with the cursor, key_type can be left unspecified
	*/
	template<class data_t>
	auto tcursor_index(db_txn& txn, const ss::bytebuffer_& key_prefix) {
		return  db_tcursor_index<data_t>(txn, dbi, dbi_index, key_prefix);
	}

	template<class data_t>
	auto tcursor_index(db_txn& txn) {
		return  db_tcursor_index<data_t>(txn, dbi, dbi_index);
	}


	//cursor for navigating the log table
	template<class data_t>
	auto tcursor_log(db_txn& txn, const ss::bytebuffer_& key_prefix) {
		return  db_tcursor_index<data_t>(txn, dbi, dbi_log, key_prefix);
	}

	template<class data_t>
	auto tcursor_log(db_txn& txn) {
		return  db_tcursor_index<data_t>(txn, dbi, dbi_log);
	}


	db_txn wtxn() {
		if(!is_open()) {
			dterror("Attempting to access non opened lmdb database");
			assert(0);
		}
		return db_txn(*this, 0);
	}
	db_txn rtxn() {
		if(!is_open()) {
			dterror("Attempting to access non opened lmdb database");
			assert(0);
		}
		return  db_txn(*this, MDB_RDONLY);
	}

	virtual ~neumodb_t();

	virtual int convert_record(db_cursor& from_cursor, db_txn& to_txn, uint32_t type_id, unsigned int put_flags=0)
		{ assert (0);
			return -1;
		};

	virtual void store_schema(db_txn& txn, unsigned int put_flags)
		{ assert (0);
		};


};


/*!
	read an old database record by record using from_txn, transforming the records to
	the latest format and storing them in to_txn
	put_flags can be set to MDB_APPEND for databases (e.g. recdb) which
	are always appended. This results in a lot of space saving as no free room
	is left between records.
*/
int convert_db(neumodb_t& from_db, neumodb_t& to_db, unsigned int put_flags);

namespace schema {
struct neumo_schema_t;
};

void print_schema(schema::neumo_schema_t& s);

bool check_schema(const dbdesc_t& stored, const dbdesc_t& current);

template<typename T> EXPORT const char* enum_to_str(const T& val);
template<typename T> EXPORT  bool enum_is_valid(const T& val);

std::ostream& operator<<(std::ostream& os, field_matcher_t::match_type_t match_type);
std::ostream& operator<<(std::ostream& os, const field_matcher_t& matcher);
