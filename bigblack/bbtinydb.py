#!/usr/bin/env python
#######################################################################
# bbtinydb.py - Tiny Database subsystem for BigBlack CGI Framework.
#
# Copyright (c) hylom <hylomm at gmail.com>, 2009.
# 
# This file is released under the GPL.
#
#######################################################################
"""BBTinyDb: Tiny Database subsystem for BigBlack CGI Framework"""

VERSION = "0.1.0"
VERSION_DATE = VERSION + " 06/16/2009"
VERSION_SPLIT = tuple(VERSION.split('.'))

import os.path

import tinydb
import bigblack


#class BBTinyDb(bigblack.BigBlack):
def get_database(self, database):
    db_path = os.path.join(self.get_config("database_dir"), database + ".db")
    db = tinydb.TinyDbSQLite(db_path)
    return db;

# append class function
bigblack.BigBlack.get_database = get_database

