# blog.py = the /blog page
 
from flask import request, redirect

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import paginate

from allpages import app, jinjaEnv
import ht
from userdb import User
import models

import messlist
   
#---------------------------------------------------------------------
  
@app.route('/blog/<id>')
def blog(id):
    user = User.getDoc(id)
    ai = models.getAccountInfo(id)
    q = {'author_id': user._id}
    lf = messlist.ListFormatter(q)
        
    tem = jinjaEnv.get_template("blog.html")
    h = tem.render(
        id = id,
        user = user,
        ai = ai,
        messages = lf.getMessagesH(),
        blogTitle = ai.asReadableH('title'),
        name = ai.asReadableH('realName'),
        bio = ai.bioHtml,
    )
    return h
 
    
#---------------------------------------------------------------------


#end
