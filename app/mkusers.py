# mkusers.py = make some users (for testing)

import bozen
from bozen.butil import *

import config
bozen.setDefaultDatabase(config.DB_NAME)
import userdb
import models

#---------------------------------------------------------------------

def makeUser(un):
    u = userdb.User.getDoc(un)
    if u:
        # user already exists, nothing to do
        return
    
    u = userdb.User(
        userName = un,
        password="password",
        email=un+"@example.com")
    u.save()
    dpr("created user %r", u)

def makeUsers():
    for i in range(22):
        makeUser("theuser%i" % (i,))

#---------------------------------------------------------------------

if __name__=='__main__':
    makeUsers()

#end
