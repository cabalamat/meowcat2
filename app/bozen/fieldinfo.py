# fieldinfo.py = information about fields

import inspect
import os.path
import re
from typing import *

from . import butil
from .butil import *
from . import bozenutil

#import butil
#from butil import *
#import bozenutil

#---------------------------------------------------------------------
# utility functions


def titleize(fn: str)->str:
    """ Convert a field name into a title
    :param string fn: a field name
    :rtype string
    """
    if fn[-3:]=="_id" and len(fn)>3:
        # remove trailing _id
        fn = fn[:-3]
    fn = fn[:1].capitalize() + fn[1:]
    r = ""
    insideNumber = False
    for ch in fn:
        if ch.isupper() or (ch.isdigit() != insideNumber):
            r += " "
        r += ch
        insideNumber = ch.isdigit()
    return r.strip()



""" For discussion of valid CSS class names, see:
https://stackoverflow.com/questions/448981/which-characters-are-valid-in-css-class-names-selectors
"""
validCssClassName = re.compile("-?[_a-zA-Z]+[_a-zA-Z0-9-]*")

def cssClasses(*args) -> str:
    """ Utility function for producing HTML containing the CSS classes
    of an HTML element. Examples:
    
    cssClasses() => ''
    cssClasses('') => ''
    cssClasses('foo','bar') => ' class="foo bar"'
    cssClasses(['foo','bar']) => ' class="foo bar"'
    cssClasses('foo',False,'bar') => ' class="foo bar"'
    cssClasses('foo','','bar') => ' class="foo bar"'
    cssClasses('foo',True and 'monospace') => ' class="foo monospace"'
    cssClasses('bar',False and 'monospace') =. ' class="bar"'
    
    (args) is 0 or more arguments, each of which is either a list or
    an atom, where an atom is either a sting or something with a 
    truth-value of False.
    
    cssClasses collects all the non-False atoms; these are CSS class names.
    It returns a string containing all the CSS classes. If there are none, 
    it returns ''.
    
    The function does not permit invalid CSS class names.
    """
    atoms = []
    for arg in args:
        if isinstance(arg, list):
            atoms += arg
        else:
            atoms.append(arg)
    goodAtoms = [a for a in atoms 
                   if a and isinstance(a, str)
                      and validCssClassName.fullmatch(a)]
    if len(goodAtoms)<1: return ""
    h = ' class="' + " ".join(goodAtoms) + '"'
    return h

def possibleAttr(attrName:str, attrValue:Optional[str])->str:
    """ If an attribute is not None, include it in the html for an
    element.
    :param str attrName: the attribute name
    :param attrValue: the value of the attribute
    :return a string possibly containing an attribute name and value
    :rtype str
    """
    if attrValue is None: return ""
    h = form("{attrName}='{attrValue}'",
        attrName = attrName,
        attrValue = attrValue)
    return h

#---------------------------------------------------------------------
"""
Things a field index (fi) must do:

fi.formField() = return a form field

fi.errorMsg() = return an error message (or "" if no errors)

fi.convertValue(fv) = convert from a form-value into a value that can be
    stored in a database field.
    
fi.convertToScreen(dbv)->str = convert from a py-value into a string

fi.convertToScreenH(dbv)->str = convert from a py-value into an html
    marked up string

"""


fieldIndex = bozenutil.Incrementor()

class FieldInfo:
    """ superclass for Bozen fields """

    def __init__(self, **kwargs):
        self.index = fieldIndex()
        self.desc = ""
        self.readArgs(**kwargs)

        caller = inspect.stack()[1]
        pan = caller[1]
        self.definedFile = os.path.basename(pan)
        self.definedLine = caller[2]

        dpr("%s:{} [%r] create %s, kwargs=%r",
            self.definedFile, self.definedLine,
            self.index, str(self.__class__.__name__), kwargs)


    def __repr__(self)->str:
        r = "<%s %s>" % (self.__class__.__name__,
            butil.exValue(lambda: self.fieldName, "(name unknown)"))
        return r

    def createWithInitialValue(self):
        return self.defaultValue
    
    @classmethod
    def takesMultipleValues(cls) -> bool:
        """ Return true if this is the sort of field type that in the
        MultiDict that comes back from the form, it can have multiple
        values from the same key.
        Usually this is False. If it true for field types where the
        form displaces a series of check boxes, such as MultiChoiceField 
        and FKeys; in those classes this metrhod must be redefined.
        """
        return False

    #========== html output to form ==========

    def xxxformBox(self, v, **kwargs):
        return self.formField(v, **kwargs)

    def formField(self, v, **kwargs):
        """
        Create a form field (typically an <input> tag).
        This method will be over-ridden by most subclasses.

        :param v: this is the value of the field in the FormDoc
        :param kwargs: these arguments may include
            - readOnly :: bool (default False) = the form is read only
        :type kwargs: dict str:Any
        :return html containing the field
        :rtype str
        """
        readOnly = kwargs.get('readOnly', self.readOnly)
        if readOnly:
            return self.formField_ro(v, **kwargs)
        else:
            return self.formField_rw(v, **kwargs)

    def autocompleteAttr(self) -> str:
        """ html to be generated as an attribute in the field for 
        autocomplete. if autocomplete==False, this is:
            autocomplete='off'
        otherwise, an empty string.
        """
        if self.autocomplete:
            return ""
        else:
            return "autocomplete='off'"
        

    def formField_rw(self, v, **kwargs)->str:
        vStr = self.convertToScreen(v)
        h = form("""<input{cc} id="id_{fn}"
            name="{fn}"
            type="text" value="{v}" size={fieldLen} {ac}>""",
            cc = cssClasses("bz-input", self.monospaced and "monospace"),
            fn = self.fieldName,
            v = attrEsc(vStr),
            fieldLen = self.fieldLen,
            ac = self.autocompleteAttr())
        return h

    def formField_ro(self, v, **kwargs)->str:
        vStr = self.convertToScreenH(v)
        if vStr.strip() == "": vStr = "&nbsp;"
        h = form("<span{cc} id='id_{fn}'>{v}</span>",
            cc = cssClasses("bz-read-only",  self.monospaced and "monospace"),
            fn = self.fieldName,
            v = vStr,
        )
        return h


    #========== error message for field

    def errorMsg(self, v)->str:
        """ Calculate an error message for this field
        :param v: data for this field (in format as it goes in the
            database)
        :return an error message for this field,
            or "" if there are no errors
        """
        retVal = ""
        #pr("v=%r self.minValue=%r", v, self.minValue)
        if (self.minValue is not None) and v < self.minValue:
            retVal += "Value %s must be >=%s.\n" % (v, self.minValue)
        if (self.maxValue is not None) and v > self.maxValue:
            retVal += "Value %s must be <=%s.\n" % (v, self.maxValue)

        return retVal


    #========== subclasses should re-implement these ==========

    def readArgs(self, **kwargs):
        """ Reads the keyword arguments when the FieldInfo was created.
        Subclasses of FieldInfo may wish to call this using super and
        then add their own keyword arguments.
        """
        #pr("FieldInfo:readArgs kwargs=%r", kwargs)
        self.defaultValue = kwargs.get('default', self.defaultDefault())
        if 'desc' in kwargs:
            self.desc = kwargs['desc']
        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'columnTitle' in kwargs:
            self.columnTitle =  kwargs['columnTitle']

        self.fieldLen = kwargs.get("fieldLen", 20)
        self.formatStr = kwargs.get("formatStr", "{}")
        self.readOnly = kwargs.get('readOnly', False)
        self.autocomplete = kwargs.get('autocomplete', True)
        self.monospaced = kwargs.get('monospaced', False)
        self.minValue = kwargs.get('minValue', None)
        self.maxValue = kwargs.get('maxValue', None)
        self.displayInForm = kwargs.get('displayInForm', True)
        self.convertF = kwargs.get('convertF', None)

    def defaultDefault(self):
        """ return the default value for the default value of the
        object.
        """
        return None

    def convert(self, v: str):
        """ Convert a value from something got from a form to a value
        that can be stored in the database for that field. uses the
        (convertF) parameter if it is set, otherwise uses the FieldInfo
        subclass's convertValue() method
        The return type necessarily depends on what field type it is.
        """
        v2 = str(v)
        if self.convertF:
            return self.convertF(v2)
        else:
            return self.convertValue(v2)

    def convertValue(self, v: str):
        """ Convert a value from something got from a form to a value
        that can be stored in the database for that field.
        The return type necessarily depends on what field type it is.
        """
        raise ImplementedBySubclass

    def convertToScreenH(self, v) -> str:
        """ Convert the internal value in a document (v) to a screen
        value (i.e. a string that could de displayed in a form
        or elsewhere). 

        :param v: value in document
        """
        return htmlEsc(self.convertToScreen(v))


    def convertToScreen(self, v) -> str:
        """ Convert the internal value in the database (v) to a screen
        value (i.e. a string  that could de displayed in a form
        or elsewhere). This method is the opposite of the convertValue()
        method.
        @param v = value from database
        """
        s = self.formatStr.format(v)
        return s

    def convertFromDatabase(self, v):
        """ Convert from a value got from the database to a value to go 
        into a Python object. For most field types this will be the
        identity function (and therefore doesn't have to be overridden).
        """
        return v
        
    def convertToDatabase(self, v):
        """ Convert from an internal Python value to a value to go into 
        the database. For most field types this will be the
        identity function (and therefore doesn't have to be overridden).
        """
        return v

    #========== helper functions

    def setFieldName(self, fieldName: str) -> str:
        """
        This is called from formdoc.initialiseClass() to set the
        fieldName to be whatever the class variable name is in the
        class definition.
        Also sets the title and columnTitle.
        """
        dpr("setting field name to %r", fieldName)
        self.fieldName = fieldName
        if not hasattr(self, 'title'):
            self.title = titleize(self.fieldName)
        if not hasattr(self, 'columnTitle'):
            self.columnTitle = self.title

    def setDocClass(self, docClass: Type['FieldInfo']):
        """
        This is called from formdoc.initialiseClass() to set the
        docClass to the class for which this is a field.
        :param docClass: the class of this FieldInfo
        :type docClass: a subclass of FormDoc or MonDoc
        """
        self.docClass = docClass

    def classFieldName(self) -> str:
        """ Text giving the class and fieldname of the FieldInfo, e.g.
        "Customer.phoneNumber". May be useful for debugging.
        """
        return "%s.%s" % (self.docClass.__name__, self.fieldName)


#---------------------------------------------------------------------


class StrField(FieldInfo):
    """ a field holding a Python str """

    def readArgs(self, **kwargs):
        super().readArgs(**kwargs)
        self.minLength = kwargs.get('minLength', None)
        self.maxLength = kwargs.get('maxLength', None)
        self.charsAllowed = kwargs.get('charsAllowed', None)
        self.required = kwargs.get('required', False)


    def defaultDefault(self):
        """ return the default value for the default value of the
        object.
        """
        return ""

    def convertValue(self, v) -> str:
        return str(v)


    def errorMsg(self, v) -> str:
        if self.required and not v:
            return "This field is required."

        msg = "Value '{}' ".format(v)

        if self.minLength!=None and len(v)<self.minLength:
            msg += "must be at least %d characters long"%self.minLength
            return msg

        if self.maxLength!=None and len(v)>self.maxLength:
            msg += "must be no longer than %d characters"%self.maxLength
            return msg

        if self.charsAllowed!=None:
            for ch in v:
                if ch not in self.charsAllowed:
                    msg += ("may only contain chars in: %s"
                            % self.charsAllowed)
                    return msg

        return ""


#---------------------------------------------------------------------

class TextAreaField(StrField):
    """ a string field displayed using a textarea element """

    def readArgs(self, **kwargs):
        super().readArgs(**kwargs)
        self.rows = kwargs.get('rows', 2)
        self.cols = kwargs.get('cols', 30)
        self.wysiwyg = kwargs.get('wysiwyg', False)


    def formField_rw(self, v, **kwargs) -> str:
        """ return html for a form field for this fieldInfo """
        h = form('''<textarea{cc}
 id="id_{fieldName}" name="{fieldName}"
 {rows} {cols}
 >{v}</textarea>''',
            cc = cssClasses(
                "bz-input",
                self.monospaced and "monospace",
                self.wysiwyg and "wysiwyg"),
            fieldName = self.fieldName,
            rows = possibleAttr("rows", self.rows),
            cols = possibleAttr("cols", self.cols),
            v = htmlEsc(v),
        )
        return h

    def formField_ro(self, v, **kwargs) -> str:
        if self.monospaced:
            h2 = form("<pre{cc}>{v}</pre>",
                cc = cssClasses("bz-read-only", "monospace"),
                v = htmlEsc(v))      
            return h2
        else:    
            lines = [htmlEsc(line.strip()) for line in v.split("\n")]
            h = "<br>\n".join(lines)
            if h == "": h = "&nbsp;"
            h2 = form("<span{cc}>{h}</span>",
                cc = cssClasses("bz-read-only"),
                h = h)
            return h2

#---------------------------------------------------------------------


class PasswordField(StrField):
    """ a StrField that displays characters as "*"s, for security """

    def formField_rw(self, v: str, **kwargs) -> str:
        """ return  html for a form field for this fieldInfo """
        h = form('''<input{cc} id="id_{fieldName}" name="{fieldName}"
            type="password" value="{v}" size={fieldLen} {ac}>''',
            cc = cssClasses("bz-input"),
            fieldName = self.fieldName,
            v = attrEsc(self.formatStr.format(v)),
            fieldLen = self.fieldLen,
            ac = self.autocompleteAttr()
        )
        return h




#---------------------------------------------------------------------





#end
