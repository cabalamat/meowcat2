# mark.py = interface to python markdown

import sys

import markdown
from markdown.extensions import extra, sane_lists, codehilite

#---------------------------------------------------------------------

extra


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


#end
