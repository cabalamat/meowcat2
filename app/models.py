# models.py = database initilisation for frambozenapp

from typing import *

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
        
    def url(self):
        u = "/mess/" + self.id()
        return u
    
    def fullUrl(self):
        return config.SITE_STUB + self.url()
        
    #========== display a message ==========
    
    def viewH(self) -> str:
        """ return HTML displaying this message """
        h = form("""
<div class='mess'>            
    <div class='mess-header'>
        {messLink}/{userLink} at {published}{replyToText}
    </div>
    {body}
    <p class='mess-footer'>
    {context}
    - <a href='/thread/{id}'>thread</a> 
    {reply}
    - <a href='/messSource/{id}'>view source</a></p>
</div>""",
            id = self.id(),
            messLink = self.linkA(),
            userLink = self.author.blogLink(),
            replyToText = self.replyToText(),
            published = self.asReadableH('published'),
            body = self.html,
            context = self.contextA(),
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
                 
    def contextA(self) -> str:
        """ if post is a reply, return html for link to context of post """
        if self.isHeadPost(): return ""
        h = form("- <a href='/context/{id}'>context</a>",
            id = self.id())
        return h
    
    #========== misc utility functions ==========
    
    def context(self) -> List['Message']:
        """ the list of messages leading up to this one, including this 
        one, in chronological order 
        """
        if self.isHeadPost(): return [self]
        parent = self.getParent()
        if parent:
            return parent.context() + [self]
        else: 
            return [self]     
    
    def isReply(self) -> bool:
        return bool(self.replyTo_id)
    
    def isHeadPost(self) -> bool:
        return not self.isReply()
    
    def getParent(self) -> Union['Message',None]:
        """ if a post has a parent, return it, else return None """
        if self.isHeadPost(): return None
        return Message.getDoc(self.replyTo_id)
        
    def getNumChildren(self) -> int:
        """ return the number of replies this message has """
        return Message.count({'replyTo_id': self._id})
    
    def getChildren(self):
        """ return an iterator to the message's replies (oldest first) 
        returns an Iterable[Message]
        """
        ms = Message.find({'replyTo_id': self._id}, sort='published')
        return ms

Message.autopages(
    showFields=['title', 'source', 'replyTo_id', 'author_id', 'published'], 
    sort='published')

#---------------------------------------------------------------------
"""
Holds information about an account other that what is in the user table.
The key is the User._id.
"""

class AccountInfo(MonDoc):
    _id = StrField(desc="User id", readOnly=True)
    bio = TextAreaField(desc="Biography of user (Markdown)",
        monospaced=True)
    bioHtml = TextAreaField(desc="bio compiled to HTML",
        monospaced=True, readOnly=True)
    title = StrField(title="Title of Blog")
    following_ids = FKeys('AccountInfo',
        title="Following",
        readOnly=True,
        desc="users this user is following")
    realName = StrField(
        desc="your real name or anything else you want to put here")
    
    def preCreate(self):
        self.title = form("{id}'s blog", 
            self.asReadableH('_id'))
    
    def preSave(self):
        """ before saving, create the bioHtml """
        self.bioHtml = mark.md(self.bio)

AccountInfo.autopages()

def getAccountInfo(userId: str) -> AccountInfo:
    """ get an account info, creating it if necessary """
    ai = AccountInfo.getDoc(userId)
    if not ai:
        ai = AccountInfo(_id=userId)
    return ai    

def follows(a1: str, a2: str) -> bool:
    ai = AccountInfo.find_one({'_id': a1, 'following_ids': a2})
    return bool(ai)
    

#---------------------------------------------------------------------
# tags   


#---------------------------------------------------------------------


#end

