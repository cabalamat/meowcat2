# mess.py = the /mess page, view a single message
 
from flask import request, redirect

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import (StrField, ChoiceField, TextAreaField,
    IntField, FloatField, BoolField,
    MultiChoiceField, FK, FKeys,
    DateField, DateTimeField)

from allpages import app, jinjaEnv
import ht
from userdb import User
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
   
@app.route('/messRep')
@app.route('/messRep/<id>')
def messRep(id=None):
    if id:
        isReply = True
        m = models.Message.getDoc(id)
        mh = m.viewH()
    else:    
        isReply = False
        m = None
        mh = ""
        
    mf = MessageForm()    
        
    tem = jinjaEnv.get_template("messRep.html")
    h = tem.render(
        id = id,
        isReply = isReply,
        m = m,
        mh = mh,
        mf = mf,
        msg = "",
    )
    return h
 
#---------------------------------------------------------------------


#end