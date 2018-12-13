# models.py = database initilisation for frambozenapp


import bozen
from bozen.butil import *
from bozen import MonDoc, BzDateTime
from bozen import (StrField, ChoiceField, TextAreaField,
    IntField, FloatField, BoolField,
    MultiChoiceField, FK, FKeys,
    DateField, DateTimeField)

import config
bozen.setDefaultDatabase(config.DB_NAME)
import allpages
bozen.notifyFlaskForAutopages(allpages.app, allpages.jinjaEnv)

#---------------------------------------------------------------------
# messages

class Message(MonDoc):
    title = StrField()
    body = TextAreaField()
    replyTo_id = FK('Message', allowNull=True,
        desc="the message this is a reply to")
    author_id = FK('User', allowNull=False,
        desc="the author of this message")
    #tags_ids = FKeys('Tag')
    published = DateTimeField(readOnly=True)
     
    @classmethod
    def classLogo(cls):
        return "<i class='fa fa-comment-o'></i> "
    
    def preCreate(self):
        self.published = BzDateTime.now()

Message.autopages(
    showFields=['title','body','author_id', 'published'], 
    sort='published')

#---------------------------------------------------------------------
# tags   


#---------------------------------------------------------------------


#end

