# test_wiki.py = test <wiki.py>

from bozen.butil import *
from bozen import lintest

import wiki

#---------------------------------------------------------------------

class T_paths(lintest.TestCase):  
    
    def test_decomposePathName(self):
        folder, filename = wiki.decomposePathName("foo/bar")
        self.assertSame(folder, "foo", "folder for 'foo/bar'")
        self.assertSame(filename, "bar", "filename for 'foo/bar'")
        
        folder, filename = wiki.decomposePathName("foo/bar/")
        self.assertSame(folder, "foo/bar", "folder for 'foo/bar/'")
        self.assertSame(filename, "", "filename for 'foo/bar/'")
        
        folder, filename = wiki.decomposePathName("foo/bar/baz")
        self.assertSame(folder, "foo/bar", "folder for 'foo/bar/baz'")
        self.assertSame(filename, "baz", "filename for 'foo/bar/baz'")
   
#---------------------------------------------------------------------


group = lintest.TestGroup()
group.add(T_paths)

if __name__=='__main__': group.run()


#end
