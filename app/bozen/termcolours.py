# termcolours.py

"""***
Optional support for printing to the terminal in multiple colurs

***"""

#---------------------------------------------------------------------

class TermColours:
   BLACK   = chr(27) + "[0;30m"
   RED     = chr(27) + "[0;31m"
   GREEN   = chr(27) + "[0;32m"
   BLUE    = chr(27) + "[0;34m"
   MAGENTA = chr(27) + "[0;35m"
   
   RED_ON_GREY = chr(27) + "[47;31m"
   LRED_ON_GREY = chr(27) + "[1;47;31m"
   BLACK_ON_RED = chr(27) + "[41;30m"
   BLACK_ON_GREY = chr(27) + "[47;30m"
   BLUE_ON_GREY = chr(27) + "[47;34m"
   YELLOW_ON_RED =  chr(27) + "[1;47;30m"
   GREY_ON_WHITE = chr(27) + "[48;37m"
   DGREY_ON_WHITE = chr(27) + "[1;48;30m"
   LCYAN_ON_BLUE = chr(27) + "[1;44;36m"
   
   NORMAL = chr(27) + "[0m"
   BOLD = chr(27) + "[1m"
   FAINT = chr(27) + "[2m"
   UNDERLINE = chr(27) + "[4m"


class NullColours:
   BLACK   = ''
   RED     = ''
   GREEN   = ''
   BLUE    = ''
   MAGENTA = ''
   RED_ON_GREY = ''
   LRED_ON_GREY = ''
   BLACK_ON_RED = ''
   BLACK_ON_GREY = ''
   BLUE_ON_GREY = ''
   YELLOW_ON_RED =  ''
   GREY_ON_WHITE = ''
   DGREY_ON_WHITE = ''
   LCYAN_ON_BLUE = ''



#end
