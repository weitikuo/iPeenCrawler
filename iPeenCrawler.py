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
#url = 'http://www.ipeen.com.tw/shop/' + '67012'
url = 'http://www.ipeen.com.tw/shop/' + sys.argv[1]
response = http_download(url)
soup = BeautifulSoup(response, "html.parser")

print "=========================================================="
print "Now Processing the restaurant ID: " + sys.argv[1]
print "url = " + url
print "=========================================================="

if(str(soup).find("愛評網") == -1):
	print 'page not found!!!'
	exit()

introduction = soup.find("div",{"class":"info"})
restaurant_name = remove_html_tags(introduction.find("h1").renderContents()).strip().replace('\n','')
print "restaurant_name: " + restaurant_name

if str(restaurant_name).startswith("已歇業".encode('utf-8')):
    print 'Skip this restaurant!!!'
    exit()

basic_info = introduction.find("div",{"class":"brief"})
cusine_style = remove_html_tags(basic_info.find("p",{"class":"cate i"}).renderContents().strip('\n'))
print "cusine_style: " + cusine_style
average_price = remove_html_tags(basic_info.find("p",{"class":"cost i"}).renderContents().strip('\n')).replace('本店均消','').replace('元','').replace(' ', '')
print "average_price: " + average_price
telephone = remove_html_tags(basic_info.find("p",{"class":"tel i"}).renderContents().strip('\n')).replace('\n', '').replace(' ', '')
print "phone_number: " + telephone
address = remove_html_tags(basic_info.find("p",{"class":"addr i"}).renderContents().strip('\n')).replace('\n', '').replace(' ', '')
print "address: " + address

score_info = soup.find("div",{"class":"scalar"})
scores = score_info.find_all('p')

star_class = str(scores[0].find("i"))
star = middle(star_class,'i class="s-','"></i>')
print "star: " + star

ratingCount = scores[0].find("em").renderContents().strip('\n')
print "ratingCount: " + ratingCount
browse_number = scores[2].find("em").renderContents().strip('\n')
print "browse_number: " + browse_number
collect_number = scores[3].find("em").renderContents().strip('\n')
print "collect_number: " + collect_number

detail_data = soup.find("div",{"id":"shop-details"}).find("table")
for item in detail_data.findAll("tr"):
    subitem_key = item.find("th")
    subitem_val = item.find("td")
    if subitem_key is None:
        continue
    if subitem_key.renderContents() == "商家名稱".encode('utf-8'):
        print "restaurant_name: " + subitem_val.renderContents().strip('\n')
        continue
    if subitem_key.renderContents() == "商家分類".encode('utf-8'):
        business_classification = subitem_val.renderContents().strip('\n')
        business_classification = re.sub(r'( |\n|\t|&nbsp;)+', r' ', remove_html_tags(str(business_classification))).strip()
        classifications = business_classification.split(" &gt; ");
        channel_classification = classifications[0]
        if channel_classification != "美食":
            print '不是美食!!!!!!!!!!!!!!!!!!!!!!!!!'
            exit()
        super_big_classification = classifications[1]
        big_classification = classifications[2]
        small_classification = classifications[3]
        print "channel_classification: " + channel_classification
        print "super_big_classification: " + super_big_classification
        print "big_classification: " + big_classification
        print "small_classification: " + small_classification
        continue
    if subitem_key.renderContents() == "捷運資訊".encode('utf-8'):
        mrt_info = re.sub(r'( |\n|\t|&nbsp;)+', r'', remove_html_tags(subitem_val.renderContents().strip('\n')))
        print "mrt_info: " + mrt_info
        continue
    if subitem_key.renderContents() == "公休日".encode('utf-8'):
        official_holiday = remove_html_tags(subitem_val.renderContents().strip('\n'))
        print "official_holiday: " + official_holiday
        continue
    if subitem_key.renderContents() == "補充說明".encode('utf-8'):
        extra_explaination = remove_html_tags(subitem_val.renderContents().strip('\n'))
        print "extra_explaination: " + extra_explaination
        continue
    if subitem_key.renderContents() == "媒體情報".encode('utf-8'):
        media_news = remove_html_tags(subitem_val.renderContents().strip('\n'))
        print "media_news: " + media_news
        continue
    if subitem_key.renderContents() == "媒體推薦".encode('utf-8'):
        media_recommendation = re.sub(r'( |\n|\t|&nbsp;)+', r' ', remove_html_tags(str(subitem_val))).strip()
        print "media_recommendation: " + media_recommendation
        continue
    if subitem_key.renderContents() == "更新時間".encode('utf-8'):
        update_date = remove_html_tags(subitem_val.renderContents().strip('\n'))
        print "update_date: " + update_date
        continue
    if subitem_key.renderContents() == "建立者".encode('utf-8'):
        update_user = remove_html_tags(subitem_val.renderContents().strip('\n'))
        print "update_user: " + update_user
        continue

day_info = []
business_hour_div = soup.find("div",{"class":"business-hour-detail hide"})
if business_hour_div != None:
    print "working_time: "
    business_hour_table = business_hour_div.find("table")
    for item in business_hour_table.findAll("tr"):
        day_info = item.findAll("td")
        day_of_week = remove_html_tags(day_info[0].renderContents().strip('\n'))
        print "day_of_week = " + day_of_week.strip('\n')
        day_working_hour = str(day_info[1].renderContents().strip('\n')).split("br/")
        first_time_slot = re.sub(r'( |<|\r|\n|\t|&nbsp;)+', r'', remove_html_tags(day_working_hour[0]).strip('\n'))
        print "first_time_slot = " + first_time_slot
        second_time_slot = re.sub(r'( |>|\r|\n|\t|&nbsp;)+', r'', remove_html_tags(day_working_hour[1]).strip('\n'))
        print "second_time_slot = " + second_time_slot

rating_data = soup.find("dl",{"class":"rating"})
rating_data_score = rating_data.findAll("dd")
delicious_score = middle(str(rating_data_score[0].find("i")),'<i style="width: ','%"></i>')
service_score = middle(str(rating_data_score[1].find("i")),'<i style="width: ','%"></i>')
atmosphere_score = middle(str(rating_data_score[2].find("i")),'<i style="width: ','%"></i>')
print "delicious_score: " + delicious_score
print "service_score: " + service_score
print "atmosphere_score: " + atmosphere_score

