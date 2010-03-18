#!/usr/bin/env python
#######################################################################
# htmlelements.py - HTML Elements utilities
#
# Copyright (c) hylom <hylomm at gmail.com>, 2010.
# 
# This file is released under the GPL.
#
#######################################################################
"""htmlelements: HTML Elements utilitiesk"""

def build_attrs(attrs):
    """attrs: tuple contents (attribute, value)"""
    items = [tag,]
    for (attr, val) in attrs:
        if val:
            t = "%s='%s'" % (attr, val)
        else:
            t = attr
        items.append(t)
    return " ".join(items)


def build_begin_tag(tag, attrs):
    """
    tag: HTML tagname
    attrs: tuple contents (attribute, value)
    """
    items = [tag,]
    for (attr, val) in attrs:
        if val:
            t = "%s='%s'" % (attr, val)
        else:
            t = attr
        items.append(t)
    return "<%s>" % " ".join(items)

def build_begin_end_tag(tag, attrs):
    """
    tag: HTML tagname
    attrs: tuple contents (attribute, value)
    """
    items = [tag,]
    for (attr, val) in attrs:
        if val:
            t = "%s='%s'" % (attr, val)
        else:
            t = attr
        items.append(t)
    return "<%s/>" % " ".join(items)

def build_end_tag(tag):
    """
    tag: HTML tagname
    """
    return "</%s>" % tag



