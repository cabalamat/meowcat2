# test_mark.py = test <mark.py>


from bozen.butil import *
from bozen import lintest

import mark


#---------------------------------------------------------------------

class T_mark(lintest.TestCase):  
    pass

    
#---------------------------------------------------------------------


group = lintest.TestGroup()
group.add(T_mark)

if __name__=='__main__': group.run()

#end