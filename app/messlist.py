# messlist.py = lists of messages

from typing import *

import models


MESS_SHOW = 15 # default messages to show
MESS_SHOW_ONE = 100 # default messages to show when one-line
   
#---------------------------------------------------------------------
   
class ListFormatter:
    """ formats a list of messages """


    def __init__(self, q):
        self.q = q

    def getMessages(self) -> Iterable[models.Message]:
        ms = models.Message.find(self.q, 
             sort=('published', -1),
             limit=MESS_SHOW)
        return ms
        
        
    def getMessagesH(self) -> str:
        """ Return HTML for the list of messages """
        h = ""
        for m in self.getMessages():
            h += m.viewH() + "<p></p>"
        #//for
        return h


    #========== methods to be implemented by subclass


    #========== auto-update


    #========== RSS methods
    
    def renderRss(self) -> str:
        """ Return RSS for this feed """


#---------------------------------------------------------------------


#end
