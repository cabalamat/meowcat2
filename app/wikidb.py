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

#---------------------------------------------------------------------

#end
