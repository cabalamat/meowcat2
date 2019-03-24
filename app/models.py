# models.py = database initilisation for frambozenapp

from typing import *
import json

import bozen
from bozen.butil import *
from bozen import MonDoc, BzDateTime
from bozen import (StrField, ChoiceField, TextAreaField,
    IntField, FloatField, BoolField,
    MultiChoiceField, FK, FKeys, ObjectField,
    DateField, DateTimeField)

import config
bozen.setDefaultDatabase(config.DB_NAME)
import allpages
from allpages import app, jinjaEnv
bozen.notifyFlaskForAutopages(allpages.app, allpages.jinjaEnv)

import userdb
from permission import currentUserName, needUser
import mark

#---------------------------------------------------------------------
# messages

MESS_TIME_DISPLAY_FORMAT = "%Y-%m-%d %H:%M"

class Message(MonDoc):
    title = StrField(readOnly=True)
    source = TextAreaField(monospaced=True, required=True)
    html = TextAreaField(monospaced=True, readOnly=True)
    
    replyTo_id = FK('Message', allowNull=True,
        desc="the message this is a reply to")
    author_id = FK('User', allowNull=False,
        desc="the author of this message")
    tags = ObjectField()
    published = DateTimeField(readOnly=True,
        dateTimeFormat=MESS_TIME_DISPLAY_FORMAT)
    starredBy_ids = FKeys('User')
    numStars = IntField(desc='number of stars on this message')
     
    @classmethod
    def classLogo(cls) -> str:
        return "<i class='fa fa-comment-o'></i> "
    
    def preCreate(self):
        self.published = BzDateTime.now()
        
    def preSave(self):
        """ before saving, create the title """
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
    - <a href='/messSource/{id}'>source</a>
    {reply}
    - {star}
    </p>
</div>""",
            id = self.id(),
            messLink = self.linkA(),
            userLink = self.author.blogLink(),
            replyToText = self.replyToText(),
            published = self.asReadableH('published'),
            body = self.html,
            context = self.contextA(),
            reply = self.replyA(),
            star = self.starH(),
        )
        return h
    
    def starH(self) -> str:
        """ The HTML for a star underneath a message """
        h = ""; c = ""
        if self.numStars >= 1: 
            h = form("{} ", self.numStars)
        cun = currentUserName()
        if not cun or cun==self.author_id:
            #>>>>> not logged in, or author
            h += "<i class='fa fa-star-o fa-lg'></i> "
        else:
            #>>>>> user is not message author
            # has this user starred the message?
            starred = cun in self.starredBy_ids
            if starred:
                h += "<i class='starred fa fa-star fa-lg'></i> "
                c = "starred"
            else:
                h += form("""<i onclick='starClicked("{mid}")' """
                    "class='can_star fa fa-star-o fa-lg'></i> ",
                    mid = self._id)
                c = "can_star"
        #//if
        h2 = form("<span class='{c}'>{h}</span>",
            c = c,
            h = h)
        return h2
        
    
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
    
    def viewOneLine(self, showAuthor:bool =True) -> str:
        """ View this message as one line 
        @parasm showAuthor = if true, show the author of this message
        """
        publishedShort = self.asReadableH('published')[2:]
        title = self.asReadableH('title')
        authorA = ""
        if showAuthor:
            authorA = form("<a class='author' "
                "href='/blog/{u}'>@{u}</a> ",
                u = self.author_id)
        h = form("<br>{publishedShort} "
            "{authorA}"
            "<a href='/mess/{id}'>{title}</a>\n", 
            publishedShort = publishedShort, 
            authorA = authorA,
            id = self.id(),
            title = title)
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

#Message.autopages(
#    showFields=['title', 'source', 'replyTo_id', 'author_id', 'published'], 
#    sort='published')

#---------------------------------------------------------------------
"""
Holds information about an account other that what is in the user table.
The key is the User._id.
"""

class AccountInfo(MonDoc):
    _id = StrField(desc="User id", title="User Id",
        required=True, readOnly=True)
    bio = TextAreaField(desc="Biography of user (Markdown)",
        cols=60, rows=8,
        monospaced=True)
    bioHtml = TextAreaField(desc="bio compiled to HTML",
        monospaced=True, readOnly=True, displayInForm=False)
    title = StrField(title="Title of Blog")
    following_ids = FKeys('AccountInfo',
        title="Following",
        readOnly=True,
        desc="users this user is following")
    realName = StrField(
        desc="your real name or anything else you want to put here")
    
    def url(self):
        """ The URL for an acocunt is that accounts blog page """
        return "/blog/" + self._id
    
    def preCreate(self):
        self.title = form("{id}'s blog", 
            self.asReadableH('_id'))
    
    def preSave(self):
        """ before saving, create the bioHtml """
        self.bioHtml, _ = mark.render(self.bio)

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

class Tag(MonDoc):
    _id = StrField(desc="tag id")
    created = DateTimeField(desc="when tag was created")
    lastUsed = DateTimeField(desc="when tag was most recently used")
    timesUsed = IntField(desc="number of times used")
        
    def getName(self) -> str:
        return "#" + self._id

    @classmethod
    def classLogo(cls) -> str:
        return "<i class='fa fa-hashtag'></i> "
    
def notifyTags(tags: List[str]):
    """ notify that a message with new tags has been saved """
    for ts in tags:
        notifyTag(ts)

def notifyTag(ts: str):
    t = Tag.getDoc(ts)
    now = BzDateTime.now()
    if t:
        t.lastUsed = now
        t.timesUsed += 1
    else:
        t = Tag(_id = ts,
            created = now,
            lastUsed = now,
            timesUsed = 1)
    t.save()    

#---------------------------------------------------------------------
# Alerts

ALERT_TYPES = [
    ('star', "Message starred"), 
    ('reply', "Message replied to"),    
]    

class Alert(MonDoc):
    user_id = FK(userdb.User, desc="who this alert is for")
    alertType = ChoiceField(choices=ALERT_TYPES,
        desc="type of this alert",
        allowNull=False,
        readOnly=True)
    message_id = FK(Message, desc="the message this alert relates to")
    live = BoolField(default=False,
        desc="an alert is live until the user clicks to view it")
    created = DateTimeField(desc="when this alert was created",
        readOnly=True)
    doer_id = FK(userdb.User, desc="user who starred/replied")
    reply_id = FK(Message, desc="the reply",
         allowNull=True)         
        


@app.route('/numActiveAlerts')
@needUser
def numActiveAlerts() -> str:
    #numAlerts = Alert.count(activeAlertQ())
    numAlerts = 12
    #dpr("numAlerts=%r", numAlerts)
    return json.dumps([numAlerts])


#---------------------------------------------------------------------


#end

