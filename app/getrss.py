# getrss.py = get RSS data

import requests

URL = "http://esr.ibiblio.org/?feed=rss2"

def getRss(u):
    r = requests.get(u)
    dpr("status_code=%r", r.status_code)
    dpr("\n----- r.text=\n%s\n-----(end)", r.text)

if __name__=='__main__':
    getRss(URL)


#end
