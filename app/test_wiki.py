# test_wiki.py = test <wiki.py>

from bozen.butil import *
from bozen import lintest

import models
import wiki

#---------------------------------------------------------------------

class T_paths(lintest.TestCase):  
    
    def testDecompose(self, pn, fo, fi):
        """ test decomposePathName """
        folder, filename = wiki.decomposePathName(pn)
        dpr("decomposePathName(%r) => (%r,%r)", pn, folder, filename)
        self.assertSame(folder, fo, 
            "testing %r, folder should be %r" % (pn, fo))
        self.assertSame(filename, fi, 
            "testing %r, filename should be %r" % (pn, fi))
    
    
    def test_decomposePathName(self):
        self.testDecompose("", "", "")
        self.testDecompose("foo", "", "foo")
        self.testDecompose("foo/", "foo", "")
        self.testDecompose("foo/bar", "foo", "bar")
        self.testDecompose("foo/bar/", "foo/bar", "")
        self.testDecompose("foo/bar/baz", "foo/bar", "baz")
        
   
#---------------------------------------------------------------------


group = lintest.TestGroup()
group.add(T_paths)

if __name__=='__main__': group.run()


#end
