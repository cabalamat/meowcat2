# blog.py = the /blog page
 
from flask import request, redirect

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import paginate

from allpages import app, jinjaEnv
import ht
from userdb import User
   
#---------------------------------------------------------------------
  
@app.route('/blog/<id>')
def blog(id):
    user = User.getDoc(id)
        
    tem = jinjaEnv.get_template("blog.html")
    h = tem.render(
        user = user,
        id = id,
    )
    return h
 
    
#---------------------------------------------------------------------


#end
