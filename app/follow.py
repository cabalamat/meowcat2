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
        <a href='/listFollowing/{user}'>{numFollowing}</a></td> 
    <td style='text-align:right;'>
        <a href='/listFollowers/{user}'>{numFollowers}</a></td>                                    
</tr>""",
            user = id,
            numPosts = numPosts, 
            numHeadPosts = numHeadPosts,
            numFollowing = numFollowing,
            numFollowers = numFollowers,
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
 

#end
