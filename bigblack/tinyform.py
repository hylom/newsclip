#!/usr/bin/env python
#######################################################################
# tinyform.py - HTML form generator
#
# Copyright (c) hylom <hylomm at gmail.com>, 2009.
# 
# This file is released under the GPL.
#
#######################################################################
"""tinyform: HTML form generator"""

VERSION = "0.1.0"
VERSION_DATE = VERSION + " 06/16/2009"
VERSION_SPLIT = tuple(VERSION.split('.'))

class FormdataError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class form_element(object):
    """form elements' base class"""
    def attr2str(self, attr=None):
        """generate html tag's attribute string"""
        divider = " "
        if not attr:
            attr = self._attr
        myattr = dict(attr)
        if myattr.has_key("title"):
            del myattr["title"]
        if myattr.has_key("items"):
            del myattr["items"]

#        if not(attr.has_key("class")) and hasattr(self, "_name") and tf:
#            myattr["class"] = tf._classprefix + self._name

        attrs = ['%s="%s"' % (key, myattr[key]) for key in myattr]
        return divider.join(attrs)


class rawhtml(form_element):
    """raw html in forms"""
    def __init__(self, string):
        self._contents = string

    def as_html(self):
        """represent contents as html form"""
        return self._contents

#    def html(self, buf, tf):
#        buf.append(self._contents)

class input(form_element):
    """INPUT element"""
    def __init__(self, type, name, title="", **args):
        """initialize object."""
        self._type = type
        self._name = name
        self._title = title
        self._attr = dict(args)

    def as_html(self):
        """represent contents as html form"""
        return """<input type="%s" name="%s" %s>""" % (self._type,
                                                       self._name,
                                                       self.attr2str())

#    def html(self, buf, tf):
#        buf.append("""<input type="%s" name="%s" %s>""" % 
#                   (self._type, self._name, self.attr2str(tf=tf)))


class button(form_element):
    """BUTTON element"""
    def __init__(self, name, contents, **args):
        """initialize object."""
        self._contents = contents
        self._name = name
        self._attr = dict(args)

    def as_html(self):
        """represent contents as html form"""
        return """<button name="%s" %s>%s</button>""" % (self._name,
                                                         self.attr2str(),
                                                         self._contents.as_html())
    

class select(form_element):
    def __init__(self, name, contents, title="", **args):
        self._name = name
        self._title = title
        self._contents = contents
        self._attr = dict(args)

    def html(self, buf, tf):
        buf.append("""<select name="%s" %s>""" %
                   (self._name, self.attr2str()))
        for item in self._contents:
            item.html(buf, tf)
        buf.append("""</optgroup>""")


def options(**args):
    return [option(args[key], value=key) for key in args]

class option(form_element):
    def __init__(self, label="", value="", **args):
        self._label = label
        if value == "":
            self._value = label
        else:
            self._value = value
        for item in args:
            self._value = item
            self._label = args[item]

    def html(self, buf, tf):
        buf.append("""<option value="%s">%s</option>""" %
                   (self._value, self._label))


class optgroup(form_element):
    def __init__(self, label, contents, **args):
        self._label = label
        self._contents = contents
        self._attr = dict(args)

    def html(self, buf, tf):
        buf.append("""<optgroup label="%s" %s>""" %
                   (self.attr2str(), label))
        for item in self._contents:
            item.html(buf)
        buf.append("""</optgroup>""")


class textarea(form_element):
    def __init__(self, name, title="", value="", **args):
        self._name = name
        self._title = title
        self._value = value
        self._attr = dict(args)

    def html(self, buf, tf):
        buf.append("""<textarea name="%s" %s>%s</textarea>""" %
                   (self._name, self.attr2str(), self._value))
                   

class fieldset(form_element):
    def __init__(self, title, contents, **args):
        self._title = title
        self._contents = contents
        self._attr = dict(args)

    def html(self, buf, tf):
        # generate "fieldset"
        legend = self._title
        subitem = self._contents
        buf.append("<fieldset>")
        buf.append("<legend>" + legend + "</legend>")
        for item in self._contents:
            item.html(buf, tf)
        buf.append("</fieldset>")


class TinyForm(object):
    """TinyForm main class."""

    def __init__(self, mode="html"):
        """Creates TinyForm object."""
        self._mode = mode
        self._attr = {}

    def set_attr(self, key, value):
        """Set form tag's attribute."""
        self._attr[key] = value

    def set_classprefix(self, prefix):
        """Set classname's prefix for each element."""
        self._classprefix = prefix

    def get_classprefix(self):
        """Set classname's prefix for each element."""
        return self._classprefix

    def generate(self, form, params=None, **args):
        """Creates form from given parameter."""
        if self._mode == "html":
            return self.generate_html(form, params, args)
        else:
            raise Exception("mode %s isn't implemented." % mode)

    def _attrdict2str(self, attr):
        # generate "form" tag
        divider = " "
        myattr = dict(attr)
        if myattr.has_key("title"):
            del myattr["title"]
        if myattr.has_key("items"):
            del myattr["items"]

        if not(attr.has_key("class")) and attr.has_key("name"):
            myattr = dict(attr)
            myattr["class"] = self._prefix + attr["name"]

        attrs = ['%s="%s"' % (key, myattr[key]) for key in myattr]
        return divider.join(attrs)

    def _generate_html_recur(self, form, begin, end):
        # generate form elements
        for item in form:
            item.html(begin, self)

    def construct_tag(self, tag, attributes, xhtml_empty_tag=False):
        """Construct tag with given attributes.

        example:
        >>> tf = TinyForm()
        >>> attrs = {"href":"http://example.com/", "class":"anchor"}
        >>> tf.construct_tag("a", attrs)
        '<a href="http://example.com/" class="anchor">'
        >>> tf.construct_tag("a", attrs, True)
        '<a href="http://example.com/" class="anchor" />'
        """
        terms = [tag]
        for attr in attributes:
            terms.append('%s="%s"' % (attr, attributes[attr]))

        if xhtml_empty_tag:
            return "<" + " ".join(terms) + " />";
        else:
            return "<" + " ".join(terms) + ">";

    def generate_html(self, form, params=None, args={}):
        """Creates HTML form from given parameter."""

        # generate "form" tag
#        divider = " "
#        attrs1 = self._attrdict2str(self._attr)
#        attrs2 = self._attrdict2str(args)
#        attr = ("<form", attrs1, attrs2, ">")
        attrs = dict(self._attr)
        attrs.update(args)

        self._begin = [self.construct_tag("form", attrs)]
        self._end = ["</form>"]

        self._generate_html_recur(form, self._begin, self._end)
        return "\n".join(self._begin + self._end)

        
# for doctest 
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
