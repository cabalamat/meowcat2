# mark.py = interface to python markdown

import sys
import re
from typing import List, Tuple

import markdown
from markdown.extensions import extra, sane_lists, codehilite

from bozen.butil import dpr

#---------------------------------------------------------------------



markdownProcessor = markdown.Markdown(externsions=[
    extra, 
    codehilite.CodeHilite(guess_lang=False),
    sane_lists])

def md(s: str) -> str:
    """ Convert markdown to html

    Uses the Python Markdown library to do this.
    See: <http://packages.python.org/Markdown/>
    """
    markdownProcessor.reset()
    h = markdownProcessor.convert(s)
    return h

#---------------------------------------------------------------------

def render(s: str) -> Tuple[str, List[str]]:
    """ Render markup into HTML als o return tags
    @return (h,tags) where:
       h:str = rendered html
       tags:List[str] = canonicalised hashtags
    """
    md = markdown.Markdown()
    h = md.convert(encloseHashtagAtStart(s))
    newHtml, tags = GetHashtags(h).calc()
    return (newHtml, tags)


hashtagAtStartRe = re.compile(r"^#([A-Za-z0-9_-]+)", re.MULTILINE)

def encloseHashtagAtStart(s: str) -> str:
    """ If a line starts with a hashtag, enclose it in [...], so that
    markdown does not treat it as a header
    @param smu [str] = sdhout markup
    @return [str]
    """
    s2 = hashtagAtStartRe.sub(r"[#\1]", s)
    return s2

#---------------------------------------------------------------------

hashtagRe = re.compile(r"\[#[ A-Za-z0-9_-]+\]|#[A-Za-z0-9_-]+")

class GetHashtags:

    def __init__(self, html: str):
        """
        @param html [unicode] some html
        """
        self.html = html
        self.tags = []

    def calc(self) -> Tuple[str, List[str]]:
        """ Put correct html around tag, return a list of them
        @return [str, list of str] = html string,
           followed by a list of tags
        """
        #print "calc() html=%r" % (self.html,)

        newHtml = hashtagRe.sub(self.substFun, self.html)
        return (newHtml, self.tags)

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
        canonicalTag = hashtag.lower().replace(" ", "_")
        self.tags.append(canonicalTag)
        result = "<a class='tag' href='/tag/%s'>#%s</a>" % (canonicalTag,
            hashtag)
        return result

#---------------------------------------------------------------------



#end
