# ht.py = project-level html functions

from bozen import butil
from bozen.butil import form

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

def boolH(b: bool, yesText:str="yes", noText:str="no") -> str:
    """ Return html for a boolean
    """
    if b:
        h = form("<span class='yes'><i class='fa fa-check'></i> {}</span>",
            yesText)
    else:
        h = form("<span class='no'><i class='fa fa-times'></i> {}</span>",
            noText)
    return h


#---------------------------------------------------------------------


#end
