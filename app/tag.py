# tag.py = tags

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
 
@app.route('/popularTags')
def popularTags():
    count = models.Tag.count()
    pag = paginate.Paginator(count)
    tem = jinjaEnv.get_template("popularTags.html")
    h = tem.render(
        table = popularTagsTable(pag),
        pag = pag,
    )
    return h

def popularTagsTable(pag: paginate.Paginator) -> str:
    """ table of popular tags """
    h = """<table class='bz-report-table'>
<tr>
    <th>Tag</th>
    <th>Popularity</th>
    <th>Created</th>
    <th>Last Used</th>
</tr>
"""
    tags = models.Tag.find(
        skip=pag.skip, # skip this number of docs before returning some
        limit=pag.numShow, # max number of docs to return
        sort=[('timesUsed',-1),('lastUsed',-1),'_id'])
    for t in tags:
        h += form ("""<tr>
    <td><a href='/tag/{id}'>#{id}</a></td>
    <td style='text-align:right;'>{timesUsed}</td>
    <td>{created}</td>
    <td>{lastUsed}</td>
</tr>""",
            id =t._id,
            timesUsed = t.asReadableH('timesUsed'),
            created = t.asReadableH('created'),
            lastUsed = t.asReadableH('lastUsed'),
        )
    #//for t
    h += "</table>"
    return h

#---------------------------------------------------------------------
    
class TagFormatter(messlist.ListFormatter):
    
    def __init__(self, t: str):
        super().__init__()
        self.tag = t
        self.q = {'tags': self.tag}
    
    def pageUrl(self) -> str:
        """ Return the url of the page,
        """
        return "/tag/" + self.tag
    
    def getFeedGenerator(self) -> FeedGenerator:
        fg = FeedGenerator()
        fg.title("%s - Messages tagged %s" % (config.SITE_NAME, self.tag))
        fg.link(href="%s/tag/%s" % (config.SITE_STUB, self.tag))
        fg.description("Messages tagged %s" % (self.tag,))
        return fg  
  
@app.route('/tag/<t>')
def tag(t): 
    lf = TagFormatter(t)
    tem = jinjaEnv.get_template("tag.html")
    
    h = tem.render(
        t = t,
        lf = lf,
        qh = htmlEsc(repr(lf.q)),
    )
    return h

@app.route('/rss/tag/<t>') 
def rss_tag(t):
    """ RSS feed for messages of a tag """
    lf = TagFormatter(t)
    xml = lf.renderRss()
    return Response(xml, mimetype="text/xml")

@app.route('/au/tag/<t>')
def au_tag(t):
    lf = TagFormatter(t)
    ts = lf.mostRecentTimeStamp()
    tsj = json.dumps({'ts':ts})
    dpr("ts=%r tsj=%r", ts, tsj)
    return tsj   
 
   
#---------------------------------------------------------------------




#end
