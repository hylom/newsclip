#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""test for ui.py"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath("."))

import ui

class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_menu(self):
        """test ui.Menu #1"""
        m = ui.Menu("menu", "test_menu")
        m.add_link("this is test", "http://example.com/")
        m.add_item("<span class='right'>hogehoge</span>")
        t = m.render()

        t_ok = """
<div class="menu" id="test_menu">
<ul>
<li><a href='url'>this is test</a></li>
<li><span class='right'>hogehoge</span></li>
</ul>
</div>
"""
        self.failUnlessEqual(t, t_ok, "invalid output:" + t)

if __name__ == '__main__':
    unittest.main()

