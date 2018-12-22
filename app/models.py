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

from permission import currentUserName
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
        
        #>>>>> title
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
        {messLink}/{userLink} at {published}{replyToText}
    </div>
    {body}
    <p class='mess-footer'><a href=''>context</a> 
    - <a href=''>thread</a> 
    {reply}
    - <a href='/messSource/{id}'>view source</a></p>
</div>""",
            id = self.id(),
            messLink = self.linkA(),
            userLink = self.author.blogLink(),
            replyToText = self.replyToText(),
            published = self.asReadableH('published'),
            body = self.html,
            reply = self.replyA(),
        )
        return h
    
    def linkA(self) -> str:
        """ link to this message's /mess page """
        h = form("<a href='/mess/{id}'>{id}</a>",
            id = htmlEsc(self._id))
        return h
    
    def replyA(self) -> str:
        """ html containing the link to reply to this message.
        If not logged in this is empty.
        """
        cun = currentUserName()
        if not cun: return ""
        h = form("- <a href='/messRep/{id}'>reply</a> ",
            id = self.id())
        return h
    
    def replyToText(self) -> str:
        """ if this message is a reply, text in the header linking to the
        message it's a reply to. """
        if not self.replyTo_id: return ""
        parent = self.replyTo
        if not parent: return ""
        h = form(" reply-to: {messLink}/{userLink}",
            messLink = parent.linkA(),
            userLink = parent.author.blogLink()
        )
        return h
                 
    
    #==========

Message.autopages(
    showFields=['title', 'source', 'replyTo_id', 'author_id', 'published'], 
    sort='published')

#---------------------------------------------------------------------
# tags   


#---------------------------------------------------------------------


#end

