#!/usr/bin/env python

from bigblack.bigblack import BigBlack
import bigblack.bbtinydb

class testcgi(BigBlack):
    def root(self):
        print self.http_header()
        print self.html_header(title="root")
        print self.html_body("<p>this is root</p>")
        print "<p>path_info:%s</p>" % self.path_info()
        print self.html_footer()

    def hoge(self):
        print self.http_header()
        print self.html_header(title="/hoge")
        print self.html_body("<p>this is /hoge</p>")
        print "<p>path_info:%s</p>" % self.path_info()
        print self.html_footer()
        

testcgi().run()
