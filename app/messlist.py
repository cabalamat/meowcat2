# messlist.py = lists of messages

import models


MESS_SHOW = 15 # default messages to show
MESS_SHOW_ONE = 100 # default messages to show when one-line
   
#---------------------------------------------------------------------
   
class ListFormatter:
    """ formats a list of messages """


    def __init__(self, q):
        self.q = q

    def getMessagesH(self) -> str:
        """ Return HTML for the list of messages """
        ms = models.Message.find(self.q, sort=('published', -1))
        h = ""
        for m in ms:
            h += m.viewH()
        #//for
        return h


    #========== methods to be implemented by subclass


    #========== auto-update


    #========== RSS methods


#---------------------------------------------------------------------


#end
