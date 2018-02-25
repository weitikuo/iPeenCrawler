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

# ==========================================================================
url = 'http://www.ipeen.com.tw/shop/' + '67012'
response = http_download(url)
soup = BeautifulSoup(response, "html.parser")

if(str(soup).find("愛評網") == -1):
	print 'page not found!!!'
	exit()

introduction = soup.find("div",{"class":"info"})
restaurant_name = remove_html_tags(introduction.find("h1").renderContents()).strip().replace('\n','')
print "restaurant_name: " + restaurant_name

basic_info = introduction.find("div",{"class":"brief"})
cusine_style = remove_html_tags(basic_info.find("p",{"class":"cate i"}).renderContents().strip('\n'))
print "cusine_style: " + cusine_style
average_price = remove_html_tags(basic_info.find("p",{"class":"cost i"}).renderContents().strip('\n')).replace('本店均消','').replace('元','').replace(' ', '')
print "average_price: " + average_price
telephone = remove_html_tags(basic_info.find("p",{"class":"tel i"}).renderContents().strip('\n')).replace('\n', '').replace(' ', '')
print "telephone: " + telephone
address = remove_html_tags(basic_info.find("p",{"class":"addr i"}).renderContents().strip('\n')).replace('\n', '').replace(' ', '')
print "address: " + address

score_info = soup.find("div",{"class":"scalar"})
scores = score_info.find_all('p')

#star = score_info.find("p",{"class":"rating"}).find("i")
#print star

star = scores[0].find("i")
print star
ratingCount = scores[0].find("em").renderContents().strip('\n')
print "ratingCount: " + ratingCount
browse_number = scores[2].find("em").renderContents().strip('\n')
print "browse_number: " + browse_number
collect_number = scores[3].find("em").renderContents().strip('\n')
print "collect_number: " + collect_number

detail_data = soup.find("div",{"id":"shop-details"}).find("table")
detail_info = []

print detail_data

for item in detail_data.findAll("tr"):
   subitem_key = item.find("th")
   subitem_val = item.find("td")
   detail_info.append({'key' : subitem_key, 'value' : subitem_val})
   print subitem_key.renderContents() + " = " + subitem_val.renderContents()

















