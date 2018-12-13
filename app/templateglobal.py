# templateglobal.py

"""
Template globals 
"""

import random

from flask import Flask, request, redirect, session

from bozen.butil import form
from allpages import jinjaEnv

import config

#---------------------------------------------------------------------
"""
Simplifying twitter Bootstrap

Inside a template, to start a new row:

    {{rowcol("md-6")}}

Once we're in the row, a new column is:

    {{col("md-6")}}

To End the row:

    {{endrow()}}

"""

def rowcol(colSpec: str)->str:
    cs = "col-" + colSpec
    s = form("""<div class="container-fluid">
  <div class="row">
    <div class="{cs}">""",
        cs = cs)
    return s
jinjaEnv.globals['rowcol'] = rowcol
jinjaEnv.globals['rowCol'] = rowcol

def col(colSpec: str)->str:
    cs = "col-" + colSpec
    s = form("""
    </div>
    <div class="{cs}">""",
        cs = cs)
    return s
jinjaEnv.globals['col'] = col

def endrow()->str:
    s = """</div></div></div><!-- endrow -->"""
    return s
jinjaEnv.globals['endrow'] = endrow
jinjaEnv.globals['endRow'] = endrow

#---------------------------------------------------------------------
""" Section headings in form tables
    ===============================

    {{formSection("This is a title")}}

"""

def formSection(t: str)->str:
    """
    @param t::str containing html = text to go in title
    @return::str containing html
    """
    r = form("""<tr><td colspan=2 class='form-section'>
    <div>{}</div>
</td></tr>""",
        t)
    return r
jinjaEnv.globals['formSection'] = formSection

#---------------------------------------------------------------------
# about the app

jinjaEnv.globals['APP_LOGO'] = config.APP_LOGO
jinjaEnv.globals['APP_TITLE'] = config.APP_TITLE
jinjaEnv.globals['APP_NAME'] = config.APP_NAME
jinjaEnv.globals['DB_NAME'] = config.DB_NAME
jinjaEnv.globals['PORT'] = config.PORT

#---------------------------------------------------------------------

def helpPage():
    p = request.path[1:]
    r = p.split('/')[0]
    if r=="": r = "main"
    return r
jinjaEnv.globals['helpPage'] = helpPage

def highlightPageIfCurrent(testUrl, *moreUrls):
    """ If the current page starts with (testUrl), highlight it
    by returning the code " class='active'".
    Otherwise return ""
    """
    urls = [testUrl] + list(moreUrls)
    p = request.path.lstrip("/")
    for url in urls:
        if p.startswith(url):
            return " class='active'"
    return ""
jinjaEnv.globals['hpic'] = highlightPageIfCurrent

def highlightPageExact(testUrl, *moreUrls):
    """ If the current page before the first '/' is (testUrl),
    highlight it by returning the code " class='active'".
    Otherwise return ""
    """
    urls = [testUrl] + list(moreUrls)
    p = request.path.lstrip("/")
    p1 = p.split("/")[0]
    for url in urls:
        if p1==url:
            return " class='active'"
    return ""
jinjaEnv.globals['hpex'] = highlightPageExact

def completeH(b, yesText="complete", noText="not complete"):
    """ return a string saying whether something is complete
    @param b::bool
    @return::str containing html
    """
    tStr = """<span class='text-success'><i class='fa fa-check'></i>
        %s</span>""" % (yesText,)
    fStr = """<span class='text-danger'><i class='fa fa-times'></i>
        %s</span>""" % (noText,)
    if b:
        return tStr
    else:
        return fStr
jinjaEnv.globals['completeH'] = completeH

def yesNoH(b, yesText="yes", noText="no"):
    """ return a string saying whether something is complete
    @param b::bool
    @return::str containing html
    """
    return completeH(b, yesText, noText)
jinjaEnv.globals['yesNoH'] = yesNoH

def usingHelp():
    return False
jinjaEnv.globals['usingHelp'] = usingHelp

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(random.randint(1,1000000000))
    return session['_csrf_token']
jinjaEnv.globals['csrf_token'] = generate_csrf_token


#---------------------------------------------------------------------
# users

def currentUserName():
    return "(none)"
jinjaEnv.globals['currentUserName'] = currentUserName

def canView(page):
    return True
jinjaEnv.globals['canView'] = canView

#---------------------------------------------------------------------

#end
