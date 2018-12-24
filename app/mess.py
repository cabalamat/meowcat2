# mess.py = pages for messages
 
from flask import request, redirect

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import (StrField, ChoiceField, TextAreaField,
    IntField, FloatField, BoolField,
    MultiChoiceField, FK, FKeys,
    DateField, DateTimeField)

import mark
from allpages import app, jinjaEnv
import ht
from userdb import User
import permission
import models
import messlist
   
#---------------------------------------------------------------------

@app.route('/messList')
def messList():
    """ recent messages in message list view """
        
    lf = messlist.ListFormatter({})
        
    tem = jinjaEnv.get_template("messList.html")
    h = tem.render(
        messages = lf.getMessagesH(),
    )
    return h
 

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
        
    tem = jinjaEnv.get_template("messSource.html")
    h = tem.render(
        m = m,
        id = id,
        ms = m.viewH(),
        messSource = htmlEsc(m.source),
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
        
    mf = MessageForm()
    if request.method=='POST':
        mf = mf.populateFromRequest(request)
        
        messRepButton = request.form['messRepButton']
        dpr("messRepButton=%r", messRepButton)     
        if mf.isValid():
            if messRepButton=='preview':
                #>>>>> preview message
                previewH = mark.md(mf.message)
                hasPreview = True
            else:    
                #>>>>> create message
                dpr("create new message")
                newM = models.Message(
                    source = mf.message,
                    author_id = permission.currentUserName())
                newM.save()
                dpr("newM=%r", newM)
                u = "/mess/" + newM.id()
                dpr("u=%r", u)
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
    )
    return h
 
#---------------------------------------------------------------------
  
@app.route('/context/<id>')
def context(id):
    m = models.Message.getDoc(id)
    ms = m.context()
    msh = "<p></p>\n".join(m.viewH() for m in ms)
        
    tem = jinjaEnv.get_template("context.html")
    h = tem.render(
        m = m,
        id = id,
        msh = msh,
    )
    return h
   
#---------------------------------------------------------------------
 

#end