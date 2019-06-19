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

#---------------------------------------------------------------------
# WikiPage table

class WikiPage(MonDoc):
    _id = StrField(readOnly=True)
    owner_id = FK('User', allowNull=False,
        desc="the owner of this wikipage")
    folder = StrField(desc="path to folder")
    filename = StrField(desc="canonical filename (in folder)")
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
        
    def canAlter(self, userName: str) -> bool:
        """ Can a user alter this wiki page? 
        At the moment only the owner of a apge can alter it.
        Later we will enable collaborative wikis.
        """
        return canAlter(userName, self.owner_id, self.folder, self.filename)

def getWikiPage(u: str, folder: str, filename: str) -> Optional[WikiPage]:
    """ return a wiki page. If it doesn't exist, return None.
    @param u = user name
    @param folder = the path to the page (not inculding filename)
    @param filename = the filename
    """
    wantedId = (u + "/"
        + folder
        + ("/" if folder else "")
        + filename)
    wp = WikiPage.getDoc(wantedId)
    return wp

def canAlter(u2: str, u: str, folder: str, filename: str) -> bool:
    """ Can a user alter this wiki page? 
    @param u2 = user who we are asking if they can alter it
    (u, folder, filename) = address of page
      
    At the moment only the owner of a page can alter it.
    Later we will enable collaborative wikis.
    """
    return u2 == u

#---------------------------------------------------------------------

#end
