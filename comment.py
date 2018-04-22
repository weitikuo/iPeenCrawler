# -*- coding: UTF-8 -*-
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
restaurantID = sys.argv[1]
#comment_url = "http://www.ipeen.com.tw/comment/1414229"
comment_url = sys.argv[2]
response = http_download(comment_url)
soup = BeautifulSoup(response, "html.parser")

print "=========================================================="
#print "Now Processing the restaurant ID: " + sys.argv[1] + ", comment page: " + sys.argv[2]
print "Now Processing the restaurant ID: " + restaurantID + ", comment page: " + comment_url
print "=========================================================="

basic_info = soup.find("div",{"class":"info"})
comment_title = remove_html_tags(basic_info.find("h1").renderContents()).strip().replace('\n','')
print "comment_title: " + comment_title

score_info = soup.find("div",{"class":"scalar"})
scores = score_info.find_all('p')
star_class = scores[0].find("i")['class']
print "star_class = " + str(star_class)

rating_info = score_info.find('dl',{"class":"rating"})
#print "rating_info = " + str(rating_info)

ratings = rating_info.findAll("dd")
print "Delicious Level = " + remove_html_tags(str(ratings[0]))
print "Service Level = " + remove_html_tags(str(ratings[1]))
print "Atmosphere Level = " + remove_html_tags(str(ratings[2]))

section_block = soup.find("section",{"class":"main layout-wrapper"})
description_block = section_block.find("div",{"class":"description"})
paragraphs = description_block.findAll("p", {"style":"text-align:center;"})
#print paragraphs
for paragraph in paragraphs:
    image_info = paragraph.find("img")
    if image_info is None:
        continue
    else:
        print "Picture Url: " + str(image_info['src'])
