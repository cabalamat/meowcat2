# rssin.py = /rssin endpoint
 
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

import messlist
   
#---------------------------------------------------------------------

     
#---------------------------------------------------------------------
  
@app.route('/rssin')
def rssin():
    """ Display RSS page """
    tem = jinjaEnv.get_template("rssin.html")
    h = tem.render()
    return h
   
#---------------------------------------------------------------------
  

#end
