# objectfield.py = the ObjectField class

from .butil import *
from . import fieldinfo

#---------------------------------------------------------------------

class ObjectField(fieldinfo.FieldInfo):
    """ a read-only field holding a Python object, which will be
    something representable as JSON, i.e. list, dict, int, str, float,
    bool, None.
    """

    def defaultDefault(self):
        """ return the default value for the default value of the
        object.
        """
        return None

    def convertToScreen(self, v):
        """ Convert the internal value in the database (v) to a readable
        value (i.e. a string or unicode that could de displayed in a form
        or elsewhere). This method is the opposite of the convertValue()
        method.

        :param v: value from database
        :rtype str or unicode
        """
        s = pretty(v, 2)
        return s

    def formField_rw(self, v, **kwargs):
        return self.formField_ro(v, **kwargs)

    def formField_ro(self, v, **kwargs) -> str:
        h2 = form("<pre{cc}>{h}</pre>",
            cc = fieldinfo.cssClasses("bz-read-only"),
            h = self.convertToScreenH(v)
        )    
        return h2

#---------------------------------------------------------------------


#end
