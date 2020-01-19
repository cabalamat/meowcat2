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
def wiki_page(u, pn):
    wp = wikidb.getWikiPage(u, pn)
    
    tem = jinjaEnv.get_template("wikiPage.html")
    h = tem.render(
        userName = htmlEsc(u),
        pn = htmlEsc(pn),
        wp = wp,
        exists = bool(wp),
        canAlter = True,
        nav = wikiPageNav(u, pn),
    )
    return h  

class WikiForm(FormDoc):
    source = TextAreaField(title="Wiki Page",
        rows=8, cols=60,
        required=True,
        monospaced=True)


@app.route('/wikiEdit/<u>/<pn>', methods=['POST', 'GET'])
def wikiEdit(u, pn):
    wp = wikidb.getWikiPage(u, pn, create=True)
    wf = WikiForm(source=wp.source)
    if request.method=='POST':
        wf = wf.populateFromRequest(request) 
        wp.source = wf.source
        wp.save()
    #//if    
    
    tem = jinjaEnv.get_template("wikiEdit.html")
    h = tem.render(
        userName = htmlEsc(u),
        pn = htmlEsc(pn),
        wp = wp,
        wf = wf,
        exists = bool(wp),
        canAlter = True,
        nav = wikiPageNav(u, pn),
    )
    return h    
    

           
#---------------------------------------------------------------------
   
def wikiPageNav(u: str, pn: str) -> str:
    """ Return html for navigation for a wiki page """
    pageIconFa = "fa-home" if pn=="home" else "fa-file-text-o"
    pageIcon = form("<i class='fa {fa}'></i>", fa=pageIconFa)
    h = form("""<span class='nav-instance'>
        <i class='fa fa-bank'></i> {siteLocation}</span>
        <span class='nav-user'>
        <i class='fa fa-user'></i> {u}</span>
        </span>
        <span class='nav-wiki'>
        <i class='fa fa-database'></i> 
        {pageIcon} {pn}</span>      
        """,
        siteLocation = config.SITE_LOCATION,
        u = htmlEsc(u),
        pageIcon = pageIcon,
        pn = htmlEsc(pn))
    return h
 
 
#---------------------------------------------------------------------

#end
