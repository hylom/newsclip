#!/usr/bin/env python
#######################################################################
# ui.py - BigBlack UserInterface class
#
# Copyright (c) hylom <hylomm at gmail.com>, 2009.
# 
# This file is released under the GPL.
#
#######################################################################
"""ui.py: ui module"""

import htmlelements

class Menu(object):
    templ = """
<div class="%(class)s" id="%(id)s">
<ul>
%(body)s
</ul>
</div>
"""
    def __init__(self, class="menu", id=""):
        self._class = class
        self._id = id
        self._elements = []

    def add_link(self, text, url, attrs=[]):
        if len(attrs):
            l = list(attrs)
        else:
            l = []
        l.append(("href", "url"))
        t = htmlelements.build_begin_tag("a", l)
        t = t + text + "</a>"
        self._elements.append(t)

    def render(self):
        elems = ["<li>" + e + "</li>" for e in self._elements]
        d = dict(body="\n".join(elems),
                 id=self._id,
                 class=self._class)
        return templ % d

            
