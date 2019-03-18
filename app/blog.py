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
  
class BlogFormatter(messlist.ListFormatter):
    
    def __init__(self, id: str):
        super().__init__()
        self.id = id
        self.q = {'author_id': id}
    
    def pageUrl(self) -> str:
        """ Return the url of the page,
        """
        return "/blog/" + id
    
    def getFeedGenerator(self) -> FeedGenerator:
        """ return a feed generator for an RSS feed for this class
        """
        ai = models.getAccountInfo(self.id)
        fg = FeedGenerator()    
        fg.title(ai.title or self.id)
        fg.author({'name': self.id}) 
        fg.link(href="%s/blog/%s" % (config.SITE_STUB, self.id))
        fg.description(ai.bioHtml)  
        return fg

    
#---------------------------------------------------------------------
 
@app.route('/blog/<id>')
def blog(id):
    user = User.getDoc(id)
    ai = models.getAccountInfo(id)
    lf = BlogFormatter(id)
    numPosts = models.Message.count({'author_id': id})
    numHeadPosts = models.Message.count({
        'author_id': id,
        'replyTo_id': {'$in': [None, '']},  
    })
    numFollowing = len(ai.following_ids)
    numFollowers = models.AccountInfo.count({'following_ids': id})
    
    cun = currentUserName()
    if not cun:
        # not logged in, so no follow button
        followButton = ""
    else:
        if models.follows(cun, id):
            # follows, so unfollow button
            followButton = "unfollow"
        else:  
            # doesn't currently follow, so follow button  
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
        numPosts = numPosts,
        numHeadPosts = numHeadPosts,
        numFollowing = numFollowing,
        numFollowers = numFollowers,
        followButton = followButton,
        lf = lf,
        fof = lf.fof,
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
    lf = BlogFormatter(id)
    xml = lf.renderRss()
    return Response(xml, mimetype="text/xml")

 
@app.route('/au/blog/<id>')
def au_blog(id):
    lf = BlogFormatter(id)
    ts = lf.mostRecentTimeStamp()
    tsj = json.dumps({'ts':ts})
    dpr("ts=%r tsj=%r", ts, tsj)
    return tsj   
    
#---------------------------------------------------------------------


#end
