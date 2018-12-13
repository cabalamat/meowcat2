# nulldoc.py = the NullDoc clsss


#---------------------------------------------------------------------
""" A NullDoc is used when dereferencing an FK field in a MonDoc and
there is no valid target.
"""

class NullDoc(object):

    def __init__(self, fakeClass):
        """ Create a NullDoc faking a (fakeClass).
        :param fakeClass:
        :type fakeClass: a MonDoc subclass
        """
        self.fakeClass = fakeClass

    def __repr__(self) -> str:
        s = "NullDoc(%s)" % (self.fakeClass.__name__)
        return s

    def a(self) -> str:
        return ""

    def __getattr__(self, fieldName: str):
        """ This is unfinished -- it should follow FK references
        by creating a NullDoc of the relevent target class

        :param string fieldName:
        """
        if fieldName in self.fakeClass.classInfo.fieldNameTuple:
            fi = self.fakeClass.getFieldInfo(fieldName)
            #prvars("fi")
            return fi.defaultDefault()
        else:
            tryFk = fieldName + "_id"
            if tryFk in self.fakeClass.classInfo.fieldNameTuple:
                fi = self.fakeClass.getFieldInfo(tryFk)
                if isinstance(fi, FK):
                    useMDSC = fi.foreignTable
                    return NullDoc(useMDSC)
                else:
                    return fi.defaultValue

        return ""

    def getName(self) -> str:
        return ""

    def asReadable(self, fn: str) -> str:
        return ""

    def asReadableH(self, fn: str) -> str:
        return ""

    def id(self) -> str:
        return ""


#---------------------------------------------------------------------

#end