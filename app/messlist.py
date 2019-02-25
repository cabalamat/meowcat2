# messlist.py = lists of messages

from typing import *

from feedgen.feed import FeedGenerator
from flask import request, redirect, Response

import bozen
from bozen import (MonDoc, FormDoc,
    StrField, TextAreaField, PasswordField,
    ChoiceField, FK, FKeys, MultiChoiceField,
    DateField, DateTimeField,
    IntField, FloatField, BoolField)

import models


MESS_SHOW = 10 # default messages to show
MESS_SHOW_ONE = 100 # default messages to show when one-line
   
#---------------------------------------------------------------------
 
class FormattingOptionsForm(FormDoc):
    oneLine = BoolField(desc="show one line summary",
        widget='toggleSwitch', showTitle = False,
        offText = "Show Message", onText = "1-Line Summary")
    
    headOnly = BoolField(desc="show head posts only",
        widget='toggleSwitch', showTitle = False,
        default = True,
        offText = "All Posts", onText = "Head Posts")
    
    mrf = BoolField(desc="most recent posts first",
        widget='toggleSwitch', showTitle = False,
        default = True,
        offText = "Oldest First", onText = "Most Recent First")
    
    au = BoolField(desc="Auto Update",       
        widget='toggleSwitch', showTitle = False,
        offText = "Static", onText = "Auto Update")
    
    def setFromUrl(self):
        """ Set the values of the fields in the form to that
        from the GET parameters in the URL """
        x = request.args.get('x', "")
        if not x:
            # no form fields, don't change anything
            return
        
        self.oneLine = bool(request.args.get('oneLine', False))
        self.headOnly = bool(request.args.get('headOnly', False))
        self.mrf = bool(request.args.get('mrf', False))
        self.au = bool(request.args.get('au', False))
 
 
#---------------------------------------------------------------------
   
class ListFormatter:
    """ formats a list of messages """


    def __init__(self, q):
        self.q = q
        self.fof = FormattingOptionsForm()
        self.fof.setFromUrl()

    def getMessages(self) -> Iterable[models.Message]:
        q2 = {}
        q2.update(self.q)
        
        if self.fof.oneLine:
            numShow = MESS_SHOW_ONE
        else:
            numShow = MESS_SHOW
        
        if self.fof.headOnly:
            # only select head posts
            q2.update({'replyTo_id': {'$in': [None, '']}})
            
        if self.fof.mrf: 
            sortValue = ('published', -1)  
        else:
            sortValue = ('published', 1)  
            
        ms = models.Message.find(q2, 
             sort=sortValue,
             limit=numShow)
        return ms
        
        
    def getMessagesH(self) -> str:
        """ Return HTML for the list of messages """
        h = ""
        if self.fof.oneLine:
            for m in self.getMessages():
                h += m.viewOneLine()
            #//for    
        else:    
            for m in self.getMessages():
                h += m.viewH() + "<p></p>"
            #//for
        return h


    #========== methods to be implemented by subclass


    #========== auto-update


    #========== RSS methods
    

    def setRssFeed(self, feed: FeedGenerator):
        self.rssFeed = feed

    def renderRss(self) -> str:
        """ Return RSS for this feed """
        
        for m in self.getMessages():
            fe = self.rssFeed.add_entry()
            fe.id(m.fullUrl())
            fe.title(m.title)
            fe.content(m.html)
        #//for  
        
        return self.rssFeed.rss_str(pretty=True) 


#---------------------------------------------------------------------


#end
