# star.py = pages for starring

from flask import request, redirect, Response

from bozen.butil import pr, prn, dpr, form, htmlEsc
from bozen import paginate

import config
from allpages import app, jinjaEnv
import userdb
import permission
import models
   
#---------------------------------------------------------------------
 
@app.route('/mostStarred')
@app.route('/mostStarred/<uid>')
def mostStarred(uid=None):
    """ list of most-starred messages """
    if uid:
        u = userdb.User.getDoc(uid)
        if not u:
            return permission.http404()
        q = {'author_id': uid}
    else:
        q = {}
        uid = None
    q.update({'numStars': {'$gte': 1}})  
    count = models.Message.count(q)
    pag = paginate.Paginator(count)
    tem = jinjaEnv.get_template("mostStarred.html")
    h = tem.render(
        count = count,
        uid = uid,
        pag = pag,
        table = mostStarredTable(q, pag),
    )
    return h

def mostStarredTable(q: dict, pag: paginate.Paginator) -> str:
    """ html table of most-starred messages 
    @param q = MongoDB query
    """
    h = """<table class='bz-report-table'>
<tr>
    <th>Message</th>
    <th>Author</th>
    <th>Stars</th>
    <th>Published</th>
</tr>
"""
    ms = models.Message.find(q,
        skip = pag.skip, 
        limit = pag.numShow,
        sort = [('numStars',-1), 'published'])
    for m in ms:
        h += form("""<tr>
    <td><a href='/mess/{mid}'>{title}</a></td>
    <td><a href='/blog/{u}'>@{u}</a></td>
    <td style='text-align:right;'>{numStars}</td>
    <td>{published}</td>
</tr>""",
            mid = m._id,
            title = m.asReadableH('title'),
            u = m.author_id,
            numStars = m.asReadableH('numStars'),
            published = m.asReadableH('published'),
        )
    #//for m
    h += "</table>"
    return h
  
#---------------------------------------------------------------------
  
#end
