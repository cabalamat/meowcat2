# bozenutil.py = utility function etc for Bozen


#---------------------------------------------------------------------

class Incrementor:
    """ every time you call an instance of this class, it returns 1
    more than the last time it was called.
    """

    def __init__(self, before=0):
        self.i = before

    def __call__(self):
        self.i += 1
        return self.i

#---------------------------------------------------------------------

#end

