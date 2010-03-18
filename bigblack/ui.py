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


class Form(object):
    def __init__(self, action, method="GET", cls="form", id="", attr=[]):
        self.action = action
        self.method = method
        self.cls = cls
        self.id = id
        self.attr = attr
        self._elems = []

    def add_text(self, name, label, attr=[], cls=""):
        if cls == "":
            cls = label
        if cls:
            t = """<span class='%(cls)s'>
<label for='%(name)s'>%(label)s</label>
<input type='text' name='%(name)s'%(attr)s>
</span>"""
        else:
            t = """<span>
<label for='%(name)s'>%(label)s</label>
<input type='text' name='%(name)s'%(attr)s>
</span>"""

            d = dict(name=name,
                     label=label,
                     cls=cls,
                     attr=" " + htmlelements.build_attrs(attr))
            self._elems.append(t % d)

    def render(self):
        pass


class Menu(object):
    _templ = """
<div class="%(cls)s" id="%(id)s">
<ul>
%(body)s
</ul>
</div>
"""
    def __init__(self, cls="menu", id=""):
        self._class = cls
        self._id = id
        self._elements = []

    def add_item(self, item):
        self._elements.append(item)

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
                 cls=self._class)
        return self._templ % d

            
