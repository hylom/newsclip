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

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import RichTraceback

class Http(object):
    """BigBlack http render module"""
    def __init__(self, bb):
        self._bb = bb

    def header(self, ctype="text/html; charset=utf-8"):
        """
        return HTTP header.

        @param ctype="text.html": content-type string.
        @type ctype: string
        """
        return "Content-type: %s\n" %(ctype)

 
class Html(object):
    """BigBlack html render module"""
    def __init__(self, bb):
        self._bb = bb

    def body(self, content):
        """return <body>%s</body>"""
        return """<body>
%s
</body>
""" % content
        
    def header(self, **headers):
        """
        return HTML header (<html><head></head>

        @param headers={}: header parameters.
        @type headers: dict
        """
        header_string = "<html>\n<head>\n"

        for key in headers:
            header_string += "  <%s>%s</%s>\n" % (key,headers[key],key)

        header_string += "</head>\n<body>"
        return header_string

    def footer(self):
        """
        return HTML footer (</html>)
        """
        return "</html>"

    def redirection(self, url):
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


class Cgi(object):
    """BigBlack cgi utilities module"""
    def __init__(self, bb):
        self._bb = bb
        self._form = cgi.FieldStorage()

    def param(self, key):
        """return CGI parameter.

        @param key: name of parameter
        @type key: string
        """

        if os.environ.get("METHOD") in ("GET", "POST"):
            return None;

        #FIXME: if form's value is large file?
        try:
            return self._form.getfirst(key)
        except AttributeError:
            self._form = cgi.FieldStorage()
            return self._form.getfirst(key)

    def path_info(self):
        """
        return PATH_INFO.
        """
        pathinfo = os.environ.get("PATH_INFO", "")
        if os.name == "nt":
            scriptname = self.script_name()
            if pathinfo.startswith(scriptname):
                pathinfo = pathinfo[len(scriptname):]
        return pathinfo

    def script_name(self):
        """
        return CGI's script name.
        """
        return os.environ.get("SCRIPT_NAME", "")

    def new_dict(self):
        return dict(self._form)


class Config(object):
    """BigBlack configuration module"""
    def __init__(self, bb):
        self._bb = bb
        from config import config as bb_cfg
        self._config = bb_cfg

    def get_value(self, key, default=None):
        """return config variable's value"""
        return self._config.get(key, default)

    def get_dir(self, key, default=None):
        if key not in self._config:
            return default
        p = os.path.expanduser(self._config[key])
        return os.path.abspath(p)

    def new_dict(self):
        return dict(self._config)
        

class View(object):
    """BigBlack View module"""
    def __init__(self, bb):
        self._bb = bb

    def render(self, template_name, stash):
        tpath = self._bb.config.get_dir("template_dir", None)
        tl = TemplateLookup(directories=[tpath],
                            input_encoding="utf-8",
                            output_encoding="utf-8",
                            default_filters=['decode.utf8'])
#                            format_exceptions=True)

        t = tl.get_template(template_name)
        vars = self._bb.config.new_dict()
        vars.update(stash)
        vars["DEBUG_MSG"] = self._bb.debugger.debug_string()
        try:
            return t.render(**vars)
        except:
            traceback = RichTraceback()
            for (filename, lineno, function, line) in traceback.traceback:
                print "File %s, line %s, in %s" % (filename, lineno, function)
                print line, "\n"
            print "%s: %s" % (str(traceback.error.__class__.__name__), traceback.error)
            sys.exit(-1)


class NullDebugger(object):
    def __init__(self, bb):
        self._bb = bb

    def debug_string(self):
        return ""

class Debugger(NullDebugger):
    def debug_string(self):
        params = self._bb.cgi.new_dict()
        p = ["%s: %s<br/>" % (key, params[key]) for key in params]
        str = """
<hr/>
This is debug message.
<hr/>
 Parameters:<br/>
%s
<hr/>
"""
        return str % "\n".join(p)


class Dispatch(object):
    """BigBlack dispatcher class"""
    def __init__(self, bb):
        self._bb = bb

    def go(self):
        p = self._bb.cgi.path_info()
        pathspec = p.split("/")
        if len(pathspec) > 1:
            func = pathspec[1]
            try:
                f = getattr(self._bb, "h_" + func)
                f()
            except AttributeError:
                self._bb.fallback()
        else:
            self._bb.root()


class BigBlack(object):
    """BigBlack main class"""

    def __init__(self):
        """Creates the BackBlack object"""
        self.html = Html(self)
        self.http = Http(self)
        self.cgi = Cgi(self)
        self.config = Config(self)
        self.dispatch = Dispatch(self)
        self.view = View(self)
        self.debugger = NullDebugger(self)


#### cgi exection dispatcher functions
    def run(self):
        if os.environ.get("METHOD") in ("GET", "POST"):
            return self.dispatch.go()
        else:
            return self.standalone()

    def fallback(self):
        self.fallback()

    def standalone(self):
        self.root()

    def fallback(self):
        self.root()

    def root(self):
        print self.http.header()
        print self.html.header(title="BigBlack initial page")
        print """<h1>BigBlack initial page</h1>
<p>This is BigBlack initial root page.</p>
"""
        print self.html.footer()

