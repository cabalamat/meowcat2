# __init__.py = initialisation for Bozen

# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))


#---------------------------------------------------------------------
# utility and debugging modules

#import butil


#---------------------------------------------------------------------
# bozen form and field classes

from .formdoc import FormDoc

from .fieldinfo import FieldInfo, StrField, TextAreaField, PasswordField
from .keychoicefield import ChoiceField, FK
from .numberfield import IntField, FloatField, BoolField
from .multichoicefield import MultiChoiceField, FKeys
from .timefield import BzDate, DateField, BzDateTime, DateTimeField
from .objectfield import ObjectField

                       
#---------------------------------------------------------------------
# interact with mongoDB

from .mongo import setDefaultDatabase, getDefaultDatabase
from .mondoc import MonDoc
    
    
#---------------------------------------------------------------------
# utilities for HTML / web pages

from .paginate import Paginator
from .autopages import notifyFlaskForAutopages
 
#---------------------------------------------------------------------
# admin site

from .admin import AdminSite
  
    
#---------------------------------------------------------------------



#end
