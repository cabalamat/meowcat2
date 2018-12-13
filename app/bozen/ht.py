# ht.py = project-level html functions

from . import butil
from .butil import form

#---------------------------------------------------------------------

def errorBox(msg: str, escapeForHtml:bool=True) -> str:
    """ if a message is blank, leave it blank.
    Otherwise, wrap it up in css that makes it look like a
    pretty error message.
    @param msg = message to be displayed
    @param escapeForHtml = if True, the msg is deemed to contain
       a non-html string, which  needs to be escaped for HTML (because
       it might contain chars such as "&" or "<"). Set to False if
       msg contains HTML.
    """
    if not msg: return ""
    if escapeForHtml:
        msgH = butil.htmlEsc(msg)
    else:
        msgH = msg
    h = form("<div class='form-error-line'>"
        "<i class='fa fa-warning'></i> {msg}</div>",
        msg = msgH)
    return h

def warningBox(msg: str, escapeForHtml:bool=True) -> str:
    """ If a message is blank, leave it blank.
    Otherwise, wrap it up in css that makes it look like a
    pretty warning message.
    @param msg = message to be displayed
    @param escapeForHtml = if True, the msg is deemed to contain
       a non-html string, which  needs to be escaped for HTML (because
       it might contain chars such as "&" or "<"). Set to False if
       msg contains HTML.
    """
    if not msg: return ""
    if escapeForHtml:
        msgH = butil.htmlEsc(msg)
    else:
        msgH = msg
    h = form("<div class='form-warning-line'>"
        "<i class='fa fa-question-circle'></i> {msg}</div>",
        msg = msgH)
    return h

def goodMessageBox(msg: str, escapeForHtml:bool=True) -> str:
    """ If a message is blank, leave it blank.
    Otherwise, wrap it up in css that makes it look like a
    pretty warning message.
    @param msg = message to be displayed
    @param escapeForHtml = if True, the msg is deemed to contain
       a non-html string, which  needs to be escaped for HTML (because
       it might contain chars such as "&" or "<"). Set to False if
       #msg contains HTML.
    """
    if not msg: return ""
    if escapeForHtml:
        msgH = butil.htmlEsc(msg)
    else:
        msgH = msg
    h = form("<div class='message-box'>"
        "{msg}</div>",
        msg = msgH)
    return h
messageBox = goodMessageBox


#---------------------------------------------------------------------


#end
