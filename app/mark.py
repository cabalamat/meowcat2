# mark.py = interface to python markdown

import sys
import re
from typing import List, Tuple

import markdown
from markdown.extensions import extra, sane_lists, codehilite, toc
from markdown.extensions.toc import TocExtension

from bozen.butil import dpr

#---------------------------------------------------------------------
'''
markdownProcessor = markdown.Markdown(extensions=[
    extra, 
    toc,
    codehilite.CodeHilite(guess_lang=False),
    sane_lists])
'''
markdownProcessor = markdown.Markdown(extensions=[
    'extra',
    'toc', 
    'sane_lists',
    'codehilite',
    ])

def render(s: str) -> Tuple[str, List[str]]:
    """ Render markup into HTML also return tags
    (this version doesn't process tags)
    @return (h,tags) where:
       h:str = rendered html
       tags:List[str] = canonicalised hashtags
    """
    markdownProcessor.reset()
    h = markdownProcessor.convert(s)
    return (h, [])

def renderWithTags(s: str) -> Tuple[str, List[str]]:
    """ Render markup into HTML als o return tags
    @return (h,tags) where:
       h:str = rendered html
       tags:List[str] = canonicalised hashtags
    """
    markdownProcessor.reset()
    h = markdownProcessor.convert(encloseHashtagAtStart(s))
    newHtml, tags = GetHashtags(h).calc()
    return (newHtml, tags)


hashtagAtStartRe = re.compile(r"^#([A-Za-z0-9_-]+)", re.MULTILINE)

def encloseHashtagAtStart(s: str) -> str:
    """ If a line starts with a hashtag, enclose it in [...], so that
    markdown does not treat it as a header
    @param s = marked-up message
    """
    s2 = hashtagAtStartRe.sub(r"[#\1]", s)
    return s2

#---------------------------------------------------------------------

hashtagRe = re.compile(r"#[A-Za-z0-9_-]+")
#hashtagRe = re.compile(r"\[#[ A-Za-z0-9_-]+\]|#[A-Za-z0-9_-]+")

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
        canonicalTag = hashtag.lower().replace("-", "_")
        dpr("canonicalTag=%r", canonicalTag)
        self.tagSet.add(canonicalTag)
        dpr("self.tagSet=%r", self.tagSet)
        result = "<a class='tag' href='/tag/%s'>#%s</a>" % (canonicalTag,
            hashtag)
        return result

#---------------------------------------------------------------------



#end
