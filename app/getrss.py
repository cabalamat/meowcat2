# getrss.py = get RSS data

from typing import Optional

import requests
import feedparser

from bozen.butil import *

URL = "http://esr.ibiblio.org/?feed=rss2"

def getRss(u) -> Optional[feedparser.FeedParserDict]:
    dpr("Getting RSS feed %s", u)
    r = requests.get(u)
    dpr("status_code=%r", r.status_code)
    rawData = r.text
    dpr("returned {} chars" , len(rawData))
    #dpr("\n----- r.text=\n%s\n-----(end)", r.text)
    
    feedData = feedparser.parse(rawData)
    dpr("feedData::%s", type(feedData))
    return rawData, feedData

def saveData(filename: str, data: str):
    f = open(filename, 'w')
    f.write(data)
    f.close()
    
def getFeedDataFromFile(filename: str)\
    -> Optional[feedparser.FeedParserDict]:
    f = open(filename, 'r')
    rawData = f.read()
    f.close()
    feedData = feedparser.parse(rawData)
    return feedData


def displayFeedData(fd: feedparser.FeedParserDict):
    feed = fd.feed
    prn("feed=%s", pretty(feed))
    prn("Feed Title: %s", feed.title)
    prn("Feed Link: %s", feed.link)
    prn("Feed Description: %s", feed.description)
    prn("Feed Updated: %s", feed.updated)
    prn("Feed Updated: %s", feed.updated_parsed)

if __name__=='__main__':
    #fd = getRss(URL)
    #saveData("rss", rd)
    fd = getFeedDataFromFile("rss")
    displayFeedData(fd)


#end
