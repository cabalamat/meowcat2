# bztypes.py = types for bozen

from typing import *

import pymongo
from bson.objectid import ObjectId


#---------------------------------------------------------------------

"""
A database _id field is either a MongoDB ObjectId (a 12 byte value displayed
as 24 hex digits, or a string. If it is a string:

* allowed characters are letters, digits and "-"
* it must not be empty
* if it is exactly 24 chars long, at least one must not be in [0-9a-f], so
  it looks distinct fromn an ObjectId
"""
DbId = Union[ObjectId, str]

"""
Contains a string that will be diosplayed on the screen; contrast
with DbValue.
"""
DisplayValue = str

"""
An HtmlStr is a string that includes HTML markup, e.g. "<b>bold</b>"
"""
HtmlStr = str

""" 
a value in a FormDoc field as it will go in the Database
"""
DbValue = str

"""
ChoiceList is used for the choices in ChoiceFiled and MultiChoiceField
"""
ChoiceList = List[Tuple[DbValue, DisplayValue]]

"""
SortSpec is how MongoDB sorts are specified in Bozen. See MonDoc.fixSort(),
which converts SortSpec values into the format used by pymongo.
"""
SortSpec1 = Union[str,
                  Tuple[str,int]]
SortSpec = Union[SortSpec1, 
                 List[SortSpec1]]


"""
Jsonable is a python value that can be converted into JSON
"""

"""
MongoValue is a value that can go in a MongoBD document 
"""

"""
MongoDict is a MongoDB object (==python dictionary)
"""


#---------------------------------------------------------------------

#end
