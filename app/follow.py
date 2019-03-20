# follow.py = pages relating to folloing/followers

from typing import *
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

@app.route('/listFollowing/<id>')
def listFollowing(id):
    """ list of people who follow (id) """   
    user = User.getDoc(id)
    ai = models.getAccountInfo(id)
    count = len(ai.following_ids)
    pag = paginate.Paginator(count)
    
    tem = jinjaEnv.get_template("listFollowing.html")
    h = tem.render(
        id = id,
        user = user,
        ai = ai,
        count = count,
        pag = pag,
        table = followingTableH(ai, pag),
    )
    return h
 
def followingTableH(ai: str, pag: paginate.Paginator) -> str:
    h = USER_INFO_TABLE_HEADER
    userIds = sorted(ai.following_ids)
    userIds2 = userIds[pag.skip:pag.skip+pag.numShow]
    for userId in userIds2:
        h += userInfoLine(userId)
    #//for
    h += "</table>\n"
    return h

USER_INFO_TABLE_HEADER = """<table class='bz-report-table'>
<tr>
    <th>User</th>
    <th>Posts</th>
    <th>Head<br>Posts</th>
    <th>Following</th>
    <th>Followers</th>
    <th>Real<br>Name</th>
    <th>Blog<br>Title</th>
</tr>
"""   

def userInfoLine(id: str) -> str:
    """ Return an HTML line (<tr>) for one user.
    """
    ai = models.getAccountInfo(id)
    numPosts = models.Message.count({'author_id': id})
    numHeadPosts = models.Message.count({
        'author_id': id,
        'replyTo_id': {'$in': [None, '']},  
    })
    numFollowing = len(ai.following_ids)
    numFollowers = models.AccountInfo.count({'following_ids': id})

    h = form("""<tr>
    <td><a href='/blog/{user}'>@{user}</a></td> 
    <td style='text-align:right;'>{numPosts}</td> 
    <td style='text-align:right;'>{numHeadPosts}</td> 
    <td style='text-align:right;'>
        <a href='/listFollowing/{user}'>{numFollowing}</a> &nbsp;
        <a href='/followingMess/{user}'><i class='fa fa-eye'></i></a></td> 
    <td style='text-align:right;'>
        <a href='/listFollowers/{user}'>{numFollowers}</a> &nbsp;
        <a href='/followerMess/{user}'>
            <i class='fa fa-arrow-circle-left'></i></a></td>   
    <td>{realName}</td> 
    <td>{title}</td> 
</tr>""",
            user = id,
            numPosts = numPosts, 
            numHeadPosts = numHeadPosts,
            numFollowing = numFollowing,
            numFollowers = numFollowers,
            realName = ai.asReadableH('realName'),
            title = ai.asReadableH('title'),
    )
    return h
    
 
 
#---------------------------------------------------------------------

@app.route('/listFollowers/<id>')
def listFollowers(id):
    """ list of people who follow (id) """   
    user = User.getDoc(id)
    count = models.AccountInfo.count({'following_ids': id})
    pag = paginate.Paginator(count)
    
    tem = jinjaEnv.get_template("listFollowers.html")
    h = tem.render(
        id = id,
        user = user,
        count = count,
        pag = pag,
        table = followersTableH(id, pag),
    )
    return h
 
def followersTableH(id: str, pag: paginate.Paginator) -> str:
    h = USER_INFO_TABLE_HEADER
    followers = models.AccountInfo.find({'following_ids': id},
        skip=pag.skip, # skip this number of docs before returning some
        limit=pag.numShow, # max number of docs to return
        sort='_id')
    for follower in followers:
        h += userInfoLine(follower._id)
    #//for
    h += "</table>\n"
    return h
 
#---------------------------------------------------------------------


@app.route('/userList')
def userList():
    """ list all users """   
    count = User.count()
    pag = paginate.Paginator(count)
    tem = jinjaEnv.get_template("userList.html")
    h = tem.render(
        count = count,
        pag = pag,
        table = userListTableH(pag),
    )
    return h

def userListTableH(pag):
    h = USER_INFO_TABLE_HEADER
    users = User.find(
        skip=pag.skip, # skip this number of docs before returning some
        limit=pag.numShow, # max number of docs to return
        sort='_id')
    for u in users:
        h += userInfoLine(u._id)
    #//for
    h += "</table>\n"
    return h
 
#---------------------------------------------------------------------

class FollowingFormatter(messlist.ListFormatter):
    
    def __init__(self, id: str):
        super().__init__()
        self.id = id
        ai = models.getAccountInfo(id)
        self.q = {'author_id': {'$in': ai.following_ids}}
    
    def pageUrl(self) -> str:
        """ Return the url of the page,
        """
        return "/followingMess/" + id
    
    def getFeedGenerator(self) -> FeedGenerator:
        """ return a feed generator for an RSS feed for this class
        """
        fg = FeedGenerator()
        fg.title("%s - Newsfeed for @%s" % (config.SITE_NAME, self.id))
        fg.link(href="%s/followingMess/%s" % (config.SITE_STUB, self.id))
        fg.description("Newsfeed for @%s" % (self.id,))
        return fg

@app.route('/followingMess/<id>')
def followingMess(id): 
    user = User.getDoc(id)
    lf = FollowingFormatter(id)
    tem = jinjaEnv.get_template("followingMess.html")
    
    h = tem.render(
        id = id,
        user = user,
        lf = lf,
    )
    return h

@app.route('/rss/followingMess/<id>') 
def rss_followingMess(id):
    """ RSS feed for following messages """
    lf = FollowingFormatter(id)
    xml = lf.renderRss()
    return Response(xml, mimetype="text/xml")

@app.route('/au/followingMess/<id>')
def au_followingMess(id):
    lf = FollowingFormatter(id)
    ts = lf.mostRecentTimeStamp()
    tsj = json.dumps({'ts':ts})
    return tsj   
     
#---------------------------------------------------------------------

class FollowerFormatter(messlist.ListFormatter):
    
    def __init__(self, id: str):
        super().__init__()
        self.id = id
        followers = models.AccountInfo.find({'following_ids': id})
        follower_ids = [f._id for f in followers]
        self.q = {'author_id': {'$in': follower_ids}}
    
    def pageUrl(self) -> str:
        """ Return the url of the page,
        """
        return "/followerMess/" + id
    
    def getFeedGenerator(self) -> FeedGenerator:
        """ return a feed generator for an RSS feed for this class
        """
        fg = FeedGenerator()
        fg.title("%s - Followers of @%s" % (config.SITE_NAME, self.id))
        fg.link(href="%s/followerMess/%s" % (config.SITE_STUB, self.id))
        fg.description("Followers of @%s" % (self.id,))
        return fg

@app.route('/followerMess/<id>')
def followerMess(id): 
    user = User.getDoc(id)
    lf = FollowerFormatter(id)
    tem = jinjaEnv.get_template("followerMess.html")
    
    h = tem.render(
        id = id,
        user = user,
        lf = lf,
    )
    return h

@app.route('/rss/followerMess/<id>') 
def rss_followerMess(id):
    lf = FollowerFormatter(id)
    xml = lf.renderRss()
    return Response(xml, mimetype="text/xml")
  
@app.route('/au/followerMess/<id>')
def au_followerMess(id):
    lf = FollowerFormatter(id)
    ts = lf.mostRecentTimeStamp()
    tsj = json.dumps({'ts':ts})
    return tsj   
    
  
 
#---------------------------------------------------------------------
 

#end
