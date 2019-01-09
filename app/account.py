# account.py = account settings, etc

from flask import request, redirect

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import paginate

from allpages import app, jinjaEnv
import ht
from userdb import User
import models
   
#---------------------------------------------------------------------
  
@app.route('/accountSettings/<id>', methods=['POST', 'GET'])
def accountSettings(id):
    user = User.getDoc(id)
    ai = models.getAccountInfo(id)
    msg = ""
        
    if request.method=='POST':
        ai = ai.populateFromRequest(request)
        ai.save()
        msg = "Saved account settings"
    #//if    
    
    tem = jinjaEnv.get_template("accountSettings.html")
    h = tem.render(
        id = id,
        user = user,
        ai = ai,
        msg = ht.goodMessageBox(msg),
    )
    return h
 
    
#---------------------------------------------------------------------
