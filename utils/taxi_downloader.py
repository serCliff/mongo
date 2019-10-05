import urllib
from bs4 import BeautifulSoup
import feedparser


def rss_feed():
    link_rss = "https://datos.madrid.es/sites/v/index.jsp" \
               "?vgnextoid=4f16216612d39410VgnVCM2000000c205a0aRCRD" \
               "&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD" \
               "&vgnextfmt=rss" \
               "&preview=full"
    feed = feedparser.parse(link_rss)
    return feed

