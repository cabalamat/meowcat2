# login.py = pages for logging in and users 

"""
Contains pages:

  / = for logging in
  /logout = log out the current user
  /users = show all users
  /user = show a user's data

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
# Front page (/)

# page to go to, on login, if the user is an engineer
ENG_ON_LOGIN_PAGE = "/startday"

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

@app.route('/users')
def users():
    tem = jinjaEnv.get_template("users.html")
    h = tem.render(
        table = usersTable(),
        count = userdb.User.count(),
    )
    return h

def usersTable():
    """ returns an html table of users """
    h = """<table class='bz-report-table'>
<tr>
   <th class=debug>(id)</th>
   <th>User name</th>
   <th>Email</th>
   <th>Is Admin?</th>
   <th>Is Active?</th>
</tr>
"""
    for doc in userdb.User.find(sort=[('userName',pymongo.ASCENDING)]):

        item = form("""<tr>
    <td>{a}</td>
    <td>{email}</td>
    <td>{isAdmin}</td>
    <td>{isActive}</td>
</tr>""",
            a = doc.a(),
            userName = doc.asReadableH('userName'),
            email = doc.asReadableH('email'),
            isAdmin = doc.asReadableH('isAdmin'),
            isActive = doc.asReadableH('isActive'),
        )
        h += item
    #//for
    h += "</table>\n"
    return h

def yn(b):
    if b:
        return "Yes"
    else:
        return "No"

def orNone(s):
    if s:
        return htmlEsc(s)
    else:
        return "<span class='unemphasized'>None</span>"

#---------------------------------------------------------------------


@app.route('/user/<id>', methods=['POST', 'GET'])
def user(id):
    if id=='NEW':
        doc = userdb.User()
        dpr("doc=%r", doc)
    else:
        doc = userdb.User.getDoc(id)
        dpr("doc=%r", doc)
    msg = ""

    if request.method=='POST':
        doc = doc.populateFromRequest(request)
        if doc.isValid():
            if request.form['delete']=="1":
                doc.delete()
                msg = "Deleted user"
            else:    
                doc.save()
                msg = "Saved user"
    #//if

    tem = jinjaEnv.get_template("user.html")
    h = tem.render(
        doc = doc,
        id = htmlEsc(id),
        msg = ht.goodMessageBox(msg),
    )
    return h


#---------------------------------------------------------------------


#end