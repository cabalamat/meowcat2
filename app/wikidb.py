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
    
    def preCreate(self):
        self.published = BzDateTime.now()
      

def getWikiPage(u: str, pn: str) -> Optional[WikiPage]:
    """ return a wiki page. If it doesn't exist, return None.
    @param u = user name
    @param pn = the page name
    """
    wp = WikiPage.find_one({
        'owner_id': u,
        'pageName': pn},
        sort='version')
    return wp


#---------------------------------------------------------------------

#end
