# wikidb.py = database for the wiki

from typing import *

import bozen
from bozen.butil import *
from bozen import MonDoc, BzDateTime
from bozen import (StrField, ChoiceField, TextAreaField,
    IntField, FloatField, BoolField,
    MultiChoiceField, FK, FKeys, ObjectField,
    DateField, DateTimeField)

import userdb
import mark
import models

"""***
Wikis in MeowCat
================

Note on variable names:

pn: str = page name, a string such as "home" (for home page)

page: WikiPage = the contents of a page

***"""

#---------------------------------------------------------------------
# WikiPage table

class WikiPage(MonDoc):
    owner_id = FK('User', allowNull=False,
        desc="the owner of this wikipage")
    pageName = StrField(desc="page name")
    version = IntField(desc="version number")
    
    source = TextAreaField(monospaced=True, required=True)
    html = TextAreaField(monospaced=True, readOnly=True)
    published = DateTimeField(readOnly=True,
        dateTimeFormat=models.MESS_TIME_DISPLAY_FORMAT)

    @classmethod
    def classLogo(cls) -> str:
        return "<i class='fa fa-file-text-o'></i> "
    
    def logo(self) -> str:
        return ("<i class='fa fa-home'></i> " 
                if self.pageName=="home" 
                else "<i class='fa fa-file-text-o'></i> ")
    
    def url(self) -> str:
        theUrl = form("/wiki/{u}/{pn}",
            u = self.owner_id,
            pn = self.pageName)
        return theUrl
    
    def getName(self) -> str:
        return self.pageName
    
    def preCreate(self):
        self.published = BzDateTime.now()
        
    def preSave(self):
        """ before saving, render the source into html """
        self.html, _ = mark.render(self.source)
      

def getWikiPage(u: str, pn: str, create:bool=True) -> Optional[WikiPage]:
    """ return a wiki page. If it doesn't exist, return None.
    @param u = user name
    @param pn = the page name
    @param create = if True, and the page doesn't exit, create it
    """
    wp = WikiPage.find_one({
        'owner_id': u,
        'pageName': pn},
        sort='version')
    
    if create and not wp:
        wp = WikiPage(
            owner_id=u, 
            pageName=pn, 
            source=form("# %s\n\n", pn))
        wp.save()
    return wp

def getWikiPages(u: str) -> Iterable[WikiPage]:
    """ return all the wiki pages for a user 
    @param u = user name
    """
    wps = WikiPage.find({'owner_id': u}, sort='pageName')
    return wps
                         
    
    

#---------------------------------------------------------------------

#end
