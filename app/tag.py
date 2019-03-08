# tag.py = tags

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
   
   
class TagFormatter(messlist.ListFormatter):
    
    def __init__(self, t: str):
        super().__init__()
        self.tag = t
        self.q = {'tags_ids': self.tag}
    
    def pageUrl(self) -> str:
        """ Return the url of the page,
        """
        return "/tag/" + self.tag
    
  
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
   
#---------------------------------------------------------------------




#end
