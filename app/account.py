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
  
@app.route('/accountSettings/<id>')
def accountSettings(id):
    user = User.getDoc(id)
    ai = models.getAccountInfo(id)
        
    tem = jinjaEnv.get_template("accountSettings.html")
    h = tem.render(
        id = id,
        user = user,
        ai = ai,
    )
    return h
 
    
#---------------------------------------------------------------------
