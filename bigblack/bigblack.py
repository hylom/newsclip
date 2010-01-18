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

import cgi
import sys
import os
import os.path
import ConfigParser
import marshal

VERSION = "0.1.0"
VERSION_DATE = VERSION + " 06/16/2009"
VERSION_SPLIT = tuple(VERSION.split('.'))


class BigBlack(object):
    """BigBlack main class"""

    def __init__(self):
        """Creates the BackBlack object"""
        self._init_plugins()

#### plugin system
    def _init_plugins(self):
        self._cfg_reader = None
        self._config = {}

    def regist_configreader(self, cls):
        self._cfg_reader = cls.__call__(self)


#### built-in configuration system
    def _builtin_load_config(self, config_dir=""):
        """load config file.

        @param configfile: config file's directory
        @type configfile: string
        """
        if config_dir:
            sys.path.insert(0, config_dir)

        from config import config as bb_cfg
        return bb_cfg

    def get_config(self, key, default=None):
        return self._config.get(key, default)

    def _load_config(self):
        if self._cfg_reader:
            self._config = self._cfg_reader.load_config()
        else:
            self._config = self._builtin_load_config()

#### env/parameter access functions
    def param(self, key):
        """return CGI parameter.

        @param key: name of parameter
        @type key: string
        """

        if os.environ.get("METHOD") in ("GET", "POST"):
            return None;

        #FIXME: if form's value is large file?
        try:
            return self._form.getvalue(key)
        except AttributeError:
            self._form = cgi.FieldStorage()
            return self._form.getvalue(key)

    def path_info(self):
        """
        return PATH_INFO.
        """
        pathinfo = os.environ.get("PATH_INFO", "")
        if os.name == "nt":
            scriptname = getScriptname()
            if pathinfo.startswith(scriptname):
                pathinfo = pathinfo[len(scriptname):]
        return pathinfo

    def script_name(self):
        """
        return CGI's script name.
        """
        return os.environ.get("SCRIPT_NAME", "")

#### HTTP/HTML manipulation functions
    def html_body(self, content=""):
        return """<body>
%s
</body>
""" % content
        
    def http_header(self, ctype="text/html; charset=utf-8"):
        """
        return HTTP header.

        @param ctype="text.html": content-type string.
        @type ctype: string
        """
        return "Content-type: %s\n" %(ctype)

    def html_header(self, **headers):
        """
        return HTML header.

        @param headers={}: header parameters.
        @type headers: dict
        """
        header_string = "<html>\n<head>\n"

        for key in headers:
            header_string += "  <%s>%s</%s>\n" % (key,headers[key],key)

        header_string += "</head>\n<body>"
        return header_string

    def html_footer(self):
        """
        return HTML footer.
        """
        return "</body></html>"

    def html_redirection(self, url):
        """
        return redirection HTML code.

        @param url: redirection url
        @type url: string
        """
        return """<html>
  <head>
    <meta http-equiv="refresh" content="0;url=%s">
  </head>
</html>""" %(url)

#### cgi exection dispatcher functions
    def run(self):
        self._load_config()

        if os.environ.get("METHOD") in ("GET", "POST"):
            return self.dispatch()
        else:
            return self.standalone()

    def standalone(self):
        self.root()

    def dispatch(self):
        p = self.path_info()
        pathspec = p.split("/")
        if len(pathspec) > 1:
            func = pathspec[1]
            try:
                f = getattr(self, func)
                f()
            except AttributeError:
                self.fallback()
        else:
            self.root()

    def root(self):
        print self.http_header()
        print self.html_header(title="BigBlack initial page")
        print """<h1>BigBlack initial page</h1>
<p>This is BigBlack initial root page.</p>
"""
        print self.html_footer()

