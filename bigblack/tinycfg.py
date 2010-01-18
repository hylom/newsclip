#!/usr/bin/env python
#######################################################################
# bigblack.py - BigBlack the CGI Framework
#
# Copyright (c) hylom <hylomm at gmail.com>, 2009.
# 
# This file is released under the GPL.
#
#######################################################################
"""BigBlack: CGI Framework"""

import os
import os.path
import ConfigParser
import marshal
import bigblack

VERSION = "0.1.0"
VERSION_DATE = VERSION + " 06/16/2009"
VERSION_SPLIT = tuple(VERSION.split('.'))

class TinyCfg(object):
    def __init__(self, bb):
        self.bb = bb

    def _update_config_cache(self):
        fpath = self.bb.get_config("appconfig", None) + ".cache"
        f = open(fpath, "w")
        marshal.dump(bb._config, f)
        f.close()

    def _load_config_cache(self):
        fpath = self.bb.get_config("appconfig", None) + ".cache"
        f = open(fpath, "r")
        c = marshal.load(f)
        f.close()
        return c
        
    def load_config(self):
        cf = self.bb.get_config("appconfig", None)
        if cf == None:
            self.bb._config = {}
            return

        cache_path = cf + ".cache"
        if os.path.exists(cache_path) and os.path.getmtime(cache_path) > os.path.getmtime(cache_path):
            self.bb._config = self._load_config_cache()
            return

        self._config = {}
        c = ConfigParser.SafeConfigParser()
        c.read(cf)
        for sec in c.sections():
            self.bb._config[sec] = {}
            for opt in c.options(sec):
                self.bb._config[sec][opt] = c.get(sec, opt)
        _update_config_cache(self)


