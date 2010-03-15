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

class Session(object):
    "session manager"
    def __init__(self, bb, storage, salt):
        self._bb = bb
        self._storage = storage
        self._salt = salt
        
    def new_session(self, param, expire="None"):
        c = Cookie.SimpleCookie()
        
        s = hashlib.sha1()
        s.update(self._salt)
        s.update(time.asctime())
        c["sid"] = s.hexdigest()
        c["sid"]["path"]  = "/"
        self._bb.http.append_header(c.output())
