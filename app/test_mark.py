# test_mark.py = test <mark.py>


from bozen.butil import *
from bozen import lintest

import mark


#---------------------------------------------------------------------

class T_mark(lintest.TestCase):  
    
    def test_normal(self):
        s = "some text here"
        h, ts = mark.renderWithTags(s)
        dpr("----- h:\n%s\n-----end", h)
        self.assertTrue("some text here" in h)
        self.assertSame(ts, [], "no tags")
        
    def test_tags(self):
        s = "some text #with #tags and #more #tags"
        h, ts = mark.renderWithTags(s)
        dpr("----- h:\n%s\n-----end", h)
        dpr("ts=%r", ts)
        #self.assertTrue("some text here" in h)
        self.assertSame(len(ts), 3, "3 tags")
        self.assertBool("with" in ts, "'with' tag")
        self.assertBool("tags" in ts, "'tags' tag")
        self.assertBool("more" in ts, "'more' tag")

    
#---------------------------------------------------------------------


group = lintest.TestGroup()
group.add(T_mark)

if __name__=='__main__': group.run()

#end