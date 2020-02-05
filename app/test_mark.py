# test_mark.py = test <mark.py>

from typing import List, Tuple

from bozen.butil import *
from bozen import lintest

import mark

#---------------------------------------------------------------------

class T_mark(lintest.TestCase):  
    
    def checkTags(self, h: str, ts: List[str], tagsSB: List[str]):
        """ check that the tags returned in (h) and (ts) are
        what they should be (tagsSB).
        If not, raise an exception
        """
        ts2 = sorted(ts)
        tagsSB2 = sorted(tagsSB)
        self.assertSame(ts2, tagsSB2, 
            "tags in (ts) are what they should be")
        for t in tagsSB2:
            tagInHtml = "href='/tag/%s'" % (t,)
            self.assertTrue(tagInHtml in h, 
                "(h) contains link to tag '%s'" % (t,))
        #//for   
        
    def checkHeading(self, h: str, headText: str, headType: str):
        """ Check a heading.
        @param h = html returned from render function
        @param headText = the text of the heading e.g. "This is the title"
        @param headType = the html heading type e.g. "h2" 
        """
        hStrSB = ">%s</%s>" % (headText, headType)
        self.assertTrue(hStrSB in h,
            "(h) contains heading HTML %r" % (hStrSB,))
        
    
    def test_normal(self):
        s = "some text here"
        h, ts = mark.render(s)
        dpr("----- h: -----\n%s\n-----end", h)
        self.assertTrue("some text here" in h)
        self.checkTags(h, ts, [])
        
    def test_headings(self):
        s = """\
# should be h1 heading

## this is h2

### and h3
"""
        h, ts = mark.render(s)
        dpr("----- h: -----\n%s\n-----end", h)
        self.checkTags(h, ts, [])
        self.checkHeading(h, "should be h1 heading", "h1")
        self.checkHeading(h, "this is h2", "h2")
        self.checkHeading(h, "and h3", "h3")
        
    def test_tags(self):
        s = "some text #with #tags and #more #tags"
        h, ts = mark.render(s)
        dpr("----- h: -----\n%s\n-----end", h)
        self.checkTags(h, ts, ["more", "tags", "with"])
        
    def test_tagsAtStart(self):
        """ make sure a tag at the start of a line isn't confused 
        with a heading 
        """
        s = "#monster #cat"
        h, ts = mark.render(s)
        dpr("----- h: -----\n%s\n-----end", h)
        self.checkTags(h, ts, ["cat", "monster"])
        self.assertFalse("[" in h, "html doesn't contain '['")
        self.assertFalse("]" in h, "html doesn't contain ']'")
        
    def test_tagsUnderline(self):
        """ tags that replace a character with '_' """        
        s = """\
[#a monster]
#a_nother
#xxx-yyy
"""
        h, ts = mark.render(s)
        dpr("----- h: -----\n%s\n-----end", h)
        self.checkTags(h, ts, ["a_monster", "a_nother", "xxx_yyy"])
        
#---------------------------------------------------------------------
    
class T_normaliseTagWpn(lintest.TestCase):  
    
    def ntw(self, s: str, sb: str, comment=""):
        """ Chack that normaliseTagWan(s) == sb """
        r = mark.normaliseTagWpn(s)
        if not comment:
            comment = form("norm(%r)==%r ?", s, sb)
        self.assertSame(r, sb, comment)
    
    def test_capitalisation(self):
        self.ntw("putin", "putin")
        self.ntw("Putin", "putin")
        self.ntw("PUTIN", "putin")
        self.ntw("pUtIn", "putin")
        
    def test_cyrillic(self):
        self.ntw("Путин", "putin")
        
    def test_spaces(self):
        self.ntw("Vladimir Putin", "vladimir_putin")
        self.ntw(" Vladimir Putin ", "vladimir_putin")
        self.ntw(" Vladimir   Putin ", "vladimir_putin")
        self.ntw(" Vladimir _  Putin ", "vladimir_putin")
        
    def test_dots(self):
        self.ntw("Python 3.5", "python_3_5")
        self.ntw("** Python 3.5 **", "python_3_5")
       
#---------------------------------------------------------------------
    


group = lintest.TestGroup()
group.add(T_mark)
group.add(T_normaliseTagWpn)

if __name__=='__main__': group.run()

#end