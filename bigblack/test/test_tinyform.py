#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""geeral test for tinyform.py"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath("."))

import tinyform

class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_construct(self):
        select_items = (tinyform.option(item1="その1"),
                        tinyform.option(item2="その2"),
                        tinyform.option(item3="その3"),
                        tinyform.option(item4="その4"))
        formdata = ( 
            tinyform.fieldset("inputs", (
                    tinyform.input(type="text", name="text1", title="textbox:", value="text!"),
                    tinyform.input(type="password", name="passwd1", title="password:", value="hoge"),
                    tinyform.input(type="checkbox", name="check1", title="check", value="hoge"),
                    tinyform.input(type="submit", name="submit", value="go"),
                    tinyform.input(type="hidden", name="hidden1", value="hidden")
                    )),
            tinyform.select("select1", select_items,
                            title="select:", size="4"),
            tinyform.textarea(name="text2", title="textarea:", rows="4", cols="40")
            )

        params = dict(text1="texthoge",
                      check1=1,
                      hidden1="hidden",
                      text2="foobarhogehoge",
                      select1="item2"
                      )
                      
        tf = tinyform.TinyForm()
        tf.set_attr("class", "tinyform")
        tf.set_attr("method", "get")
        tf.set_attr("action", "cgi.pl")
        tf.set_classprefix("form_")
        
        form = tf.generate(formdata, params=params)
        print "==== test output: ===="
        print form
        print "==== end of test output ===="

if __name__ == '__main__':
    unittest.main()

