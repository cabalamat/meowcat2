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

MESS_TIME_DISPLAY_FORMAT = "%Y.%m.%d %H:%M:%S"

class Message(MonDoc):
    title = StrField()
    body = TextAreaField()
    replyTo_id = FK('Message', allowNull=True,
        desc="the message this is a reply to")
    author_id = FK('User', allowNull=False,
        desc="the author of this message")
    #tags_ids = FKeys('Tag')
    published = DateTimeField(readOnly=True,
        dateTimeFormat=MESS_TIME_DISPLAY_FORMAT)
     
    @classmethod
    def classLogo(cls) -> str:
        return "<i class='fa fa-comment-o'></i> "
    
    def preCreate(self):
        self.published = BzDateTime.now()
        
    #==========
    
    def viewH(self) -> str:
        """ return HTML displaying this message """
        h = form("""
<div class='mess'>            
    <div class='mess-header'>
        {messLink}/{userLink} at {published}
    </div>
    <h3>{title}</h3>
    {body}
    <p class='mess-footer'>context -- thread -- reply -- view source</p>
</div>""",
            messLink = self.linkA(),
            userLink = self.author.blogLink(),
            published = self.asReadableH('published'),
            title = self.asReadableH('title'),
            body = self.asReadableH('body'),
        )
        return h
    
    def linkA(self) -> str:
        """ link to this message's /mess page """
        h = form("<a href='/mess/{id}'>{id}</a>",
            id = htmlEsc(self._id))
        return h
    
    #==========

Message.autopages(
    showFields=['title','body','author_id', 'published'], 
    sort='published')

#---------------------------------------------------------------------
# tags   


#---------------------------------------------------------------------


#end

