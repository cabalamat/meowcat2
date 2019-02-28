# follow.py = pages relating to folloing/followers

from typing import *
 
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
    
    tem = jinjaEnv.get_template("listFollowing.html")
    h = tem.render(
        id = id,
        user = user,
        ai = ai,
        table = followingTableH(id, ai),
    )
    return h
 
def followingTableH(id, ai):
    h = """<table class='bz-report-table'>
<tr>
    <th>User</th>
    <th>Posts</th>
    <th>Head Posts</th>
    <th>Following</th>
    <th>Followers</th>
</tr>
"""
    userIds = sorted(ai.following_ids)
    for userId in userIds:
        np, nhp, nf, nfer = getNumPostFollowInfo(userId)
        h += form("""<tr>
    <td><a href='/blog/{user}'>@{user}</a></td> 
    <td style='text-align:right;'>{numPosts}</td> 
    <td style='text-align:right;'>{numHeadPosts}</td> 
    <td style='text-align:right;'>
        <a href='/listFollowing/{user}'>{numFollowing}</a></td> 
    <td style='text-align:right;'>
        <a href='/listFollowers/{user}'>{numFollowers}</a></td>                                    
</tr>""",
            user = userId,
            numPosts = np, 
            numHeadPosts = nhp,
            numFollowing = nf,
            numFollowers = nfer,
        )
    #//for
    h += "</table>\n"
    return h
 
def getNumPostFollowInfo(id: str) -> Tuple[int,int,int,int]:
    """ For a user get:
    - number of posts the user has written
    - number of head posts the user has written
    - number of accounts the user is following
    - number of accounts who follow the user
    """   
    ai = models.getAccountInfo(id)
    numPosts = models.Message.count({'author_id': id})
    numHeadPosts = models.Message.count({
        'author_id': id,
        'replyTo_id': {'$in': [None, '']},  
    })
    numFollowing = len(ai.following_ids)
    numFollowers = models.AccountInfo.count({'following_ids': id})
    return (numPosts, numHeadPosts, numFollowing, numFollowers)
    
 
#---------------------------------------------------------------------

@app.route('/listFollowers/<id>')
def listFollowers(id):
    """ list of people who follow (id) """   
    user = User.getDoc(id)
    
    tem = jinjaEnv.get_template("listFollowers.html")
    h = tem.render(
        id = id,
        user = user,
        table = followersTableH(id),
    )
    return h
 
def followersTableH(id):
    h = """<table class='bz-report-table'>
<tr>
    <th>User</th>
    <th>Posts</th>
    <th>Head Posts</th>
    <th>Following</th>
    <th>Followers</th>
</tr>
"""    
    followers = models.AccountInfo.find({'following_ids': id},
        sort='_id')
    for follower in followers:
        ferId = follower._id
        np, nhp, nf, nfer = getNumPostFollowInfo(follower._id)
        h += form("""<tr>
    <td><a href='/blog/{user}'>@{user}</a></td> 
    <td style='text-align:right;'>{numPosts}</td> 
    <td style='text-align:right;'>{numHeadPosts}</td> 
    <td style='text-align:right;'>
        <a href='/listFollowing/{user}'>{numFollowing}</a></td> 
    <td style='text-align:right;'>
        <a href='/listFollowers/{user}'>{numFollowers}</a></td>                                    
</tr>""",
            user = ferId,
            numPosts = np, 
            numHeadPosts = nhp,
            numFollowing = nf,
            numFollowers = nfer,
        )
    #//for
    h += "</table>\n"
    return h
 
#---------------------------------------------------------------------
 

#end
