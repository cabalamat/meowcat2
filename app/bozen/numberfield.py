# numberfield.py = numeric fields

"""
<numberfield.py> contains fields (FieldInfo subclasses)
for date and time. These are:

- IntField
- FloatField
- BoolField

"""


from .butil import *

from . import fieldinfo

#---------------------------------------------------------------------

class IntField(fieldinfo.FieldInfo):
    """ a field holding a Python int """


    def defaultDefault(self):
        """ return the default value for the default value of the
        object.
        """
        return 0

    def convertValue(self, v):
        try:
            i = int(v)
        except:
            i = self.defaultValue
        return i

#---------------------------------------------------------------------

class FloatField(fieldinfo.FieldInfo):
    """ a field holding a Python float.

    Note that if you want fixed-point output then setting:

        formatStr="{:.2f}"

    gives you fixed point, 2 digits after the decimal point.
    """


    def defaultDefault(self):
        """ return the default value for the default value of the
        object.
        """
        return 0.0

    def convertValue(self, v):
        try:
            f = float(v)
        except:
            f = self.defaultValue
        return f

#---------------------------------------------------------------------

class BoolField(fieldinfo.FieldInfo):
    """ a field holding a Python bool """

    def defaultDefault(self):
        """ return the default value for the default value of the
        object.
        """
        return False

    def convertValue(self, v):
        return bool(v)

    def convertToScreen(self, v):
        s = "yes" if v else "no"
        return s

    def formField_rw(self, v, **kwargs):
        """ return  html for a form field for this fieldInfo, read-write
        """
        checked = ""
        if v: checked = " checked"
        h = form('''<input id="id_{fieldName}" type="checkbox"
            name="{fieldName}"{checked}>''',
            fieldName = self.fieldName,
            checked = checked,
        )
        return h



#---------------------------------------------------------------------



#end
