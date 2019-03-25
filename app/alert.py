# alert.py = pages for alerts

from flask import request, redirect, Response

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import paginate

import config
from allpages import app, jinjaEnv
import userdb
import permission
from permission import needUser
import models
  

#---------------------------------------------------------------------

@app.route('/alerts/<t>')
@needUser
def alerts(t) -> str:
    """ the current user's alerts """
    cun = permission.currentUserName()
    count = models.Alert.count({'user_id': cun})
    pag = paginate.Paginator(count)
    
    tem = jinjaEnv.get_template("alerts.html")
    h = tem.render(
        count = count,
        pag = pag,
        table = alertsTable(cun, pag),
    )
    return h

def alertsTable(cun: str, pag: paginate.Paginator) -> str:
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
    als = models.Alert.find({'user_id': cun},
        skip = pag.skip, 
        limit = pag.numShow,
        sort=('created',-1))
    for al in als:
        h += form("""<tr>
    <td>{created}</td>    
    <td>{alertType}</td>   
    <td><a href='/mess/{mid}'>{title}</a></td>   
    <td><a href='/blog/{doer}'>@{doer}</a></td>  
    <td>{reply}</td>        
</tr>""",
            created = al.asReadableH('created'),
            alertType = al.asReadableH('alertType'),
            mid = al.message_id,
            title = al.message.asReadableH('title'),
            doer = al.doer_id,
            reply = al.asReadableH('reply_id')
        )
    #//for al
    h += "</table>"
    return h

#---------------------------------------------------------------------

#end
