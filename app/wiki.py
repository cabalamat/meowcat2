# wiki.py = pages for wikis

from typing import List, Tuple

from flask import request, redirect, Response

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime

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
        userName = u,
        pn = pn,
        wp = wp,
        exists = bool(wp),
        canAlter = True,
    )
    return h    
    

           
#---------------------------------------------------------------------
       
def wikiPage(u: str, folder: str, filename: str):
    """ return a wiki page. If it doesn't exist, return a placeholder.
    @param u = user name
    @param folder = the path to the page (not inculding filename)
    @param filename = the filename
    """
    wp = wikidb.getWikiPage(u, folder, filename)
    tem = jinjaEnv.get_template("wikiPage.html")
    canAlter = wikidb.canAlter(currentUserName(), u, folder, filename)
    h = tem.render(
        nav = wikiNavigation(u, folder, filename),
        userName = u,
        folder = folder,
        filename = filename,
        wp = wp,
        exists = bool(wp),
        canAlter = canAlter,
    )
    return h    
    
#---------------------------------------------------------------------

#end
