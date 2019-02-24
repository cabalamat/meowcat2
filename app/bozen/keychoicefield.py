# keychoicefield.py = key and choice fields

from typing import *

from . import butil
from .butil import *
from .bztypes import *
from . import bozenutil

from .fieldinfo import fieldIndex, FieldInfo, StrField

#---------------------------------------------------------------------


class ChoiceField(StrField):
    """ A ChoiceField takes a choices argument of the form:
        choices=[('C', 'collection'),
                 ('D', 'delivery'),
                 ('N', 'none')]
    The 0th element of the tuple is the value of the field;
    the 1st is the displayed value. The default is the value of
    the initial tuple, unless a specific default is set.
    """

    def readArgs(self, **kwargs):
        super().readArgs(**kwargs)
        choices = kwargs.get('choices',
            (('N','No'),('Y','Yes'))
        )
        choices2 = []
        for ch in choices:
            if isinstance(ch,tuple):
                v = ch
            else:
                v = (ch,ch)
            choices2.append(v)
        #for
        self.choices = choices2
        if 'default' not in kwargs:
            self.defaultValue = self.choices[0][0]

        # if true, includes a null option on the form
        self.showNull = kwargs.get('showNull', False)
        if self.showNull:
            self.defaultValue = ''

        # if true, allow user to select the null option on the form
        self.allowNull = kwargs.get('allowNull', True)

    def formField_rw(self, v, **kwargs):
        """ return html for a form field for this fieldInfo
        @param v [ObjectId] the value in the field for the MonDoc
        @return [str] containing html
        """
        return renderChoices(self.fieldName, self.getChoices(v), v)

    def getChoices(self, v):
        """
        :param str v: the current value
        :rtype choices: [(dbValue::str, screenValue::str)]
        """
        choices = self.choices
        #prvars("v choices")
        if self.showNull:
            choices = [('',"- select one -")] + choices
        #prvars("choices")
        return choices

    def convertToScreen(self, v: str) -> str:
        for value, show in self.choices:
            if v==value:
                return show
        #//for
        return v


    def errorMsg(self, v: str) -> str:
        """
        :return an error message, or "" if there are no errors
        :rtype str
        """
        msg = ""
        if not self.allowNull and not v:
            msg += "You must select an option"
        return msg

#---------------------------------------------------------------------

class FK(FieldInfo):
    """ a foreign key to another MonDoc class """

    def __init__(self, foreignTable: Union['MonDoc',str], **kwargs):
        """
        A Foreign Key.
        @param foreignTable = the foreign table we're linking to.
            If this table isn't available (e.g. because who tables each
            have a foreign key to each other), use the name of the MonDoc
            subclass for the linked-to table.
        """
        self._foreignTable = foreignTable
        self.index = fieldIndex()
        self.desc = ""
        self.readArgs(**kwargs)

    def readArgs(self, **kwargs):
        super().readArgs(**kwargs)
        self.field = kwargs.get('field', None)

        # choice function, returns choices, similar to ChoiceField.
        self.choiceF = kwargs.get('choiceF', None)
        #pr("_foreignTable=%r choiceF=%r", self._foreignTable, self.choiceF)

        # if true, includes a null option on the form
        self.showNull = kwargs.get('showNull', False)

        # if true, allow user to select the null option on the form
        self.allowNull = kwargs.get('allowNull', True)

        # if true, display link to record pointed to
        self.showLink = kwargs.get('showLink', True)

    def formField_rw(self, v, **kwargs) -> str:
        h = ""
        if self.showLink:
            h += self.formField_ro(v, **kwargs) + "&nbsp;&nbsp;"
        choicesH = renderChoices(self.fieldName, self.getChoices(v), v)
        if choicesH:
            h += choicesH
        return h

    def formField_ro(self, v, **kwargs) -> str:
        return self.convertToScreenH(v, **kwargs)

    def convertToScreenH(self, v: DbId, **kwargs) -> str:
        """ Display a link to the relevant document """
        forDoc = self.foreignTable.getDoc(v)
        #prvars("self v kwargs forDoc")
        if not forDoc:
            if v:
                keyStr = form(", key=<tt>{}</tt>", htmlEsc(v))
            else:
                keyStr = ""
            h = form("<i>(none{keyStr})</i>", keyStr=keyStr)
            return h
        if 'adminStub' in kwargs:
            h = forDoc.adminA(adminStub=kwargs['adminStub'])
        else:
            #pr("getting forDoc.a() forDoc=%r", forDoc)
            h = forDoc.a()
            #pr("h=%r", h)
        return h

    def getChoices(self, v) -> List[Tuple[str,str]]:
        """ Return the list of choices for the select element """
        if self.choiceF:
            choices = self.choiceF(self)
        else:
            fDocs = list(self.foreignTable.find())
            fDocs.sort(key=lambda fDoc: fDoc.getName())
            choices = [(doc.id(),doc.getName())
                       for doc in fDocs]
        if (len(choices)==0
            or ((not v or self.showNull)
                and bool(choices[0][0]))):
            # add empty choice at start
            choices = [('',"- select one -")] + choices
        return choices


    def convertValue(self, v):
        """ Convert a value from something got from a form to a value
        that can be stored in the database for that field.
        The return type necessarily depends on what field type it is.
        """
        return v

    def errorMsg(self, v) -> str:
        """
        Return an error message, or "" if there are no errors
        """
        msg = ""
        if not self.allowNull and not v:
            msg += "You must select an option"
        return msg

    #========== get a document from a foreign key ===========

    def getDoc(self, fkValue) -> Optional['MonDoc']:
        """ a value of a foreign key, to be looked up """
        if self.field:
            q = {self.field: fkValue}
            #prvars("fkValue q")
            doc = self.foreignTable.find_one(q)
            #prvars("doc")
        else:
            doc = self.foreignTable.getDoc(fkValue)
        return doc

    #==========

    @property
    def foreignTable(self) -> 'MonDoc':
        """
        Return the MonDoc subclass for the foreign table
        If (self._foreignTable) is a string, change it to a MonDoc
        subclass.
        """
        from . import mondoc
        if isinstance(self._foreignTable, str):
            pr("Looking up MonDoc subclass for '%s'", self._foreignTable)
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
# convenience function for ChoiceField and FK

def renderChoices(fieldName, choices, chosen):
    """
    :param str fieldName: the field name
    :param choices: the chocies presented to the user
    :param choices: [(dbValue::str, screenValue::str)]
    :param chosen: the pre-selected choice (or None if none)
    :type chosen: str | None
    :return str containing an html <select> control
    :rtype str
    """

    h = form("<select id='id_{fieldName}' name='{fieldName}'>\n",
        fieldName = fieldName)
    for choiceVal, choiceStr in choices:
        selected = ""
        if chosen == choiceVal:
            selected = " selected='selected'"
        h += form("<option value='{cv}'{selected}>{cs}</option>\n",
            cv = choiceVal,
            cs = choiceStr,
            selected = selected)
    #//for
    h += "</select>\n"
    return h


#---------------------------------------------------------------------



#end
