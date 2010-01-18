#!/usr/bin/env python
#######################################################################
# tinydb.py - Tiny Database module
#
# Copyright (c) hylom <hylomm at gmail.com>, 2009.
# 
# This file is released under the GPL.
#
#######################################################################
"""TinyDb: Tiny Database module"""

VERSION = "0.1.0"
VERSION_DATE = VERSION + " 06/16/2009"
VERSION_SPLIT = tuple(VERSION.split('.'))

import sqlite3
import os.path

class TinyDbError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TinyDbOrderdDict(dict):
    """
    Orderd dictionary class for TinyDb.
    """
    def __init__(self, datas):
        """
        initialize.

        @param datas: list of tuples which contains key & values pair.
        @type datas: sequence
        """
        
        dict.__init__(self, datas)
        self.seq = [item[0] for item in datas]

    def keys(self):
        """ list of keys """
        return self.seq

class TinyDbItem(object):
    """
    This is TinyDb's Item class.
    """
 
    def __init__(self):
        """
        initialize TinyDbItem

        """
   

class TinyDbSQLite(object):
    """
    This is TinyDb's main class.
    """
    def __init__(self, path_to_db):
        """
        initialize TinyDbSQLite.

        @param path_to_db: path to database
        @type path_to_db: string
        """
        self._path_to_db = path_to_db
        self._connection = None


    def _connect(self):
        if self._connection == None:
            self._connection = sqlite3.connect(self._path_to_db)
            self._connection.row_factory = sqlite3.Row


    def _cursor(self):
        self._connect()
        return self._connection.cursor()


    def _close_connect(self):
        if self._connection != None:
            self._connection.close()
            self._connection = None


    def close(self):
        self._close_connect()

    def exists(self):
        if self._connection:
            return True
        else:
            return os.path.isfile(self._path_to_db)


    def begin(self):
        """begin transaction"""
        cur = self._cursor()
        cur.execute("""BEGIN TRANSACTION;""")
        cur.close()


    def commit(self):
        """commit transaction"""
        self._connection.commit()
        

    def select(self, table_name, expr=None):
        if expr != None:
            sql_cmd = "SELECT * FROM %s WHERE %s" % (table_name, expr)
        else:
            sql_cmd = "SELECT * FROM %s" % table_name
        cur = self._cursor()
        cur.execute(sql_cmd)
        return cur
    

    def insert(self, table_name, param):
        """
        do insert with given paramater.

        @param table_name: name of table to create
        @type table_name: string

        @param param: paramater
        @type param: TinyDbOrderdDict
        """

        keys = param.keys()
        sql_cmd = """INSERT INTO "%s" (\n""" % table_name
        sql_cmd = sql_cmd + ",\n".join(keys) + "\n"
        sql_cmd = sql_cmd + ") VALUES (\n"
        sql_cmd = sql_cmd + ", ".join(("?",)*len(keys))
        sql_cmd = sql_cmd + ")"

        cur = self._cursor()
        t = tuple([param[key] for key in keys])

        cur.execute(sql_cmd, t)
        cur.close()
        self.commit()

    def get_db_path(self):
        """return database file's path."""
        return self._path_to_db

    def create_table(self, table_name, prototype):
        """
        create table to database.

        @param table_name: name of table to create
        @type table_name: string

        @param prototype: list of (keyname, type) tuple
        @type prototype: list of tuple
        """

        col_list = [tpl[0] for tpl in prototype]
        type_list = [tpl[1] for tpl in prototype]

        self._create_table(table_name, col_list, type_list)

    def create_table_from_Dict(self, table_name, prototype):
        """
        create table to database.

        @param table_name: name of table to create
        @type table_name: string

        @param prototype: column and type data
        @type prototype: TinyDbOrderdDict
        """

        col_list = prototype.keys()
        type_list = [prototype[x] for x in col_list]

        self._create_table(table_name, col_list, type_list)


    def _create_table(self, table_name, col_list, type_list):
        """
        create table to database.

        @param table_name: name of table to create
        @type table_name: string

        """
        if len(col_list) != len(type_list):
            raise TinyDbError("len(col_list) isn't equal to len(type_list).")

        sql_cmd = "CREATE TABLE %s (\n" % table_name
        cmds = []
        for (column, type) in zip(col_list, type_list):
            cmds.append("  " + column + "\t" + type)

        sql_cmd = sql_cmd + ",\n".join(cmds) + "\n);"
        cur = self._cursor()

        # print sql_cmd

        cur.execute(sql_cmd)
        cur.close()
    
