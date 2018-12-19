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

import mark

#---------------------------------------------------------------------
# messages

MESS_TIME_DISPLAY_FORMAT = "%Y.%m.%d %H:%M:%S"

class Message(MonDoc):
    title = StrField(readOnly=True)
    source = TextAreaField(monospaced=True)
    html = TextAreaField(monospaced=True, readOnly=True)
    
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
        
    def preSave(self):
        """ before saving, create the html and title """
        self.html = mark.md(self.source)
        
        # title
        lines = self.source.split("\n")
        if len(lines)>=1:
            line0 = lines[0].strip()
            self.title = line0
        else:
            self.title = ""
        
        
    #==========
    
    def viewH(self) -> str:
        """ return HTML displaying this message """
        h = form("""
<div class='mess'>            
    <div class='mess-header'>
        {messLink}/{userLink} at {published}
    </div>
    {body}
    <p class='mess-footer'><a href=''>context</a> 
    - <a href=''>thread</a> 
    - <a href=''>reply</a> 
    - <a href=''>view source</a></p>
</div>""",
            messLink = self.linkA(),
            userLink = self.author.blogLink(),
            published = self.asReadableH('published'),
            body = self.html,
        )
        return h
    
    def linkA(self) -> str:
        """ link to this message's /mess page """
        h = form("<a href='/mess/{id}'>{id}</a>",
            id = htmlEsc(self._id))
        return h
    
    #==========

Message.autopages(
    showFields=['title','source','author_id', 'published'], 
    sort='published')

#---------------------------------------------------------------------
# tags   


#---------------------------------------------------------------------


#end

