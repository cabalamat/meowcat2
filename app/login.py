# login.py = pages for logging in and users 

"""
Contains pages:

  / = for logging in
  /logout = log out the current user

See also <userdb.py> which contains the database model for users.

"""

import time
import string

from flask import request, redirect, abort
from flask_login import login_user, logout_user, current_user
import pymongo

from bozen.butil import dpr, htmlEsc, form
import bozen
from bozen import (MonDoc, FormDoc,
    StrField, TextAreaField, PasswordField,
    ChoiceField, FK, FKeys, MultiChoiceField,
    DateField, DateTimeField,
    IntField, FloatField, BoolField)

import allpages
from allpages import *
from permission import *
import ht

import userdb


#---------------------------------------------------------------------

class LoginForm(FormDoc):
    userName = StrField()
    password = PasswordField()

@app.route('/login', methods=['POST', 'GET'])
def login():
    tem = jinjaEnv.get_template("login.html")
    doc = LoginForm()
    msg = ""

    if request.method=='POST':

        #>>>>> CSRF handling
        dpr("@@@ session=%r @@@", session)
        token = session.pop('_csrf_token', None)
        dpr("@@@ token=%r @@@", token)
        #if not token or token != request.form.get('_csrf_token'):
        #    pass
        #    #abort(403)

        doc = doc.populateFromRequest(request)
        u = userdb.User.find_one({'userName': doc.userName})

        ok = u and userdb.verifyPassword(u.hashedPassword,
                                         doc.password)
        dpr("doc.password=%r ok=%r", doc.password, ok)
        if ok:
            login_user(u)
            return redirect("/", code=302)
        else:
            msg = "login failed"

    h = tem.render(
        doc = doc,
        msg = ht.errorBox(msg),
    )
    return h

#---------------------------------------------------------------------

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

#---------------------------------------------------------------------

LETTERS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
          +"abcdefghijklmnopqrstuvwxyz") 
DIGITS = "0123456789"
USER_ID_CHARS = LETTERS + DIGITS + "_"

class CreateAccountForm(FormDoc):
    userName = StrField(title="Enter New Username",
        required=True, 
        autocomplete=False,
        minLength=4, maxLength=30,
        charsAllowed=USER_ID_CHARS)
    password = PasswordField(title="Enter New Password",
        required=True, 
        autocomplete=False,
        minLength=4, maxLength=30,
        charsAllowed=USER_ID_CHARS)
    confirmPassword = PasswordField(title="Confirm Password",
        required=True,
        autocomplete=False, 
        minLength=4, maxLength=30,
        charsAllowed=USER_ID_CHARS)
    
    def formWideErrorMessage(self) -> str:
        if self.password != self.confirmPassword:
            return ("The New Password and Confirm Password fields "
                "must be the same.")
        
        return ""
    

@app.route('/createAccount', methods=['POST', 'GET'])
def createAccount():
    tem = jinjaEnv.get_template("createAccount.html")
    caf = CreateAccountForm()
    goodMsg = ""
    badMsg = ""

    if request.method=='POST':
        caf = caf.populateFromRequest(request)
        if caf.isValid():
            u = userdb.User(
                userName = caf.userName,
                password = caf.password)
            u.save()
            goodMsg = ("Have created account @%s, now you need to "
                "<a href='/login'>log in</a>." 
                % (u.userName,))
        else:
            badMsg = "Cannot create account"
    #//if    

    h = tem.render(
        caf = caf,
        goodMsg = ht.goodMessageBox(goodMsg, escapeForHtml=False),
        badMsg = ht.errorBox(badMsg),
    )
    return h


#---------------------------------------------------------------------


#end