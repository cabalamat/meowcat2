# multichoicefield.py

from .butil import *
from . import fieldinfo

#---------------------------------------------------------------------

class MultiChoiceField(fieldinfo.FieldInfo):
    
    @classmethod
    def takesMultipleValues(cls) -> bool:
        return True

    def readArgs(self, **kwargs):
        super().readArgs(**kwargs)
        self.choices = kwargs.get('choices', [])
        self.separateLines = kwargs.get('separateLines', True)


    def defaultDefault(self):
        """ return the default value for the default value of the
        object.
        """
        return []

    def convert(self, v):
        """ Convert a value from something got from a form to a value
        that can be stored in the database for that field.
        :param: [str]
        :type v: [str]
        :rtype str
        """
        return v # may need changing later

    def convertValue(self, v):
        """ doesn't apply since MultiChoiceField is read-only """
        return None


    def formField_rw(self, v, **kwargs):
        ch = dict(self.choices)
        h = ""
        if self.separateLines:
            span = ""
            endSpan = ""
            br = "<br>"
        else:
            span = "<span class='mcf-keep-together'>"
            endSpan = "</span>"
            br = ""
        for dn, sn in self.choices:
            h += form("""{span}<input type="checkbox" id="id_{fn}_{value}"
                name="{fn}" value="{value}" {checked}>
                {showValue}{endSpan} {br}""",
                fn = self.fieldName,
                value = dn,
                checked = "checked" if (dn in v) else "",
                showValue = sn,
                span = span,
                endSpan = endSpan,
                br = br
            )
        #//for
        return h


    def formField_ro(self, v, **kwargs):
        h = "<span class='read-only'>"
        for dn, sn in self.choices:
            if dn in v:
                icon = "<i class='fa fa-check-square'></i>"
            else:
                icon = "<i class='fa fa-square'></i>"
            h += form("{icon} {showValue}<br>",
                icon = icon,
                showValue = sn)
        #//for
        h = h[:-4] # remove last "<br>"
        h += "</span>"
        return h


    def convertToScreen(self, v: List[str]) -> str:
        """ Convert the internal value in the database (v) to a readable
        value (i.e. a string that could de displayed in a form
        or elsewhere). This method is the opposite of the convertValue()
        method.
        """
        ch = dict(self.choices)
        s = ", ".join(ch.get(dn, dn) for dn in v)
        return s


#---------------------------------------------------------------------

class FKeys(fieldinfo.FieldInfo):
    """ a list of foreign keys to another MonDoc class
    Value of field is a list of ids.
    """

    def __init__(self, foreignTable, **kwargs):
        self._foreignTable = foreignTable
        self.index = fieldinfo.fieldIndex()
        self.desc = ""
        self.readArgs(**kwargs)

    @classmethod
    def takesMultipleValues(cls) -> bool:
        return True
    
    def readArgs(self, **kwargs):
        super().readArgs(**kwargs)

    def defaultDefault(self):
        return []

    def formField_rw(self, v, **kwargs) -> str:
        if not v: v = []
        docs = list(self.foreignTable.find())
        docs.sort(key=lambda doc: doc.getName())
        hs = []
        for doc in docs:
            checked = ""
            key = doc.id()
            if key in v: checked = " checked"
            hs.append(form("""<input type='checkbox' name='{fn}'
                value='{key}' {checked}> {text}""",
                fn = attrEsc(self.fieldName),
                key = attrEsc(key),
                checked = checked,
                text = htmlEsc(doc.getName())
            ))
        #//for key
        h = "<br>\n".join(hs)
        return h

    @printargs
    def formField_ro(self, v, **kwargs) -> str:
        """ Display a link to the relevant document """
        return self.convertToScreenH(v)

    def convertValue(self, v):
        """ Convert a value from something got from a form to a value
        that can be stored in the database for that field.
        The return type necessarily depends on what field type it is.
        :param string v:
        """
        dpr("FKeys.convertValue() v=%r:%s", v, type(v))
        return v

    def convertToScreenH(self, v: List[str]) -> str:
        """ Convert the internal value in python (v) to a readable
        value (i.e. a string that could de displayed in a form
        or elsewhere). 

        :param v: value from Python, list of keys
        """
        dpr("%s v=%r", self.classFieldName(), v)
        if not v or type(v)!=list: return ""
        h = ""
        for key in v:
            doc = self.foreignTable.getDoc(key)
            if doc:
                h += doc.a() + ", "
            else:
                h += form("<i>{}</i>, ", htmlEsc(key))
        #//for key
        h = h[:-2]
        return h

    def convertToScreen(self, v: List[str]) -> str:
        """ Convert the internal value in the database (v) to a readable
        value (i.e. a string that could de displayed in a form
        or elsewhere). 

        :param v: value from database, list of keys
        """
        h = ""
        for key in v:
            doc = self.foreignTable.getDoc(key)
            h += doc.getName() + ", "
        #//for key
        h = h[:-2]
        return h

    #==========

    @property
    def foreignTable(self) -> Type['MonDoc']:
        """
        Return the MonDoc subclass for the foreign table
        If (self._foreignTable) is a string, change it to a MonDoc
        subclass.
        """
        from . import mondoc
        if isinstance(self._foreignTable, str):
            dpr("Looking up MonDoc subclass for '%s'", self._foreignTable)
            mdsc = mondoc.monDocSubclassDict.get(self._foreignTable, None)
            if not mdsc:
                msg = ("In FK field %s.%s, "
                    "cannot find MonDoc subclass for '%s'" % (
                    self.docClass.__name__,
                    self.fieldName,
                    self._foreignTable,))
                raise KeyError(msg)
            else:
                pr("MonDoc subclass is %r", mdsc)
                self._foreignTable = mdsc
        #pr("self._foreignTable=%r", self._foreignTable)
        return self._foreignTable





#---------------------------------------------------------------------

#end
