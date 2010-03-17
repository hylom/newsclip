#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# session.py
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
"""session.py - session manager"""

import Cookie
import hashlib
import time

class SimpleSession(Cookie.SimpleCookie):
    "session object"
    bb = None
    salt = None
    @classmethod
    def init(cls, bb, salt):
        cls.bb = bb
        cls.salt = salt

    def __init__(self):
        Cookie.SimpleCookie.__init__(self)
        h = self.bb.cgi.get_env("HTTP_COOKIE")
        if h:
            self.load(h)
        else:
            s = hashlib.sha1()
            s.update(self.salt)
            s.update(time.asctime())
            self["sid"] = s.hexdigest()
            self["sid"]["path"]  = "/"

    def save(self):
        self.bb.http.append_header(self.output())


class Session(SimpleSession):
    "database associated session"
    @classmethod
    def init(cls, bb, salt, storage, database):
        cls.bb = bb
        cls.salt = salt
        cls.storage = storage
        cls.database = database
        if not storage.exists_db(database):
            storage.create_db(database)

    def retrive(self, key, default=None):
        return self.storage.retrive(self.database, key, default)

    def update(self, key, value):
        if self.storage.retrive(self.database, key, None):
            return self.storage.update(self.database, key, value)
        else:
            return self.storage.create(self.database, key, value)

