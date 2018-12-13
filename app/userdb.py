# userdb.py = user collection in database

"""
This module codes collections in the database for users and roles.
It interacts with Flask-login, for which see:
    <https://flask-login.readthedocs.org/en/latest/>

The 'user' collection stores usernames and passwords.
"""

import random
import string
from typing import *

import pyscrypt

from bozen import butil
from bozen.butil import printargs, dpr, toBytes

import bozen
from bozen import (MonDoc,
    StrField, TextAreaField,
    ChoiceField, FK, FKeys, MultiChoiceField,
    DateField, DateTimeField,
    IntField, FloatField, BoolField)

from allpages import jinjaEnv, app
from permission import loginManager

HIDDEN = "(hidden)"

#---------------------------------------------------------------------
# Users are stored in the user table

class User(MonDoc):
    userName = StrField(charsAllowed = string.ascii_letters
            + string.digits + "_",
        minLength = 2,
        desc="user name")
    hashedPassword = StrField()
    pw = StrField(desc="unencrypted password, for testing")
    password = StrField(default=HIDDEN) # for altering on /user page
    email = StrField(monospaced=True)
    isAdmin = BoolField(desc="is this user an admin?", 
        title="Is Admin?",
        default=False)
    isActive = BoolField(desc="is this an active user?", 
        title="Is Active?",
        default=True)
    following_ids = FKeys('User',
        title="Following",
        readOnly=True,
        desc="users this user is following")
    realName = StrField(
        desc="your real name or anything else you want to put here")

    @classmethod
    def classLogo(cls):
        return "<i class='fa fa-user'></i> "

    def __repr__(self):
        """ Return a string representation of myself.
        @return::str
        """
        s = "<User %r pw=%r email=%r>" % (
            self.userName, self.pw, self.email)
        return s

    #========== stuff Flask-login needs: ==========
    """ see
    <https://flask-login.readthedocs.org/en/latest/#your-user-class>
    """

    def get_id(self):
        return self.userName

    @property
    def is_authenticated(self):
        return self.isAuthenticated()

    @property
    def is_anonymous(self):
        return not self.has_key('_id')

    @property
    def is_active(self):
        return True

    def isAuthenticated(self):
        """ Do we have a logged-in user?
        @return::bool
        """
        return self.has_key('_id')

    #==========

    def getIcon(self):
        return "<i class='fa fa-user'></i> "

    def preSave(self):
        """ We don't want to save the plaintext password to
        the database.
        """
        if self.password != HIDDEN:
            self.pw = self.password
            self.hashedPassword = hashPassword(self.password)
        self.password = HIDDEN

        # userName is a unique identifier, so use this as the _id
        self._id = self.userName



@loginManager.user_loader
def load_user(userId):
    user = User.find_one({'userName': userId})
    #pr("%s~~~ usedId=%r user=%r ~~~%s",
    #   termcolours.TermColours.MAGENTA,
    #   userId, user,
    #   termcolours.TermColours.NORMAL)

    # Note that if a user wasn't found, (user) will be None
    # here, which is what loginManager wants.
    return user

#---------------------------------------------------------------------
# functions for encrypting passwords:

def randStr(length):
    return ''.join(chr(random.randint(0,255))
                   for i in range(length))

def hashPassword(password: str) -> str:
    encrypted = pyscrypt.hash(
        password = toBytes(password),
        salt = toBytes("salt"), 
        N=128, r=1, p=1, dkLen=256)
    dpr("encrypted=%r:%s", encrypted, type(encrypted))
    hx = toHex(encrypted)
    dpr("hx=%r:%s", hx, type(hx))
    return hx

def verifyPassword(hashedPassword, guessedPassword):
    encrypted = pyscrypt.hash(
        password = toBytes(guessedPassword),
        salt = toBytes("salt"), 
        N=128, r=1, p=1, dkLen=256)
    dpr("encrypted=%r:%s", encrypted, type(encrypted))
    hx = toHex(encrypted)
    dpr("hx=%r:%s", hx, type(hx))
    ok = (hx == hashedPassword)
    dpr("hashedPassword=%r ok=%r", hashedPassword, ok)
    return ok


def toHex(s: Union[str,bytes]) -> str:
    """ convert a str to another str containing hex digits, e.g.
    '\xab' -> 'ab'
    """
    hexDigits = "0123456789abcdef"
    r = ""
    for ch in s:
        if isinstance(ch, int):
            n = ch
        else:    
            n = ord(ch)
        n1 = int(n/16)
        n2 = n - n1*16
        r += hexDigits[n1] + hexDigits[n2]
    return r


#---------------------------------------------------------------------

#end
