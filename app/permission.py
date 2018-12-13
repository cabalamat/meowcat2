# permission.py = permissions to view pages

import functools

from flask import request, redirect
from flask_login import LoginManager, current_user, logout_user

from bozen.butil import dpr

import ht
import allpages
from allpages import jinjaEnv


#---------------------------------------------------------------------
# login manager

loginManager = LoginManager()
loginManager.init_app(allpages.app)

def needUser(fn):
    """ decorator that requires a page to have a logged in user """
    import models
    @functools.wraps(fn)
    def viewWrapper(*args, **kwargs):
        if not models.goodDMS():
            return http403("User permission error")
        if currentUserName() == "":
            return http403()
        return fn(*args, **kwargs)
    return viewWrapper

#---------------------------------------------------------------------
# global functions (for all templates)

jinjaEnv.globals['currentUser'] = current_user
def currentUserName():
    #pr("current_user=%r::%s", current_user, type(current_user))
    if ((not current_user)
        or current_user.is_anonymous):
        return ""
    try:
        return str(current_user.userName)
    except:
        return ""
jinjaEnv.globals['currentUserName'] = currentUserName

#---------------------------------------------------------------------


def http403(msg=""):
    """
    @param msg::str = contains text as an optional error message.
    return a response containing an HTTP 403 (forbidden) message
    """
    tem = jinjaEnv.get_template("403.html")
    h = tem.render(
        msg = html.errorBox(msg),
    )
    return (h, 403)

#end
