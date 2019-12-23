# Written by Brendan O'Connor, brenocon@gmail.com, www.anyall.org
#  * Originally written Aug. 2005
#  * Posted to gist.github.com/16173 on Oct. 2008

#   Copyright (c) 2003-2006 Open Source Applications Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging
import os
import sys
import re
import types
from datetime import datetime

logs_folder = os.path.dirname(os.path.realpath(__file__)) + "/logs/"

# Set the logger
logger = logging.getLogger()
# apply debug mode based on django debug mode

# create log handlers
file_handler = logging.FileHandler(filename=logs_folder + '/{:%Y%m%d}.log'.format(datetime.now()))
stream_handler = logging.StreamHandler(sys.stdout)
#formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | {%(pathname)s:%(lineno)04d} | %(message)s')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
# add handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

"""
More info can be found here: https://gist.github.com/brendano/16173

Have all your function & method calls automatically logged, in indented outline
form - unlike the stack snapshots in an interactive debugger, it tracks call
structure & stack depths across time!

It hooks into all function calls that you specify, and logs each time they're
called.  I find it especially useful when I don't know what's getting called
when, or need to continuously test for state changes.  (by hacking this file)

Originally inspired from the python cookbook:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/198078

Currently you can
 - tag functions or individual methods to be autologged
 - tag an entire class's methods to be autologged
 - tag an entire module's classes and functions to be autologged

CAVEATS:
 - certain classes barf when you logclass() them -- most notably,
   SWIG-generated wrappers, and perhaps others.
"""

# Globally incremented across function calls, so tracks stack depth
indent = 0
indStr = '  '

# ANSI escape codes for terminals.
#  X11 xterm: always works, all platforms
#  cygwin dosbox: run through |cat and then colors work
#  linux: works on console & gnome-terminal
#  mac: untested


BLACK = "\033[0;30m"
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
RED = "\033[0;31m"
PURPLE = "\033[0;35m"
BROWN = "\033[0;33m"
GRAY = "\033[0;37m"
BOLDGRAY = "\033[1;30m"
BOLDBLUE = "\033[1;34m"
BOLDGREEN = "\033[1;32m"
BOLDCYAN = "\033[1;36m"
BOLDRED = "\033[1;31m"
BOLDPURPLE = "\033[1;35m"
BOLDYELLOW = "\033[1;33m"
WHITE = "\033[1;37m"

NORMAL = "\033[0m"


def indentlog(message):
    global log, indStr, indent
    # print >>log, "%s%s" %(indStr*indent, message
    logger.info("%s%s" % (indStr * indent, message))


def shortstr(obj):
    """
    Where to put gritty heuristics to make an object appear in most useful
    form. defaults to __str__.
    """
    if "wx." in str(obj.__class__) or obj.__class__.__name__.startswith("wx"):
        shortclassname = obj.__class__.__name__
        # shortclassname = str(obj.__class__).split('.')[-1]
        if hasattr(obj, "blockItem") and hasattr(obj.blockItem, "blockName"):
            more_info = "block:'%s'" % obj.blockItem.blockName
        else:
            more_info = "at %d" % id(obj)
        return "<%s %s>" % (shortclassname, more_info)
    else:
        return str(obj)


def format_all_args(args, kwds):
    """
    makes a nice string representation of all the arguments
    """
    allargs = []
    for item in args:
        allargs.append('%s' % shortstr(item))
    for key, item in kwds.items():
        allargs.append('%s=%s' % (key, shortstr(item)))
    formatted_args = ', '.join(allargs)
    if len(formatted_args) > 150:
        return formatted_args[:146] + " ..."
    return formatted_args


def logmodules(list_of_modules):
    for m in list_of_modules:
        logmodule(m)


def logmodule(module, log_match=".*", log_not_match="nomatchasfdasdf"):
    """
    WARNING: this seems to break if you import SWIG wrapper classes
    directly into the module namespace ... logclass() creates weirdness when
    used on them, for some reason.

    @param module: could be either an actual module object, or the string
                   you can import (which seems to be the same thing as its
                   __name__).  So you can say logmodule(__name__) at the end
                   of a module definition, to log all of it.
    """

    def allow(s):
        return re.match(log_match, s) and not re.match(log_not_match, s)

    if isinstance(module, str):
        d = {}
        exec("import %s" % module in d)
        import sys
        module = sys.modules[module]

    names = module.__dict__.keys()
    for name in names:
        if not allow(name):
            continue

        value = getattr(module, name)
        if isinstance(value, type):
            setattr(module, name, logclass(value))
            logger.info("autolog.logmodule(): bound %s" % name)
        elif isinstance(value, types.FunctionType):
            setattr(module, name, logfunction(value))
            logger.info("autolog.logmodule(): bound %s" % name)


def logfunction(the_function, display_name=None):
    """a decorator."""
    if not display_name:
        display_name = the_function.__name__

    def _wrapper(*args, **kwds):
        global indent
        argstr = format_all_args(args, kwds)

        # Log the entry into the function
        indentlog("%s%s%s  (%s) " % (BOLDRED, display_name, NORMAL, argstr))


        indent += 1
        returnval = the_function(*args, **kwds)
        indent -= 1

        return returnval

    return _wrapper


def logmethod(the_method, display_name=None):
    """use this for class or instance methods, it formats with the object out front."""
    if not display_name:
        display_name = the_method.__name__

    def _method_wrapper(self, *args, **kwds):
        """Use this one for instance or class methods"""
        global indent

        argstr = format_all_args(args, kwds)
        selfstr = shortstr(self)

        # print >> log,"%s%s.  %s  (%s) " % (indStr*indent,selfstr,methodname,argstr)
        indentlog("%s.%s%s%s  (%s) " % (selfstr, BOLDRED, the_method.__name__, NORMAL, argstr))

        indent += 1

        if the_method.__name__ == 'OnSize':
            indentlog("position, size = %s%s %s%s" % (BOLDBLUE, self.GetPosition(), self.GetSize(), NORMAL))

        returnval = the_method(self, *args, **kwds)

        indent -= 1

        return returnval

    return _method_wrapper


def logclass(cls, method_as_functions=False, log_match=".*", log_not_match="asdfnomatch"):
    """
    A class "decorator". But python doesn't support decorator syntax for
    classes, so do it manually::

        class C(object):
           ...
        C = logclass(C)

    @param method_as_functions: set to True if you always want methodname first
    in the display.  Probably breaks if you're using class/staticmethods?
    """

    def allow(s):
        return re.match(log_match, s) and not re.match(log_not_match, s) and \
               s not in ('__str__', '__repr__')

    names_to_check = cls.__dict__.keys()

    for name in names_to_check:
        if not allow(name):
            continue
        # unbound methods show up as mere functions in the values of
        # cls.__dict__,so we have to go through getattr
        value = getattr(cls, name)

        if method_as_functions and callable(value):
            setattr(cls, name, logfunction(value))
        elif isinstance(value, types.MethodType):
            # a normal instance method
            if value.__self__ is None:
                setattr(cls, name, logmethod(value))

            # class & static method are more complex.
            # a class method
            elif value.__self__ == cls:
                w = logmethod(value.__func__,
                              display_name="%s.%s" % (cls.__name__, value.__name__))
                setattr(cls, name, classmethod(w))
            else:
                assert False

        # a static method
        elif isinstance(value, types.FunctionType):
            w = logfunction(value,
                            display_name="%s.%s" % (cls.__name__, value.__name__))
            setattr(cls, name, staticmethod(w))
    return cls


class LogMetaClass(type):
    """
    Alternative to logclass(), you set this as a class's __metaclass__.

    It will not work if the metaclass has already been overridden (e.g.
    schema.Item or zope.interface (used in Twisted)

    Also, it should fail for class/staticmethods, that hasnt been added here
    yet.
    """

    def __new__(mcs, classname, bases, classdict):
        logmatch = re.compile(classdict.get('log_match', '.*'))
        lognotmatch = re.compile(classdict.get('log_not_match', 'nevermatchthisstringasdfasdf'))

        for attr, item in classdict.items():
            if callable(item) and logmatch.match(attr) and not lognotmatch.match(attr):
                classdict['_H_%s' % attr] = item  # rebind the method
                classdict[attr] = logmethod(item)  # replace method by wrapper

        return type.__new__(mcs, classname, bases, classdict)

