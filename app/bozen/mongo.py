# mongo.py = interface to MongoDB

from typing import *
import re

import pymongo

from .butil import *
from .bztypes import DbId

#---------------------------------------------------------------------

mongoClient = None
defaultDB = None
idInc = None  # used to increment _id values

def setDefaultDatabase(dbName: str, host="localhost", port=27017):
    global mongoClient, defaultDB, idInc
    mongoClient = pymongo.MongoClient(host, port)
    defaultDB = mongoClient[dbName]
    idInc = MongoabIncrementor(defaultDB)
    
def getDefaultDatabase()->Optional[pymongo.collection.Collection]:
    """ return the default database, if this has been set """
    return defaultDB


#---------------------------------------------------------------------
# auto-increment of identifiers for Mongo DB documents

class MongoabIncrementor:
    """ Increments a number. Used to create a unique index number
    for mongo DB databases.

    Stores value in collection 'mongoab', document id 'lastIndex'.
    """

    def __init__(self, database):
        self.database = database

    def getNewIndex(self)->int:
        self.index = self.database.bozen.find_and_modify(
            query={'_id': 'lastIndex'},
            update={'$inc': {'value': 1}},
            upsert=True,
            new=True)['value']
        dpr("new index is {}", self.index)
        return self.index
    
    def getNewIndexB36(self)->str:
        """ return the index as a base 36 string """
        return indexToBase36(self.getNewIndex())
        

    def show(self):
        """ Show the current value of the indesx, without incrementing
        it.
        @return::int
        """
        lastIndexDoc = self.database.mongoab.find_one({'_id': 'lastIndex'})
        if not lastIndexDoc:
            return 1
        value = lastIndexDoc.get('value', 1)
        return value
    
    
def indexToBase36(ix: int)->str:
    ixStr = base36encode(ix)
    if len(ixStr)<3: 
        ixStr = "0"*(3-len(ixStr)) + ixStr 
    return ixStr

BASE_36_CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"

def base36encode(n: int)->str:
    """Converts an integer to a base36 string."""
    if not isinstance(n, int):
        raise TypeError('number must be an integer')

    r = ''
    sign = ''
    if n < 0:
        sign = '-'
        n = -n

    if 0 <= n < len(BASE_36_CHARS):
        return sign + BASE_36_CHARS[n]
    while n != 0:
        n, i = divmod(n, len(BASE_36_CHARS))
        r = BASE_36_CHARS[i] + r

    return sign + r

def base36decode(number: str)->int:
    return int(number, 36)

#---------------------------------------------------------------------


validObjectId = re.compile("[0-9a-fA-F]{24}")
def isObjectIdStr(s):
    """ Is (s) a string that came from an ObjectId (24 hex digits?)
    :param string s: a string that may or may not be from an ObjectId
    :rtype bool
    """
    if not isinstance(s, str):
        return False
    return bool(validObjectId.fullmatch(s))

def normaliseId(id: DbId) -> DbId:
    """ Normalise a MongoDB id, that is, if it is convertable to an
    ObjectId, do so. Else keep it as it is.
    :param id:
    """
    if isObjectIdStr(id):
        return ObjectId(id)
    return id

#---------------------------------------------------------------------

#end
