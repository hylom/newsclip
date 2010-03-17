#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# fbdb.py
# This file provided by MIT License (see below).
#
# Copyright (c) 2010 hylom <hylomm@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""fbdb.py - File-Based Database system"""

import os.path
import os
import urllib
import pickle

_VERSION = "0.1.0.0"
_DBSTR = "fddb-ver:" + _VERSION

class DbError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FbDb(object):
    """File-based key-value database."""
    _DB_FILE = ".fbdb"
    def __init__(self, basedir):
        self._basedir = os.path.abspath(basedir)
        self._db = dict()
        self._lockstate = {}

    def _quote(self, str):
        return urllib.quote(str, "")

    def _unquote(self, str):
        return urllib.quote(str)

    def _get_db_path(self, database):
        return os.path.join(self._basedir, self._quote(database))

    def exists_db(self, database):
        """check if given db is exists"""
        db_path = self._get_db_path(database)
        dbf = os.path.join(db_path, self._DB_FILE)
        return os.path.isfile(dbf)

    def create_db(self, database):
        """create new database"""
        db_path = self._get_db_path(database)
        dbf = os.path.join(db_path, self._DB_FILE)
        if os.path.isfile(dbf):
            raise DbError("database %s is exists." % db_path)
        if os.path.exists(db_path):
            raise DbError("database %s is exists, and not database." % db_path)

        os.makedirs(db_path)
        f = open(dbf, "w")
        f.write(_DBSTR)
        f.close()

    def delete_db(self, database):
        if self.exists_db(database):
            db_path = self._get_db_path(database)
            dbf = os.path.join(db_path, self._DB_FILE)
            """TODO:"""
            if os.path.isfile(dbf):
                os.removedirs(db_path)
        else:
            raise DbError("database %s is not exists or not database." % db_path)

    def query_keys(self, key="*"):
        """"TODO:"""
        pass

    def create(self, database, key, value):
        """create item with key and value to database."""
        db_path = self._get_db_path(database)
        if self.exists_db(database):
            db_path = self._get_db_path(database)
            path = os.path.join(db_path, key)
            if os.path.exists(path):
                raise DbError("database %s, key %s is exists." % (database, key))
            f = open(path, "w")
            pickle.dump(value, f)
            f.close()
        else:
            raise DbError("database %s is not exists." % database)

    def retrive(self, database, key, default=None):
        """retrive item with key."""
        if self.exists_db(database):
            db_path = self._get_db_path(database)
            path = os.path.join(db_path, key)
            if os.path.exists(path):
                f = open(path, "r")
                ret = pickle.load(f)
                f.close()
                return ret
            else:
                return default
        else:
            raise DbError("database %s is not exists." % database)

    def update(self, database, key, value):
        """update item with key and value to database."""
        if self.exists_db(database):
            db_path = self._get_db_path(database)
            path = os.path.join(db_path, key)
            if os.path.exists(path):
                f = open(path, "w")
                f.write(value)
                f.close()
            else:
                raise DbError("key %s is not exists, in database %s." % (key, database))
        else:
            raise DbError("database %s is not exists. path: %s" % database)
               
    def delete(self, database, key, default=None):
        """delete item in given database."""
        if self.exists_db(database):
            db_path = self._get_db_path(database)
            path = os.path.join(db_path, key)
            if os.path.exists(path):
                os.remove(path)
            else:
                raise DbError("database %s, key %s is not exists." % (database, key))
        else:
            raise DbError("database %s is not exists." % database)

    def lock(self, database):
        pass

    def unlock(self, database):
        pass
