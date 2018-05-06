# -*- coding: UTF-8 -*-
import sys
import urllib2, re
import mysql.connector
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
# Initial the variables in comment.py:
ipeen_restaurant_id = sys.argv[1]
#comment_url = "http://www.ipeen.com.tw//comment/1414229"
comment_url = sys.argv[2]
comment_id = comment_url.replace('http://www.ipeen.com.tw//comment/', '')

print "comment_url = " + comment_url
print "comment_id = " + comment_id

comment_id = int(comment_id)
comment_title = ""
rating_score = None
delicious_level = ""
service_level = ""
atmosphere_level = ""
comment_date = ""
# ==========================================================================
response = http_download(comment_url)
soup = BeautifulSoup(response, "html.parser")

print "=========================================================="
#print "Now Processing the restaurant ID: " + sys.argv[1] + ", comment_url: " + sys.argv[2]
print "Now Processing the restaurant ID: " + ipeen_restaurant_id + ", comment_url: " + comment_url
print "=========================================================="

basic_info = soup.find("div",{"class":"info"})
comment_title = remove_html_tags(basic_info.find("h1").renderContents()).strip().replace('\n','')
print "comment_title: " + comment_title

score_info = soup.find("div",{"class":"scalar"})
scores = score_info.find_all('p')
star_class = scores[0].find("i")['class']
print "star_class = " + str(star_class)
rating_score = str(star_class).replace("[u's-","").replace("']", "")
print "rating_score = " + rating_score

comment_date = remove_html_tags(soup.find("p",{"class":"inline date"}).find('span').renderContents().strip())
print "comment_date = " + comment_date

rating_info = score_info.find('dl',{"class":"rating"})
#print "rating_info = " + str(rating_info)

ratings = rating_info.findAll("dd")
delicious_level = remove_html_tags(str(ratings[0]))
service_level = remove_html_tags(str(ratings[1]))
atmosphere_level = remove_html_tags(str(ratings[2]))
print "delicious_level = " + delicious_level
print "service_level = " + service_level
print "atmosphere_level = " + atmosphere_level

section_block = soup.find("section",{"class":"main layout-wrapper"})
description_block = section_block.find("div",{"class":"description"})
paragraphs = description_block.findAll("p", {"style":"text-align:center;"})

picture_url_list = []
#print paragraphs
for paragraph in paragraphs:
    image_info = paragraph.find("img")
    if image_info is None:
        continue
    else:
        #print "Picture Url: " + str(image_info['src'])
        picture_url_list.append(str(image_info['src']))
# ---------------------------------------------------------------------------------------------------------
connection = mysql.connector.connect(user='gobbler', password='gobbler1', host='35.160.193.220', database='gobblerdb')
cursor = connection.cursor()

try:
    # for ipeen_restaurant_comment:
    query = "SELECT comment_id FROM ipeen_restaurant_comment where comment_id='%d'" %(comment_id)
    cursor.execute(query)
    row = cursor.fetchone()
    if row != None:
        print "The page %d is parsed before!!!!!!!" %(int(ipeen_restaurant_id))
        exit()
    else:
        # pre-process for number fields:
        if rating_score is None:
            rating_score = 0
        else:
            rating_score = float(rating_score)/10.0
        sql_comment = "INSERT INTO ipeen_restaurant_comment \
                     (ipeen_restaurant_id, comment_id, comment_title, rating_score, delicious_level, \
                      service_level, atmosphere_level, comment_date, comment_url) \
                      VALUES('%d', '%d', '%s', '%f', '%s', \
                             '%s', '%s', '%s', '%s')" % \
                      (int(ipeen_restaurant_id), comment_id, comment_title, rating_score, delicious_level, \
                       service_level, atmosphere_level, comment_date, comment_url)
        cursor.execute(sql_comment)
        connection.commit()
except Exception as e:
    print e
    connection.rollback()

try:
    print "str(len(picture_url_list))" + str(len(picture_url_list))
    # for ipeen_restaurant_comment_picture:
    for picture_url in picture_url_list:
        print "picture_url = " + picture_url
        sql_picture = "INSERT INTO ipeen_restaurant_comment_picture \
                     (comment_id, comment_url, picture_url) \
                      VALUES('%d', '%s', '%s')" % \
                      (comment_id, comment_url, picture_url)
        cursor.execute(sql_picture)
        connection.commit()
except Exception as e:
    print e
    connection.rollback()
finally:
    cursor.close()
