#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""test for ui.py"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath("../"))

import bigblack
import session
import fbdb

class TestSequence(unittest.TestCase):

    def setUp(self):
        self.bb = bigblack.BigBlack()
        self.db = fbdb.FbDb(".")
        session.Session.init(self.bb, "qwerty", self.db, "test_db")

    def test_Session(self):
        #os.environ = dict()
        s = session.Session()
        t1_val = "this_is_test1_value"
        t2_val = "this_is_test2_value"
        s.update("test1", t1_val)
        s.update("test2", t2_val)
        s.save()
        sid = s["sid"]
        h = self.bb.http.header()
        print h

        os.environ = dict(HTTP_COOKIE="sid=%s;" % sid)
        s2 = session.Session()
        self.failUnlessEqual(s2.retrive("test1"), t1_val)
        self.failUnlessEqual(s2.retrive("test2"), t2_val)

        self.db.delete_db("test_db")

if __name__ == '__main__':
    unittest.main()

