# alert.py = pages for alerts

from flask import request, redirect, Response

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import paginate

import config
from allpages import app, jinjaEnv
import tabs
import userdb
import permission
from permission import needUser
import models
  
#---------------------------------------------------------------------

ALERT_TABS = [
    ('replies', "<i class='fa fa-reply'></i>  Replies"),
    ('stars', "<i class='fa fa-star'></i> Stars"),
    ('current', "<i class='fa fa-bell'></i> Current"),
    ('historic', "<i class='fa fa-bell-o'></i> Historic"),
]

def alertTabLine(tab):
    """ Return HTML for the current tab line
    @return::str containing html
    """
    h = tabs.makeTabLine3(ALERT_TABS, tab, "/alerts/{TAB}")
    return h

#---------------------------------------------------------------------

@app.route('/alerts/replies')
@needUser
def alerts_replies() -> str:
    """ alerts for replies to the current user's posts """
    cun = permission.currentUserName()
    q = {'user_id': cun, 
         'alertType': 'reply', 
         'live': True}
    count = models.Alert.count(q)

    tem = jinjaEnv.get_template("alerts_replies.html")
    h = tem.render(
        tabLine = alertTabLine("replies"),
        count = count,
        messages = getMessages(q)
    )
    return h

def getMessages(q: dict) -> str:
    """ get messages corresponsing to query (q) """
    h = ""
    als = models.Alert.find(q, sort=('created',-1))
    for al in als:
        h += al.reply.viewH() + "<p></p>"
    #//for al
    return h

#---------------------------------------------------------------------

@app.route('/alerts/stars')
@needUser
def alerts_stars() -> str:
    """ alerts for stars to the current user's posts """
    cun = permission.currentUserName()

    tem = jinjaEnv.get_template("alerts_stars.html")
    h = tem.render(
        tabLine = alertTabLine("stars"),
    )
    return h

#---------------------------------------------------------------------

@app.route('/alerts/current')
@needUser
def alerts_current() -> str:
    """ the current user's current alerts """
    cun = permission.currentUserName()
    q = {'user_id': cun, 'live': True}
    count = models.Alert.count(q)
    pag = paginate.Paginator(count)
    
    tem = jinjaEnv.get_template("alerts_current.html")
    h = tem.render(
        tabLine = alertTabLine("current"),
        count = count,
        pag = pag,
        table = alertsTable(q, pag),
    )
    return h

def alertsTable(q: dict, pag: paginate.Paginator) -> str:
    """ html table of alerts
    @param q = MongoDB query
    """
    h = """<table class='bz-report-table'>
<tr>
    <th>Time</th>
    <th>Alert Type</th>
    <th>Message</th>
    <th>Doer</th>
    <th>Reply</th>
</tr>
"""
    als = models.Alert.find(q,
        skip = pag.skip, 
        limit = pag.numShow,
        sort=('created',-1))
    for al in als:
        h += form("""<tr>
    <td>{created}</td>    
    <td>{alertType}</td>   
    <td>{message}</td>   
    <td><a href='/blog/{doer}'>@{doer}</a></td>  
    <td>{reply}</td>        
</tr>""",
            created = al.asReadableH('created'),
            alertType = al.asReadableH('alertType'),
            mid = al.message_id,
            message = al.asReadableH('message_id'),
            doer = al.doer_id,
            reply = al.asReadableH('reply_id')
        )
    #//for al
    h += "</table>"
    return h

#---------------------------------------------------------------------

@app.route('/alerts/historic')
@needUser
def alerts_historic() -> str:
    """ the current user's current alerts """
    cun = permission.currentUserName()
    q = {'user_id': cun, 'live': False}
    count = models.Alert.count(q)
    pag = paginate.Paginator(count)
    
    tem = jinjaEnv.get_template("alerts_historic.html")
    h = tem.render(
        tabLine = alertTabLine("historic"),
        count = count,
        pag = pag,
        table = alertsTable(q, pag),
    )
    return h

#---------------------------------------------------------------------

#end
