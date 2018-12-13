# front.py = front page

from allpages import app, jinjaEnv
from bozen.butil import pr, prn

prn("*** front.py ***")

#---------------------------------------------------------------------

@app.route('/')
def front():
    tem = jinjaEnv.get_template("front.html")
    h = tem.render(
    )
    return h


# end
