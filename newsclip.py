#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# newsclip.py
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
"""newsclip.py - news clipping system"""
import cgi
import cgitb; cgitb.enable()
import hashlib

from bigblack.bigblack import BigBlack, Debugger
from bigblack.session import Session
from bigblack.fbdb import FbDb

class NewsClipApp(BigBlack):
    "news clipping system main application class"
    def __init__(self):
        "NewsClipApp constructor"
        BigBlack.__init__(self)
        self.debugger = Debugger(self)
        db = FbDb(self.config.get_dir("storage_dir"))
        self._db = db
        self.session = Session(db)

# subroutines
    def _login(self):
        uname = self.cgi.getfirst("loginname")
        passwd = self.cgi.getfirst("passwd")
        if self._db.exists("users"):
            pass #if uname and passwd:
        else:
            self._setup()

    def _setup(self):
        self.view.render("setup.html", dict(title="newsclip setup"))

# handlers
    def h_setup(self):
        if self.cgi.getfirst("setup") != "1":
            print self.redirect("")
            return

        uname = self.cgi.getfirst("loginname")
        passwd = self.cgi.getfirst("passwd")
        
        if uname and passwd:
            s = hashlib.sha1()
            s.update(passwd)
            d = dict(uname=uname, passwd=s.hexdigest())
            self._db.create_db("users")
            self._db.create("users", uname, d)
        self.redirect("")

    def root(self):
        if not self._db.exists("users"):
            return self._setup()

        if self.cgi.getfirst("login") == "1":
            return self._login()

        self.view.render("login.html", dict(title="newsclip login"))

if __name__ == '__main__':
    app = NewsClipApp()
    app.run()

