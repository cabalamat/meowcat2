# mark.py = interface to python markdown

import sys
import re
from typing import List, Tuple

import markdown
from markdown.extensions import extra, sane_lists, codehilite, toc
from markdown.extensions.toc import TocExtension
from markdown.extensions.wikilinks import WikiLinkExtension

from unidecode import unidecode

from bozen.butil import dpr

#---------------------------------------------------------------------

markdownProcessor = markdown.Markdown(extensions=[
    'extra',
    'toc', 
    'sane_lists',
    'codehilite',
])

markdownWikiProcessor = markdown.Markdown(extensions=[
    'extra',
    'toc', 
    'sane_lists',
    'codehilite',
    WikiLinkExtension(base_url="", end_url=""),
])

def render(s: str, wikiExt:bool=False) -> Tuple[str, List[str]]:
    """ Render markup into HTML, also return tags
    @param wiki = True if it should be rendered with the WikiLinkExtension
    @return (h,tags) where:
       h:str = rendered html
       tags:List[str] = canonicalised hashtags
    """
    s2 = encloseHashtagAtStart(s)
    s3, tags = GetHashtags(s2).calc()
    dpr("s3=%s", s3)
    if wikiExt:
        markdownWikiProcessor.reset()
        h = markdownWikiProcessor.convert(s3)
    else:
        markdownProcessor.reset()
        h = markdownProcessor.convert(s3)
    dpr("h=%s", h)
    return (h, tags)

hashtagAtStartRe = re.compile(r"^#([A-Za-z0-9_-]+)", re.MULTILINE)

def encloseHashtagAtStart(s: str) -> str:
    """ If a line starts with a hashtag, enclose it in [...], so that
    markdown does not treat it as a header
    @param s = marked-up message
    """
    s2 = hashtagAtStartRe.sub(r"[#\1]", s)
    return s2

#---------------------------------------------------------------------

#hashtagRe = re.compile(r"#[A-Za-z0-9_-]+")
#hashtagRe = re.compile(r"\[#[ A-Za-z0-9_-]+\]|#[A-Za-z0-9_-]+")

# For Unicode words:
hashtagRe = re.compile(r"\[#[ \w-]+\]|#[\w-]+")

class GetHashtags:

    def __init__(self, html: str):
        """
        @param html [unicode] some html
        """
        self.html = html
        self.tagSet = set()

    def calc(self) -> Tuple[str, List[str]]:
        """ Put correct html around tag, return a list of them
        @return [str, list of str] = html string,
           followed by a list of tags
        """
        #print "calc() html=%r" % (self.html,)

        newHtml = hashtagRe.sub(self.substFun, self.html)
        return (newHtml, list(self.tagSet))

    def substFun(self, mo) -> str:
        """ Substitution function
        """
        dpr("substFun() mo.groups()=%r start=%r end=%r",
            mo.groups(), mo.start(), mo.end())
        matchedText = mo.string[mo.start():mo.end()]
        if matchedText[:2]=="[#":
            hashtag = matchedText[2:-1]
        else:
            hashtag = matchedText[1:]
        dpr("matchedText=%r hashtag=%r", matchedText, hashtag)
        canonicalTag = hashtag.lower().replace("-", "_").replace(" ", "_")
        dpr("canonicalTag=%r", canonicalTag)
        self.tagSet.add(canonicalTag)
        dpr("self.tagSet=%r", self.tagSet)
        result = "<a class='tag' href='/tag/%s'>#%s</a>" % (canonicalTag,
            hashtag)
        return result

#---------------------------------------------------------------------

def normaliseTagWan(s: str) -> str:
    """ Normalise a tag or wiki article name 
    @param s = an unnormalised tag/wan
    """
    s2 = unidecode(s) # ascii-ize
    s3 = s2.lower() # lower case
    
    s4 = ""
    lastCh = ""
    for ch in s3:
        if ch in "abcdefghijklmnopqrstuvwxyz0123456789":
            useCh = ch
        else:
            useCh = "_"
      
        if not (lastCh=="_" and useCh=="_"):
            s4 += useCh
        lastCh = useCh    
    #//for        
    
    s5 = s4.strip("_")
    return s5


#---------------------------------------------------------------------



#end
