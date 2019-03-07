# formdoc.py = FormDoc class, etc for bozen

import copy
import collections
from typing import *

from .butil import *
from . import bozenutil
from .bztypes import DbId, DisplayValue, DbValue, HtmlStr
from . import fieldinfo
from .fieldinfo import FieldInfo
from .numberfield import BoolField
from . import keychoicefield
from .keychoicefield import FK
from . import nulldoc

#from butil import *
#import bozenutil
#from fieldinfo import FieldInfo

#---------------------------------------------------------------------

class FormDocMeta(type):
    def __init__(cls, name, bases, dyct):
        dpr("!!!! in FormDocMeta init method !!!!")
        super().__init__(name, bases, dyct)
        cls.classInfo = Struct()
        initialiseClass(cls, dyct)
        
  
def initialiseClass(cls, dyct):
    """ Initialise a subclass of FormDoc
    :param class cls: the class we are initialising
    :param dict dict: a dictionary containing class variables
    """
    #dpr("cls=%r __name__=%r", cls, cls.__name__)
    cls.classInfo.fieldNameSet = set()
    cls.classInfo.fieldNameTuple = []
    #dpr("fieldNameTuple=%r", cls.classInfo.fieldNameTuple)
    for fieldName, fieldInfo in dyct.items():
        #dpr("fieldName=%r fieldInfo=%r", fieldName, fieldInfo)
        if not isinstance(fieldInfo, FieldInfo): continue
        fieldInfo.setFieldName(fieldName)
        fieldInfo.setDocClass(cls)
        #dpr("%s fieldName=%s",
        #    fieldInfo.__class__.__name__,
        #    fieldName)
        cls.classInfo.fieldNameSet.add(fieldName)
        cls.classInfo.fieldNameTuple.append(fieldName)
        #dpr("fieldNameTuple=%r", cls.classInfo.fieldNameTuple)
    #//for
    def keyFn(fieldName):
        return dyct[fieldName].index
    cls.classInfo.fieldNameTuple = tuple(
        sorted(cls.classInfo.fieldNameTuple,
               key= keyFn))
    checkForMissingIndex(cls, dyct)

def checkForMissingIndex(cls, dyct):
    #print "Checking class %s for duplicate fields..." % (cls.__name__,)
    indexes = [dyct[fieldName].index
               for fieldName in cls.classInfo.fieldNameTuple]
    if len(indexes)<2: return # array to small to check
    for at,fix in enumerate(indexes):
        fn = cls.classInfo.fieldNameTuple[at] #::str
        fi = dyct[fn] #::FieldInfo
        dpr("at={} fix={} fn=%s", at, fix, fn)
        if at>0:
            if prev+1 != fix:
                # found an error
                fn = cls.classInfo.fieldNameTuple[at] #::str
                fi = dyct[fn] #::FieldInfo
                raise Exception(
                    "In class %s, duplicate field definition before %s,"
                    " at %s:%d"
                    % (cls.__name__, fn, fi.definedFile, fi.definedLine))
        prev = fix
    #//for      
        
        
#---------------------------------------------------------------------

class FormDoc(metaclass=FormDocMeta):
    """ an collection of fields, for use in an html form

    Instance variables:

    displayErrors (bool) = do we display errors on outputting this form
    """

    def __init__(self, **kwargs):
        """ Create a new FormDoc.
        :param dict kwargs: these arguments can be used to give initial
            values to the fields in the FormDoc
        """
        self.displayErrors = False
        self.populateFields()
        allowedFieldNames = self.allowedFieldNameSet()
        for k, v in kwargs.items():
            if k not in allowedFieldNames:
                raise NameError("'%s' is not a valid field name for %s"
                    % (k, self.__class__.__name__))
            self.__dict__[k] = v
            
 
    def allowedFieldNameSet(self)->Set[str]:
        """ Return allowed field names for this class
        """
        return self.classInfo.fieldNameSet           
        
    def populateFields(self):
        """ populate the fields defined in the subclass's definition.
        """
        classDict = dict(type(self).__dict__)
        for con, co in classDict.items():
            if isinstance(co, FieldInfo):
                self.__dict__[con] = co.createWithInitialValue()
        #//for
    

    def __repr__(self) -> str:
        """
        Show a string representation of me
        :rtype str
        """
        s = "<%s" % (self.__class__.__name__,)
        showFields = self.classInfo.fieldNameTuple[:5]
        dpr("showFields=%r", showFields)
        for fn in showFields:
            fv = self[fn]
            s += " %s=%r" % (fn, fv)
        #//for
        s += ">"
        return s
       
    #========== for joins ==========

    def __getattr__(self, fieldName: str):
        """ This is called when self.__dict__ doesn't have a
        key of (fieldName)
        """
        fnid = fieldName + "_id"
        dpr("fieldName=%r fnid=%r", fieldName, fnid)

        if fnid in self.__dict__:
            fi = self.getFieldInfo(fnid)
            #dpr("fi=%r", fi)
            if isinstance(fi, FK):
                #dpr("got it")
                fetchedDoc = fi.getDoc(self[fnid]) #new
                if not fetchedDoc:
                    fetchedDoc = nulldoc.NullDoc(fi.foreignTable)
                #dpr("fetchedDoc=%r", fetchedDoc)
                self.__dict__[fieldName] = fetchedDoc
                return fetchedDoc
            
        fnids = fieldName + "_ids"
        #dpr("fieldName=%r fnids=%r", fieldName, fnids)
        
        if fnids in self.__dict__:
            return self.getFKeysDereference(fnids)

        # not found, so fall over
        raise KeyError("'%s' not found" %(fieldName,))

    def getFKeysDereference(self, fnids: str) -> List['MonDoc']:
        """ fnids is something like xxxs_ids and we have to create
        an xxxs field containing a list of Xxx objects, and also
        return this value
        """
        fi = self.getFieldInfo(fnids)
        ids = self[fnids]
        targetColClass = fi.foreignTable
        result = []
        for id in ids:
            doc = targetColClass.getDoc(id)
            if doc:
                result.append(doc)
        #//for
        self[fnids[:-4]] = result
        return result
        

    #========== make it work like a dict ==========

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def keys(self):
        return self.__dict__.keys()

    def __iter__(self):
        for item in self.__dict__:
            yield item

    def __len__(self):
        return len(self.__dict__)

    def get(self, key, defaultValue=None):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return defaultValue
        
    def has_key(self, key):   
        return key in self.__dict__
    __contains__ = has_key
        
    #========== rendering an html form ==========

    def buildForm(self, **kwargs) -> HtmlStr:
        """ Build an html form containing all the fields in the FormDoc.
        Includes enclosing '<table>' tags.
        """
        h = form("<table class='bz-form-table'>{}</table>",
            self.buildFormLines(**kwargs))
        return h

    def buildFormLines(self, **kwargs) -> HtmlStr:
        """ Build an html form containing all the fields in the FormDoc.
        Doesn't include enclosing '<table>' tags.
        """
        h = ""
        for fieldName in self.classInfo.fieldNameTuple:
            fi = self.getFieldInfo(fieldName)
            if fi.displayInForm:
                h += self.formLine(fieldName, **kwargs)
        #//for
        return h

    def formLine(self, fn, **kwargs) -> HtmlStr:
        """ Build a line of an html form
        :param str fn: field name
        """
        errCssClass = ""
        errMsg2 = ""
        fi = self.getFieldInfo(fn)
        v = self[fn] # field value
        if self.displayErrors:
            errMsg = fi.errorMsg(v)
            if errMsg:
                errMsg2 = ("<br>\n<i class='fa fa-exclamation-triangle'></i> "
                    + errMsg)
                errCssClass = "bz-form-error-line"

        h = form("""<tr class='{fn}_line {errCssClass}'>
    <th class='bz-field-title'>
      <label for="id_{fn}" title="{desc}">{title}</label></th>
    <td>{ff} {errMsg2}</td>
</tr>""",
            fn = fn,
            desc = fi.desc,
            title = fi.title,
            ff = self.formField(fn, **kwargs),
            errCssClass = errCssClass,
            errMsg2 = errMsg2,
        )
        return h
    
    def formField(self, fn, **kwargs) -> HtmlStr:
        """ Build a field of an html form
        :param str fn: field name
        """
        fi = self.getFieldInfo(fn)
        v = self[fn] # value in the field
        #prvars("fn kwargs fi v")
        h = fi.formField(v, **kwargs)
        #pr("type(h)=%s", type(h))
        #prvars("h")
        return h

    #========== populate from request ==========
    # 26-Apr-2016 this will replace populateFromForm()

    def populateFromRequest(self, req, 
        populateBools:Union[str,List[str]]='all') -> 'FormDoc':
        """
        Creates a new FormDoc object similar to (self) with data from
        the form
        :param req: HTTP POST request
        :type req: flask request type
        :param populateBools: which boolean fields to populate. This
            is because of the way http POST requests work: they
            only return data for checkboxes clicked. So it's impossible
            to differentiate based on post request between checkbox not
            clicked and checkbox not in form.
        :type populateBools: 'all' | list of str
        :rtype FormDoc subclass
        """
        from .multichoicefield import MultiChoiceField, FKeys
        dpr("req=%r:%s", req, type(req))
        dpr("populateBools=%r:%s", populateBools, type(populateBools))

        reqForm = req.form
        dpr("reqForm=%r:%s", reqForm, type(reqForm))
        reqFiles = req.files
        #pr("reqFiles=%r::%s, len=%r", reqFiles, type(reqFiles), len(reqFiles))
        import filefield
        #formDict = mongo.toDict(formData)
        #newOb = copy.copy(self)
        newOb = self.makeCopy()
        #pr("self.__dict__=%r", self.__dict__)
        for fn in self.classInfo.fieldNameTuple:
            newOb.__dict__[fn] = self.__dict__[fn]
        #pr("copied __dict__, value is: %r",  newOb.__dict__)

        for k in reqForm.keys():
            #prvars("k")
            if self.hasFieldInfo(k):
                fi = self.getFieldInfo(k)
                #prvars("fi")
                if fi.takesMultipleValues():
                    listValues = reqForm.getlist(k)
                    #prvars("k listValues")
                    #newOb.setField(k, listValues)
                    newOb[k] = listValues
                else:
                    # most fields:
                    #prvars("k fi")
                    newOb.setField(k, reqForm[k])
        #//for k

        #>>>>> get bools to populate
        if populateBools=='all':
            boolsToPop = []
            for fn in self.classInfo.fieldNameTuple:
                fi = self.getFieldInfo(fn)
                if isinstance(fi, BoolField):
                    boolsToPop.append(fn)
            #//for fn
        else:
            boolsToPop = populateBools
        #prvars("populateBools boolsToPop")
        #pr("reqForm.keys()=%r", reqForm.keys())
        for boolFn in boolsToPop:
            #prvars("boolFn")
            if boolFn not in reqForm.keys():
                #pr("unsetting boolean field %s", boolFn)
                #newOb.setField(boolFn, False) # old code
                newOb[boolFn] = False # new code
                #pr("newOb['%s']=%r", boolFn, newOb[boolFn])
        #//for boolFn

        #>>>>> check reqFiles is there
        if len(reqFiles)==0 and False:
            for fn in self.classInfo.fieldNameTuple:
                fi = self.getFieldInfo(fn)
                if isinstance(fi, filefield.FileField):
                    msg = ("No files in request, but form contains "
                        "field %s (type %s), are you sure the "
                        "<form> tag includes enctype='multipart/form-data'?"
                        % (fi.fieldName, fi.__class__.__name__))
                    raise RuntimeError(msg)
            #//for
        #//if

        #>>>>> file upload has to be processed separately:
        for k in reqFiles.keys():
            if self.hasFieldInfo(k):
                fi = self.getFieldInfo(k)
                if isinstance(fi, filefield.FileField):
                    fileData = reqFiles[k]
                    #prvars("k fi fileData")
                    if fileData.filename:
                        savedAsPan = fi.uploadFile(fileData)
                        newOb[k] = savedAsPan
        #//for k
        return newOb

    def makeCopy(self) -> 'FormDoc':
        """ return a shallow copy of this object """
        newOb = self.__class__()
        newOb.__dict__ = dict(self.__dict__)
        return newOb

    def asReadableH(self, fn: str) -> str:
        """ Get a readable version of the field data, converted to  a 
        string, and then converted to html ready to go in a 
        web page.
        """
        fi = self.getFieldInfo(fn)
        v = self[fn]
        s = fi.convertToScreenH(v)
        return s


    def asReadable(self, fn: str) -> str:
        """ Get a readable form of the field data, converted to a 
        string.
        """
        fi = self.getFieldInfo(fn)
        v = self[fn]
        s = fi.convertToScreen(v)
        return s

    #========== validation ==========

    def isValid(self, fieldsToValidate:Union[List[str],None]=None) -> bool:
        """ Is a form valid?
        """
        if fieldsToValidate is None:
            fieldsToValidate = self.classInfo.fieldNameTuple
        
        for fn in fieldsToValidate:
            v = self[fn] # field value
            #prvars("fn v")
            fi = self.getFieldInfo(fn) #::FieldInfo
            em = fi.errorMsg(v)
            #prvars("em")
            if em:
                # got an error, form is invalid
                self.displayErrors = True
                return False
        #//for
        fwem = self.formWideErrorMessage()
        if fwem:
            self.displayErrors = True
            return False
        return True

    def formWideErrorMessageH(self) -> HtmlStr:
        """
        Wrap up a form wide error message in approprate HTML.
        :return an html-ized error message, or "" is there is none.
        :rtype str containing html
        """
        if not self.displayErrors:
            return ""
        fwem = self.formWideErrorMessage()
        if not fwem: return ""
        h = form("""<div class='bz-form-error-line'>
    <i class='fa fa-exclamation-triangle'></i> {}
</div>""", fwem)
        return h

    def formWideErrorMessage(self) -> str:
        """
        Return a form-wide error message. If there is form-wide
        validation to be done, this method should be over-ridden.
        :return an error message, or "" is there is none.
        :rtype str
        """
        return ""

    #========== utility functions ==========

    @classmethod
    def getFieldInfo(cls, fieldName: str) -> FieldInfo:
        """ Get the FieldInfo object for a field in a FormDoc subclass.
        """
        return cls.__dict__[fieldName]

    @classmethod
    def hasFieldInfo(cls, fieldName: str) -> bool:
        """ Does the class have a FieldInfo for a fieldName?
        """
        return fieldName in cls.__dict__

    @classmethod
    def fieldNames(cls) -> List[str]:
        """ Return this class's field names """
        return list(cls.classInfo.fieldNameTuple)

    def setField(self, fieldName: str, newValue: str):
        """
        Set a field with a string value (e.g. coming from a form).
        Convert the value to a different type if required.
        :param str fieldName: the field we are putting the value into
        :param str newValue: the new value
        """
        if self.hasFieldInfo(fieldName):
            fieldInfo = self.getFieldInfo(fieldName)
            convertedValue = fieldInfo.convert(newValue)
            #prvars("fieldName fieldInfo newValue convertedValue")
            self[fieldName] = convertedValue
        else:
            # not a defined field, fail
            #prvars("fieldName newValue")
            raise ShouldntGetHere
        
    @classmethod
    def classTitle(cls):
        return fieldinfo.titleize(cls.__name__)
    
    @classmethod
    def classTitlePlural(cls):
        ct = cls.classTitle()
        if ct[-1:] == "s":
            return ct + "es"
        else:
            return ct + "s"
        
        
#---------------------------------------------------------------------





#end
