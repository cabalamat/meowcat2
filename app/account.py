# account.py = account settings, etc

from flask import request, redirect

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import paginate

from allpages import app, jinjaEnv
import ht
from userdb import User
import models
from permission import *
   
#---------------------------------------------------------------------
  
@app.route('/accountSettings', methods=['POST', 'GET'])
@needUser
def accountSettings():
    cun = currentUserName()
    dpr("id=%r cun=%r", id, cun)
    #if id != cun:
    #    return http403()
    user = User.getDoc(cun)
    ai = models.getAccountInfo(cun)
    msg = ""
        
    if request.method=='POST':
        ai = ai.populateFromRequest(request)
        ai.save()
        msg = "Saved account settings"
    #//if    
    
    tem = jinjaEnv.get_template("accountSettings.html")
    h = tem.render(
        user = user,
        ai = ai,
        msg = ht.goodMessageBox(msg),
    )
    return h
 
    
#---------------------------------------------------------------------
