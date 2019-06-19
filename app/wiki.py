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
    
@app.route('/wiki/<u>/<path:pathName>')
def wiki_page(u, pathName):
    dpr("pathName=%r", pathName)
    folder, filename = decomposePathName(pathName)
    dpr("folder=%r filename=%r", folder, filename)
    if filename=="":
        return wikiDir(u, folder)
    else:    
        return wikiPage(u, folder, filename)
    
def decomposePathName(pathName: str) -> Tuple[str,str]:
    """ decompose a pathname into a folder and a filename, e.g.
        "foo/bar" -> ("foo", "bar")
        "foo/bar/" -> ("foo/bar", "")
        "foo/bar/baz" -> ("foo/bar", "baz")
    """
    parts = pathName.split("/")
    if len(parts)==1:
        return "", parts[0]
    
    folderA = parts[:-1]
    filename = parts[-1]
    folder = "/".join(folderA)
    return folder, filename
           
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
