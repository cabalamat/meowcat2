# blog.py = the /blog page
 
import json 
 
from feedgen.feed import FeedGenerator
from flask import request, redirect, Response

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import FormDoc, MonDoc, BzDate, BzDateTime
from bozen import paginate

import config
from allpages import app, jinjaEnv
import ht
from userdb import User
import models
from permission import needUser, currentUserName

import messlist
   
#---------------------------------------------------------------------
  
@app.route('/blog/<id>')
def blog(id):
    user = User.getDoc(id)
    ai = models.getAccountInfo(id)
    q = {'author_id': user._id}
    lf = messlist.ListFormatter(q)
    
    cun = currentUserName()
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
        idJson = json.dumps(id),
        user = user,
        ai = ai,
        messages = lf.getMessagesH(),
        blogTitle = ai.asReadableH('title'),
        name = ai.asReadableH('realName'),
        bio = ai.bioHtml,
        followButton = followButton,
    )
    return h
 
@app.route('/x/follow/<id>/<status>', methods=['POST', 'GET'])
@needUser
def xFollow(id: str, status: str):
    """
    @param id = the followee user who the currently-logged-in user
        is following or unfollowing
    @param status = following status, 0=unfollow, 1=follow
    """
    makeFollowing = (status=="1")
    cun = currentUserName()
    dpr("id=%r status=%r cun=%r", id, status, cun)
    if not cun: return "{}"

    cu = User.getDoc(cun)
    if not cu: return "{}"
    followee = User.getDoc(id)
    if not followee: return "{}"

    ai = models.getAccountInfo(cun)
    followingSet = set(ai.following_ids)
    if makeFollowing:
        followingSet2 = followingSet | set([id])
    else:
        followingSet2 = followingSet - set([id])
    if followingSet2 != followingSet:
        ai.following_ids = list(followingSet2)
        ai.save()
    return "{}"    

     
#---------------------------------------------------------------------
  
@app.route('/rss/blog/<id>')
def rss_blog(id):
    """ RSS feed for blog """
    user = User.getDoc(id)
    ai = models.getAccountInfo(id)
    q = {'author_id': user._id}
    lf = messlist.ListFormatter(q)
    
    fg = FeedGenerator()
    
    fg.title(ai.title or id)
    fg.author({'name': ai.realName or id}) 
    fg.link(href="%s/blog/%s" % (config.SITE_STUB, id))
    fg.description(ai.bioHtml)
    
    lf.setRssFeed(fg)
    xml = lf.renderRss()
    return Response(xml, mimetype="text/xml")

    
    
#---------------------------------------------------------------------


#end
