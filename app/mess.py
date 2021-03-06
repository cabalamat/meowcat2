# mess.py = pages for messages
 
from typing import *
import json 
 
from feedgen.feed import FeedGenerator
from flask import request, redirect, Response

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import (StrField, ChoiceField, TextAreaField,
    IntField, FloatField, BoolField,
    MultiChoiceField, FK, FKeys,
    DateField, DateTimeField)

import config
import mark
from allpages import app, jinjaEnv
import ht
from userdb import User
import permission
from permission import needUser
import models
import messlist
   
#---------------------------------------------------------------------
  
class MessListFormatter(messlist.ListFormatter):
    
    def __init__(self):
        super().__init__()
        self.q = {}
    
    def pageUrl(self) -> str:
        """ Return the url of the page,
        """
        return "/messList"
    
    def getFeedGenerator(self) -> FeedGenerator:
        fg = FeedGenerator()
        fg.title("%s - Recent Messages" % (config.SITE_NAME,))
        fg.link(href="%s/messList" % (config.SITE_STUB,))
        fg.description("Recent messages")
        return fg
  
@app.route('/messList')
def messList():
    """ recent messages in message list view """
    lf = MessListFormatter()

    tem = jinjaEnv.get_template("messList.html")
    h = tem.render(
        lf = lf,
    )
    return h
    
@app.route('/rss/messList') 
def rss_messList():
    """ RSS feed for message list """
    lf = MessListFormatter()
    xml = lf.renderRss()
    return Response(xml, mimetype="text/xml")

@app.route('/au/messList')
def au_messList():
    lf = MessListFormatter()
    ts = lf.mostRecentTimeStamp()
    tsj = json.dumps({'ts':ts})
    dpr("ts=%r tsj=%r", ts, tsj)
    return tsj

#---------------------------------------------------------------------
  
@app.route('/mess/<id>')
def mess(id):
    m = models.Message.getDoc(id)
        
    tem = jinjaEnv.get_template("mess.html")
    h = tem.render(
        m = m,
        id = id,
        ms = m.viewH(),
    )
    return h
    
#---------------------------------------------------------------------
   
@app.route('/messSource/<id>')
def messSource(id):
    m = models.Message.getDoc(id)
    starredByH = ", ".join(u for u in m.starredBy_ids)
        
    tem = jinjaEnv.get_template("messSource.html")
    h = tem.render(
        m = m,
        id = id,
        ms = m.viewH(),
        messSource = htmlEsc(m.source),
        starredBy = starredByH,
    )
    return h
    
#---------------------------------------------------------------------
   
class MessageForm(FormDoc):
    message = TextAreaField(title="Your Message",
        rows=8, cols=60,
        required=True,
        monospaced=True)
   
@app.route('/messRep', methods=['POST', 'GET'])
@app.route('/messRep/<id>', methods=['POST', 'GET'])
@needUser
def messRep(id=None):
    if id:
        isReply = True
        m = models.Message.getDoc(id)
        mh = m.viewH()
    else:    
        isReply = False
        m = None
        mh = ""
    hasPreview = False; previewH = ""   
    tags = None
        
    mf = MessageForm()
    if request.method=='POST':
        mf = mf.populateFromRequest(request)
        
        messRepButton = request.form['messRepButton']
        dpr("messRepButton=%r", messRepButton)     
        if mf.isValid():
            if messRepButton=='preview':
                #>>>>> preview message
                previewH, tags = mark.render(mf.message)
                hasPreview = True
            else:    
                #>>>>> create message
                dpr("create new message")
                previewH, tags = mark.render(mf.message)
                newM = models.Message(
                    source = mf.message,
                    html = previewH,
                    tags = tags,
                    author_id = permission.currentUserName())
                if isReply:
                    newM.replyTo_id = id
                newM.save()
                models.notifyTags(tags)
                dpr("newM=%r", newM)
                dpr("tags=%r", tags)
                u = "/mess/" + newM.id()
                dpr("u=%r", u)
                if isReply:
                    al = models.Alert(
                        user_id = m.author_id,
                        alertType = 'reply',
                        message_id = m._id,
                        doer_id = newM.author_id,
                        reply_id = newM._id)
                    al.save()
                return redirect(u, code=303)
        #//if valid 
    #//if POST   
        
    tem = jinjaEnv.get_template("messRep.html")
    h = tem.render(
        id = id,
        isReply = isReply,
        m = m,
        mh = mh,
        mf = mf,
        msg = "",
        hasPreview = hasPreview,
        previewH = previewH,
        tagsH = htmlEsc(repr(tags))
    )
    return h
 
#---------------------------------------------------------------------
 
@app.route('/editMess/<id>', methods=['POST', 'GET'])
@needUser
def editMess(id):
    """ Edit an existing message """
    m = models.Message.getDoc(id)
    
    mf = MessageForm(message=m.source)
    if request.method=='POST':
        mf = mf.populateFromRequest(request)
        previewH, tags = mark.render(mf.message)
        
        m.source = mf.message
        m.html = previewH
        m.tags = tags
        m.editedAt = BzDateTime.now()
        m.save()
    #//if    
        
    tem = jinjaEnv.get_template("editMess.html")
    h = tem.render(
        m = m,
        id = id,
        ms = m.viewH(),
        mf = mf,
    )
    return h
 
 
#---------------------------------------------------------------------
  
@app.route('/context/<id>')
def context(id):
    m = models.Message.getDoc(id)
    ms = m.context()
    msh = ("<p style='margin: 0px 0px 0px 20px;color:#666;'>"
        "<i class='fa fa-arrow-down fa-lg'></i></p>\n").join(
        m.viewH() for m in ms)
        
    tem = jinjaEnv.get_template("context.html")
    h = tem.render(
        m = m,
        id = id,
        msh = msh,
    )
    return h
#---------------------------------------------------------------------
  
@app.route('/thread/<id>')
def thread(id):
    m = models.Message.getDoc(id)
        
    tem = jinjaEnv.get_template("thread.html")
    h = tem.render(
        m = m,
        id = id,
        msh = threadFromH(m),
    )
    return h
   
def threadFromH(m: models.Message) -> str:
    """ return html containing a message and its descendents """
    h = m.viewH()
    if m.getNumChildren():
        h += "<blockquote class=thread>\n"
        h += "<p></p>\n".join(threadFromH(child) 
                              for child in m.getChildren())
        h += "</blockquote>\n"
    return h    
     
#---------------------------------------------------------------------
 

#end