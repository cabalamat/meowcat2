# butil.py = basic utilities

"""
Basic utilities for Python 3.x.
"""

from typing import *
import os, os.path
import sys
import html
import inspect
import functools
import pprint

#---------------------------------------------------------------------

def normalizePath(p: str, *pathParts: List[str]) -> str:
    """ Normalize a file path, by expanding the user name and getting
    the absolute path.
    :param p: a path to a file or directory
    :param pathParts: optional path parts
    :return the same path, normalized
    """
    p1 = os.path.abspath(os.path.expanduser(p))
    if len(pathParts)>0:
        allPathParts = [ p1 ]
        allPathParts.extend(pathParts)
        p1 = os.path.join(*allPathParts)
    p2 = os.path.abspath(p1)
    return p2
normalisePath=normalizePath # alternate spelling
join=normalizePath # it works like os.path.join, but better

#---------------------------------------------------------------------
# formatting functions

def form(fs:str, *args, **kwargs) -> str:
    """ an easier to use version of python's format(). It works the same
    except that %s is converted to {} and %r is converted to {!r}
    """
    if args or kwargs:
        fs2 = fs.replace("%s", "{}").replace("%r", "{!r}")
        r = fs2.format(*args, **kwargs)
    else:
        r = fs
    return r    

def pr(fs:str, *args, **kwargs):
    """ print to stdout """
    sys.stdout.write(form(fs, *args, **kwargs))

def epr(fs:str, *args, **kwargs):
    """ print to stderr """
    sys.stderr.write(form(fs, *args, **kwargs))

def prn(fs:str, *args, **kwargs):
    """ print to stdout, with \n at end """
    sys.stdout.write(form(fs, *args, **kwargs))
    sys.stdout.write("\n")
    
def eprn(fs:str, *args, **kwargs):
    """ print to stderr, with \n at end """
    sys.stderr.write(form(fs, *args, **kwargs))
    sys.stderr.write("\n")


#---------------------------------------------------------------------
# debugging functions

def dpr(formatStr, *args, **kwargs):
    """ debugging version of pr(), prn().
    Prints to stderr, prefixes with function name and line
    number, adds newline.
    """
    caller = inspect.stack()[1]
    fileLine = caller[2]
    functionName = caller[3]
    s = form(formatStr, *args, **kwargs)
    prefix = "%s():%d: " % (functionName, fileLine)
    sys.stderr.write(prefix + s + "\n")

_PRINTARGS_DEPTH = 0
_PRINTARGS_INDENT = "| "

def printargs(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        global _PRINTARGS_DEPTH
        argStr = ", ".join([repr(a) for a in args])
        kwargStr = ", ".join(["%s=%r"%(k,v) for v,k in enumerate(kwargs)])
        comma = ""
        if argStr and kwargStr: comma = ", "
        akStr = argStr + comma + kwargStr
        eprn('%s%s(%s)', _PRINTARGS_INDENT * _PRINTARGS_DEPTH,
           fn.__name__, akStr)
        _PRINTARGS_DEPTH += 1
        retVal = fn(*args, **kwargs)
        _PRINTARGS_DEPTH -= 1
        if retVal != None:
            eprn("%s%s(%s) => %r", _PRINTARGS_INDENT * _PRINTARGS_DEPTH,
               fn.__name__, akStr,
               retVal)
        return retVal
    return wrapper

def pretty(ob, indent:int=4) -> str:
    pp = pprint.PrettyPrinter(indent)
    s = pp.pformat(ob)
    return s

#---------------------------------------------------------------------

def myStr(x):
    """ My version of the str() conversion function. This converts any
    type into a str. If x is a unicode, it is converted into a utf-8
    bytestream.
    @param x = a value of some type
    @return::str
    """
    if x is None:
        return ""
    elif type(x)==unicode:
        return x.encode('utf-8')
    else:
        return str(x)
    
HTML_DECODE = [ ('&#39;', "'"),
                ('&quot;', '"'),
                ('&lt;', '<'),
                ('&gt;', '>'),
                ('&amp;', '&') ]

def attrEsc(s, noneIs=''):
    """ Escapes a string for html attribute special characters
    @param s::str = a string
    @return::str = the equivalent string with chanracters escaped
    """
    if s==None: return noneIs
    if not (isinstance(s, str) or isinstance(s,unicode)):
        s = myStr(s)
    hdc = HTML_DECODE[-1:] + HTML_DECODE[:-1]
    for encoded, decoded in hdc:
        s = s.replace(decoded, encoded)
    return s


def htmlEsc(s: str) -> str:
    return html.escape(s)

def toBytes(b) -> bytes:
    """ convert anything to a byte array """
    if isinstance(b, bytes):
        return b
    elif isinstance(b, str):
        return bytes(b, 'utf-8')
    else:
        return bytes(str(b), 'utf-8')
      

#---------------------------------------------------------------------

class Struct:
    """ an anonymous object whose fields can be accessed using dot
    notation.
    See <http://norvig.com/python-iaq.html>
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __repr__(self):
        keys = sorted(self.__dict__.keys())
        args = ["%s=%r" % (key, self.__dict__[key])
                for key in keys]
        return 'Struct(%s)' % ', '.join(args)

    def hasattr(self, key):
        return self.__dict__.has_key(key)

#---------------------------------------------------------------------


def exValue(f, orValue):
    """ Evaluate function f. If it returns a value, return it.
    If it throws an exception, return (orValue) instead
    @param f::function
    @param orValue
    """
    r = orValue
    try:
        r = f()
    except:
        r = orValue
    return r


#---------------------------------------------------------------------


#end
