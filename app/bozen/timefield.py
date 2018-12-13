# timefield.py = date and time fields

"""
Fields for time and date representation.


The date and timer formats used here are based on ISO8601 and especially 
on RFC3339 which defines a subset of ISO8601.

Dates are stored like this: "1985-04-12"
Instances in time are stored like this: "1985-04-12T23:20:50"
Time-of-day is stored like this: "23:59:00"

"""

from typing import *
import datetime
import re

from . import butil
from .butil import *
from . import bozenutil

from .fieldinfo import fieldIndex, FieldInfo, cssClasses

#---------------------------------------------------------------------
# regular expressions for time formats
# note that seconds field can be "60" for leap seconds

validDate=re.compile("[0-9]{4}-[0-1][0-9]-[0-3][0-9]")
def isValidDate(s: str) -> bool:
    return bool(validDate.fullmatch(s[:10]))

validDate8=re.compile("[0-9]{4}[0-1][0-9][0-3][0-9]")
def isValidDate8(s: str) -> bool:
    return bool(validDate8.fullmatch(s[:8]))

validDateTime=re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}"
    "T[0-2][0-9]:[0-5][0-9]:[0-6][0-9]")
def isValidDateTime(s: str) -> bool:
    return bool(validDateTime.fullmatch(s))

validTod=re.compile("[0-2][0-9]:[0-5][0-9]:[0-6][0-9]")

def isValidTod(s: str) -> bool:
    return bool(validTod.fullmatch(s))

#---------------------------------------------------------------------

class BzDate(str):
    """ the Bozen date class """
    
    def __new__(cls, s):
        #dpr("s=%r:%s", s, type(s))
        if isinstance(s, str):
            if isValidDate(s): # yyyy-mm-dd
                return super().__new__(cls, s[:10])
            if isValidDate8(s): # yyyymmdd
                s2 = "%s-%s-%s" % (s[0:4], s[4:6], s[6:8])
                return super().__new__(cls, s2)
            else:    
                errMsg = form("String %r wrongly formatted for BzDate," 
                    "should be 'yyyy-mm-dd'", s)
                raise ValueError(errMsg)
        elif isinstance(s, (datetime.date,datetime.datetime)):
            s2 = "%04d-%02d-%02d" % (s.year, s.month, s.day)
            return super().__new__(cls, s2)
        else:
            s = ""
        
            
    def __repr__(self) -> str:
        r = "BzDate(%r)" % (str(self),)
        return r
    
    def toTuple_ymd(self) -> Tuple[int,int,int]:
        """ to tuple of (year, month, day) """
        y = butil.exValue(lambda: int(self[0:4]), 2000)
        mon = butil.exValue(lambda: int(self[5:7]), 1)
        day = butil.exValue(lambda: int(self[8:10]), 1)
        return (y, mon, day)
    
    def toTuple_ymdhms(self) -> Tuple[int,int,int,int,int,int]:
        """ to tuple of (year, month, day, hour, minute, second) """
        y = butil.exValue(lambda: int(self[0:4]), 2000)
        mon = butil.exValue(lambda: int(self[5:7]), 1)
        day = butil.exValue(lambda: int(self[8:10]), 1)
        day = butil.exValue(lambda: int(self[8:10]), 1)
        return (y, mon, day, 0, 0, 0)
    
    def to_date(self) -> datetime.date:
        """ convert to datetime.date """
        y, m, d = self.toTuple_ymd()
        return datetime.date(y, m, d)
        
    def to_datetime(self) -> datetime.datetime:
        """ convert to datetime.datetime """
        y, m, d = self.toTuple_ymd()
        return datetime.datetime(y, m, d)
    
    def formatDate(self, formatStr: str) -> str:
        dt = self.to_date()
        s = dt.strftime(formatStr)
        return s
    
    def addDays(self, numDays: int) -> 'BzDate':
        dt = self.to_date() 
        dt2 = dt + datetime.timedelta(numDays)
        return BzDate(dt2)        
        
    @classmethod
    def today(cls) -> 'BzDate':
        today = datetime.date.today()
        return BzDate(today)

#---------------------------------------------------------------------

class BzDateTime(str):
    """ the Bozen date-time class """
    
    def __new__(cls, s):
        #dpr("s=%r:%s", s, type(s))
        if isinstance(s, BzDate):
            dts = str(s) + "T00:00:00"
            return super().__new__(cls, dts)
        if isinstance(s, BzDateTime):
            return super().__new__(cls, str(s))
        elif isinstance(s, str):
            dtStr = convertToBzDataTimeStr(s)
            if dtStr:                 
                return super().__new__(cls, dtStr)
            else:   
                raise ValueError(errMsg)
        elif isinstance(s, datetime.datetime):
            s2 = "%04d-%02d-%02dT%02d:%02d:%02d" % (
                s.year, s.month, s.day,
                s.hour, s.minute, s.second)
            #dpr("s2=%r", s2)
            return super().__new__(cls, s2)
        elif isinstance(s, datetime.date):
            s2 = "%04d-%02d-%02dT00:00:00" % (s.year, s.month, s.day)
            #dpr("s2=%r", s2)
            return super().__new__(cls, s2)
        else:
            s = ""
        
            
    def __repr__(self) -> str:
        r = "BzDateTime(%r)" % (str(self),)
        return r
    
    def toTuple_ymd(self) -> Tuple[int,int,int]:
        """ to tuple of (year, month, day) """
        y = butil.exValue(lambda: int(self[0:4]), 2000)
        mon = butil.exValue(lambda: int(self[5:7]), 1)
        day = butil.exValue(lambda: int(self[8:10]), 1)
        return (y, mon, day)
    
    def toTuple_ymdhms(self) -> Tuple[int,int,int,int,int,int]:
        """ to tuple of (year, month, day, hour, minute, second) """
        y = butil.exValue(lambda: int(self[0:4]), 2000)
        mon = butil.exValue(lambda: int(self[5:7]), 1)
        day = butil.exValue(lambda: int(self[8:10]), 1)
        day = butil.exValue(lambda: int(self[8:10]), 1)
        hh = butil.exValue(lambda: int(self[11:13]), 0)
        mm = butil.exValue(lambda: int(self[14:16]), 0)
        ss = butil.exValue(lambda: int(self[17:19]), 0)
        return (y, mon, day, hh, mm, ss)
    
    def to_date(self) -> datetime.date:
        """ convert to datetime.date """
        y, m, d = self.toTuple_ymd()
        return datetime.date(y, m, d)
        
    def to_datetime(self) -> datetime.datetime:
        """ convert to datetime.datetime """
        y, m, d, hh, mm, ss = self.toTuple_ymdhms()
        return datetime.datetime(y, m, d, hh, mm, ss)
    
    def formatDateTime(self, formatStr: str) -> str:
        """ format a BzDateTime according to the format string conventions
        in strftime(). See 
        <https://docs.python.org/3.6/library/datetime.html#strftime-strptime-behavior>
        """
        dt = self.to_datetime()
        s = dt.strftime(formatStr)
        return s
    
    def addDays(self, numDays: int) -> 'BzDateTime':
        """ add days to a BzDateTime """
        dpr("self=%r numDays=%r", self, numDays)
        dt = self.to_datetime() 
        dpr("dt=%r", dt)
        dt2 = dt + datetime.timedelta(numDays) 
        dpr("dt2=%r", dt2)
        bzdt2 = BzDateTime(dt2)  
        dpr("bzdt2=%r", bzdt2)
        return bzdt2
    
    def addDaysSeconds(self, numDays: int, numSeconds: int) -> 'BzDateTime':
        """ add days and seconds to a BzDateTime """
        dt = self.to_datetime() 
        dt2 = dt + datetime.timedelta(numDays, numSeconds)
        return BzDateTime(dt2)        
        
    @classmethod
    def now(cls) -> 'BzDateTime':
        now = datetime.datetime.now()
        return BzDateTime(now)
    

#---------------------------------------------------------------------
# helper functions 

def convertToBzDataTimeStr(s: str) -> str:
    """ Convert a string to the BZDateTime format, which is:
    yyyy-mm-ddTHH:MM:SS e.g. "2017-11-28T13:45:07"
    If cannot convert it, return "".
    Valid input types are:
    
    * "2017-11-28" (date only)
    * The above followed by any of:
      "13:45" (hour:minute)
      "13:45:07" (hour:minute:second)
    
    * "20171128" (date only)
    * the above with trailing numbers for time, e.g.:
      "2017112813"
      "201711281345"
      "20171128134507"    
    """
    s = s.strip()
    if isValidDate8(s[:8]):
        return decodeDateTime8(s)
    elif isValidDate(s[:10]):
        return decodeDateTime(s)
    return "" # can't convert it

def decodeDateTime8(s: str) -> str:
    """ Convert a string to the BZDateTime format, which is:
    yyyy-mm-ddTHH:MM:SS e.g. "2017-11-28T13:45:07"

    From:
    * "20171128" (date only)
    * the above with trailing numbers for time, e.g.:
      "2017112813"
      "201711281345"
      "20171128134507" 
    """
    y = butil.exValue(lambda: int(s[0:4]), 2000)
    mon = butil.exValue(lambda: int(s[4:6]), 1)
    day = butil.exValue(lambda: int(s[6:8]), 1)
    hh = butil.exValue(lambda: int(s[8:10]), 0)
    mm = butil.exValue(lambda: int(s[10:12]), 0)
    ss = butil.exValue(lambda: int(s[12:14]), 0)
    r = "%04d-%02d-%02dT%02d:%02d:%02d" % (
        y, mon, day,
        hh, mm, ss)
    return r
    
def decodeDateTime(s: str) -> str:
    """ Convert a string to the BZDateTime format, which is:
    yyyy-mm-ddTHH:MM:SS e.g. "2017-11-28T13:45:07", from:
    
    * "2017-11-28" (date only)
    * The above followed by any of:
      "13:45" (hour:minute)
      "13:45:07" (hour:minute:second)
    """  
    dateStr = s[:10]
    hh, mm, ss = get3ints(s[10:])
    s2 = dateStr + "T%02d:%02d:%02d" % (hh, mm, ss)
    return s2

def get3ints(s: str) -> Tuple[int,int,int]:
    """ get 3 integers from a string. if there aren't any,
    return 0s for the ones there aren't
    """
    i1, s1 = getPosInt(s, 0)
    i2, s2 = getPosInt(s1, 0)
    i3, _ = getPosInt(s2, 0)
    return (i1, i2, i3)

def getPosInt(s: int, default:int = 0) -> Tuple[int,str]:
    """ Get a positive integer from the start of a string,
    If there isn't one, return (default).
    Return the remnants of ther string after the integer
    in a tuple.
    """
    while 1:
        if s=="": return (default, "")
        if s[0].isdigit(): break
        s = s[1:]
    #//while
    
    sci = "" # string containing int
    while 1:
        if s=="": break
        if s[0].isdigit():
            sci += s[0]
            s = s[1:]
        else:    
            break
    #//while
    
    i = int(sci)
    return (i, s)
    

#---------------------------------------------------------------------

""" The default format for a date to look like in a from field,
e.g. 2017-Dec-31
"""
DEFAULT_DATE_SCREEN_FORMAT = "%Y-%b-%d"

class DateField(FieldInfo):
    """ a field that contains a date """

    def readArgs(self, **kwargs):
        super().readArgs(**kwargs)
        self.fieldLen = kwargs.get('fieldLen', 13)
        self.dateFormat = kwargs.get('dateFormat', 
            DEFAULT_DATE_SCREEN_FORMAT)
        self.required = kwargs.get('required', False)

    def defaultDefault(self):
        return ""

    #========== output to form ==========

    def formField_rw(self, v, **kwargs) -> str:
        """
        Create a form field (an <input> tag).

        :param v: this is the value of the field in the FormDoc
        :param kwargs: these arguments may include
            - readOnly :: bool (default False) = the form is read only
        :type kwargs: dict str:Any
        :return html containing the field
        :rtype str
        """
        vStr = self.convertToScreen(v)
        h = form("""<input{cc} id="id_{fn}"
            name="{fn}"
            type="text" value="{v}" size={fieldLen}>""",
            cc = cssClasses(
                "bz-input",
                "bz-DateField",
                self.monospaced and "monospace"),
            fn = self.fieldName,
            v = attrEsc(vStr),
            fieldLen = self.fieldLen)
        return h

    def formField_ro(self, v, **kwargs) -> str:
        vStr = self.convertToScreenH(v)
        if not vStr: vStr = "&nbsp;"
        h = form("""<span class='bz-read-only'>{}</span>""",
            vStr)
        return h

    #========== error message for field
    
    def errorMsg(self, v) -> str:
        if self.required and not v:
            return "This field is required."

    #========== conversion functions ==========

    def convertValue(self, vStr: str) -> Union[BzDate,str]:
        """ Convert a value coming back from an html form into a format
        correct for Python (either a BzDate or "")
        """
        dpr("vStr=%s", vStr)
        vStr = vStr.strip()
        if not vStr: return ""
    
        dtd = butil.exValue(
            lambda: datetime.datetime.strptime(vStr, self.dateFormat),
            None)
        dpr("dtd=%r", dtd)
        if dtd:
            bzd = BzDate(dtd)
            return bzd
        return ""

    def convertToScreen(self, v:Union[str,BzDate]) -> str:
        """ Convert the internal value in Python (v) to a readable
        value (i.e. a string or unicode that could de displayed in a form
        or elsewhere).
        """
        dpr("v=%r:%s", v, type(v))
        if not v: return ""
        if isinstance(v,BzDate):
            s = v.formatDate(self.dateFormat)
            return s
        else:
            raise ShouldntGetHere
             
    def convertFromDatabase(self, v: str) -> Union[str,BzDate]:
        """ Convert from a value got from the database to a value to go 
        into a Python object.
        """
        if not v: return ""
        try:
            bzd = BzDate(v)
        except ValueError:
            return ""
        else:
            return bzd
            
        
    def convertToDatabase(self, v: Union[str,BzDate]) -> str:
        """ Convert from an internal Python value to a value to go into 
        the database.
        """
        if not v: return ""
        return str(v)

#---------------------------------------------------------------------

""" The default format for a date to look like in a from field,
e.g. 2017-Dec-31 17:04
"""
DEFAULT_DATETIME_SCREEN_FORMAT = "%Y-%b-%d %H:%M"

class DateTimeField(FieldInfo):
    """ a field that contains a date and a time """

    def readArgs(self, **kwargs):
        super().readArgs(**kwargs)
        self.fieldLen = kwargs.get('fieldLen', 20)
        self.dateTimeFormat = kwargs.get('dateTimeFormat', 
            DEFAULT_DATETIME_SCREEN_FORMAT)
        self.required = kwargs.get('required', False)

    def defaultDefault(self):
        return ""

    #========== output to form ==========

    def formField_rw(self, v, **kwargs) -> str:
        """
        Create a form field (an <input> tag).

        :param v: this is the value of the field in the FormDoc
        :param kwargs: these arguments may include
            - readOnly :: bool (default False) = the form is read only
        :type kwargs: dict str:Any
        :return html containing the field
        :rtype str
        """
        vStr = self.convertToScreen(v)
        h = form("""<input{cc} id="id_{fn}"
            name="{fn}"
            type="text" value="{v}" size={fieldLen}>""",
            cc = cssClasses(
                "bz-input",
                "bz-DateTimeField",
                self.monospaced and "monospace"),
            fn = self.fieldName,
            v = attrEsc(vStr),
            fieldLen = self.fieldLen)
        return h

    def formField_ro(self, v, **kwargs) -> str:
        vStr = self.convertToScreenH(v)
        if not vStr: vStr = "&nbsp;"
        h = form("""<span class='bz-read-only'>{}</span>""",
            vStr)
        return h

    #========== error message for field
    
    def errorMsg(self, v) -> str:
        if self.required and not v:
            return "This field is required."

    #========== conversion functions ==========

    def convertValue(self, vStr: str) -> Union[BzDateTime,str]:
        """ Convert a value coming back from an html form into a format
        correct for Python (either a BzDate or "")
        """
        dpr("vStr=%s", vStr)
        vStr = vStr.strip()
        if not vStr: return ""
    
        pydt = butil.exValue(
            lambda: datetime.datetime.strptime(vStr, self.dateTimeFormat),
            None)
        dpr("pydt=%r", pydt)
        if pydt:
            bzdt = BzDateTime(pydt)
            return bzdt
        return ""

    def convertToScreen(self, v:Union[str,BzDateTime]) -> str:
        """ Convert the internal value in Python (v) to a readable
        value (i.e. a string or unicode that could de displayed in a form
        or elsewhere).
        """
        dpr("python value '%s', v=%r:%s", self.fieldName, v, type(v))
        if not v: return ""
        if isinstance(v,BzDateTime):
            s = v.formatDateTime(self.dateTimeFormat)
            dpr("s=%r:%s", s, type(s))
            return s
        else:
            raise ShouldntgetHere
             
    def convertFromDatabase(self, v: str) -> Union[str,BzDateTime]:
        """ Convert from a value got from the database to a value to go 
        into a Python object.
        """
        if not v: return ""
        try:
            bzdt = BzDateTime(v)
        except ValueError:
            return ""
        else:
            return bzdt
            
        
    def convertToDatabase(self, v: Union[str,BzDateTime]) -> str:
        """ Convert from an internal Python value to a value to go into 
        the database.
        """
        if not v: return ""
        return str(v)

#---------------------------------------------------------------------

#end
