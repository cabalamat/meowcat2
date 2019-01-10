# blog.py = the /blog page
 
from flask import request, redirect

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import paginate

from allpages import app, jinjaEnv
import ht
from userdb import User
import models
import permission

import messlist
   
#---------------------------------------------------------------------
  
@app.route('/blog/<id>')
def blog(id):
    user = User.getDoc(id)
    ai = models.getAccountInfo(id)
    q = {'author_id': user._id}
    lf = messlist.ListFormatter(q)
    
    cun = permission.currentUserName()
    if not cun:
        # not logged in, so no follow button
        followButton = ""
    else:
        if models.follows(cun, id):
            # follows, so unfollow button
            followButton = "unfollow"
        else:  
            # diesn't currently follow, so follow button  
            followButton = "follow"
    dpr("followButton=%r", followButton)        
        
    tem = jinjaEnv.get_template("blog.html")
    h = tem.render(
        id = id,
        user = user,
        ai = ai,
        messages = lf.getMessagesH(),
        blogTitle = ai.asReadableH('title'),
        name = ai.asReadableH('realName'),
        bio = ai.bioHtml,
        followButton = followButton,
    )
    return h
 
    
#---------------------------------------------------------------------


#end
