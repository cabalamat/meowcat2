# wiki.py = pages for wikis

from typing import List, Tuple

from flask import request, redirect, Response

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import (StrField, ChoiceField, TextAreaField,
    IntField, FloatField, BoolField,
    MultiChoiceField, FK, FKeys,
    DateField, DateTimeField)

import config
from allpages import app, jinjaEnv
import mark
import ht
import userdb
import models
from permission import needUser, currentUserName
import wikidb

#---------------------------------------------------------------------

@app.route('/wiki/<u>')
@app.route('/wiki/<u>/')
def wiki_u(u):
    return wikiDir(u, "")
    
@app.route('/wiki/<u>/<pn>')
def wiki(u: str, pn: str):
    """ Display a wiki page
    @param u = user id
    @param pn = page name
    """
    npn = mark.normaliseTagWpn(pn) # normalised page name
    wp = wikidb.getWikiPage(u, npn)
    
    tem = jinjaEnv.get_template("wikiPage.html")
    h = tem.render(
        userName = htmlEsc(u),
        pn = htmlEsc(pn),
        wp = wp,
        exists = bool(wp),
        canAlter = True,
        nav = wikiPageNav(u, npn),
    )
    return h  

class WikiForm(FormDoc):
    source = TextAreaField(title="Wiki Page",
        rows=20, cols=70,
        required=True,
        monospaced=True)


@app.route('/wikiEdit/<u>/<pn>', methods=['POST', 'GET'])
def wikiEdit(u: str, pn: str):
    """ Edit a wiki page
    @param u = user id
    @param pn = page name
    """
    npn = mark.normaliseTagWpn(pn) # normalised page name
    wp = wikidb.getWikiPage(u, npn, create=True)
    wf = WikiForm(source=wp.source)
    if request.method=='POST':
        wf = wf.populateFromRequest(request) 
        wp.source = wf.source
        wp.save()
        return redirect(form("/wiki/{u}/{pn}", u=u, pn=pn))
    #//if    
    
    tem = jinjaEnv.get_template("wikiEdit.html")
    h = tem.render(
        userName = htmlEsc(u),
        pn = htmlEsc(pn),
        wp = wp,
        wf = wf,
        exists = bool(wp),
        canAlter = True,
        nav = wikiPageNav(u, npn),
    )
    return h    
            
#---------------------------------------------------------------------
     

@app.route('/wikiIndex/<u>')
def wikiIndex(u: str):
    """ display a list of all the pages in a wiki 
    @param u = user id
    """
    wps = wikidb.getWikiPages(u)
    wikiIndexH = ""
    for wp in wps:
        wikiIndexH += form("<br>{a}\n",
            a = wp.a())
    #//for    
    
    tem = jinjaEnv.get_template("wikiIndex.html")
    h = tem.render(
        userName = htmlEsc(u),
        nav = wikiNav(u),
        wikiIndexH = wikiIndexH,
    )
    return h    
                   
#---------------------------------------------------------------------
   
def wikiNav(u: str) -> str:
    """ Return html for navigation for a wiki """
    h = form("""<span class='nav-instance'>
        <i class='fa fa-bank'></i> {siteLocation}</span>
        <span class='nav-user'>
        <i class='fa fa-user'></i> {u}</span>
        </span>
        <span class='nav-wiki'>
        <i class='fa fa-database'></i> 
        </span>      
        """,
        siteLocation = config.SITE_LOCATION,
        u = htmlEsc(u))
    return h  

def wikiPageNav(u: str, npn: str) -> str:
    """ Return html for navigation for a wiki page """
    pageIconFa = "fa-home" if npn=="home" else "fa-file-text-o"
    pageIcon = form("<i class='fa {fa}'></i>", fa=pageIconFa)
    h = form("""<span class='nav-instance'>
        <i class='fa fa-bank'></i> {siteLocation}</span>
        <span class='nav-user'>
        <i class='fa fa-user'></i> {u}</span>
        <span class='nav-wiki'>
        <i class='fa fa-database'></i> 
        {pageIcon} {pn}</span>      
        """,
        siteLocation = config.SITE_LOCATION,
        u = htmlEsc(u),
        pageIcon = pageIcon,
        pn = htmlEsc(npn))
    return h
 
 
#---------------------------------------------------------------------

#end
