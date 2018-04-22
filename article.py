# -*- coding: UTF-8 -*-
import commands
import sys
import urllib2, re
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

def http_download(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        exit()
    except urllib2.URLError, e:
        exit()

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

# 抓substring
def middle(string, lstr, rstr):
   left = string.find(lstr) + len(lstr)
   res = string[left:]
   right = res.find(rstr)
   return res[:right]

# ==========================================================================
#comment_page_url = 'http://www.ipeen.com.tw/shop/' + '67012' + '/comments' + '?p=' + '1'
comment_page_url = 'http://www.ipeen.com.tw/shop/' + sys.argv[1] + '/comments' + '?p=' + sys.argv[2]
response = http_download(comment_page_url)
soup = BeautifulSoup(response, "html.parser")

print "=========================================================="
#print "Now Processing the restaurant ID: " + '67012' + ", comment page = " + "1"
print "Now Processing the restaurant ID: " + sys.argv[1] + ", comment page = " + sys.argv[2]
print "comment_page_url = " + comment_page_url
print "=========================================================="

share_block = soup.find("section",{"class":"review-list"})
articles = share_block.findAll("article")

if len(articles) == 0:
    print 'There are no articles in the page: ' + comment_page_url
    exit()

for article in articles:
    comment_info = article.find("a")
    comment_link = 'http://www.ipeen.com.tw/' + str(comment_info['href'])
    print "comment_link = " + comment_link
    comment_picture_url = article.find("img")['src']
    print "comment_picture_url = " + comment_picture_url
    comment_title = article.find("img")['alt']
    print "comment_title = " + comment_title

    output = commands.getoutput("python comment.py " + sys.argv[1] + " " + comment_link)
    print output
