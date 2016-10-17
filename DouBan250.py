#coding:utf-8
#encoding:utf-8
from lxml import html
from time import sleep
from urllib2 import urlopen
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def show_movie_detail(movie_info):
    director_actor = movie_info[0].split()
    age_country_category = movie_info[1].split()

    director = director_actor[0]+director_actor[1]
    actor = director_actor[4] + director_actor[5]
    age = age_country_category[0]
    country = age_country_category[2]
    category = ""
    for x in range(4,len(age_country_category)):
        category = category+" "+age_country_category[x]

    category = category.lstrip()
    age = "上映时间:"+age.encode('utf-8')
    return  age

def regular_expression(movie_info):
    director_actor = movie_info[0]
    age_country_category = movie_info[1]
    s = unicode(movie_info[0]+movie_info[1])
    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    res = re.findall(re_words,s)
    actor_index = 0
    country_index = 0
    category_index = 0
    catefory_dict = {"犯罪": 0, "剧情": 0, "喜剧": 0, "动作": 0, "动画": 0,
                     "犯罪": 0, "纪录片": 0, "传记": 0, "爱情": 0, "科幻": 0,
                     "奇幻": 0, "冒险": 0}
    actor_name = "主演"
    country_list = ["美国","法国","中国大陆","意大利","日本","印度","香港","英国",
                     "韩国","德国","新西兰","伊朗","澳大利亚","台湾","巴西","丹麦",
                     "博茨瓦纳","爱尔兰","阿根廷","泰国"]
    for x in range(len(res)):
        temp = res[x].encode('utf-8')
        if temp == (actor_name):
            actor_index = x
            #print "actor_index{}".format(actor_index)
        elif temp in country_list and country_index == 0:
            country_index = x
            #print "country_index{}".format(country_index)
        elif temp in catefory_dict and category_index == 0:
            category_index = x
            #print "category_index{}".format(category_index)
            break
    director = ""
    actor = ""
    country = ""
    category = ""
    for x in range(1,actor_index):
        director = director + res[x]+""
    for x in range(actor_index,country_index):
        actor = actor + res[x] + ""
    for x in range(country_index,category_index):
        country = country + res[x] + " "
    for x in range(category_index,len(res)):
        category = category + res[x] + " "
    director = "导演:"+director.encode('utf-8')
    actor = "主演:"+actor[2:].encode('utf-8')
    country = "国家:"+country.encode("utf-8")
    category = "类别:"+category.encode("utf-8")
    return [director,actor,country,category]

def list_append(list_temp,list_object):
    if len(list_temp) > 0:
        list_object.append(list_temp)
    else:
        list_object.append("NULL")

"""        
def find_list_length(list_object):
    max_length = 0
    for x in list_object:
        if len(x) > max_length:
            max_length = len(x)
    return max_length
"""

base_url = "https://movie.douban.com/top250{}"
next_pages = "https://movie.douban.com/top250"

#1. 构建Xpath表达式
next_button_xpath = "//span[@class='next']/a/@href"
movie_xpath = "//ol[@class='grid_view']/li" #该条返回当前页面的所有的值：e.g //ol[@class='grid_view']/li[1]
movie_name_Chinese_xpath = "//ol/li[{}]/div/div/div/a/span[1]/text()"
movie_name_English_xpath = "//ol/li[{}]/div/div/div/a/span[2]/text()"#注意处理字符串，有杂质
movie_info_xpath = "//ol/li[{}]/div/div/div/p[1]/text()" #导演，主演，上映年代，国家，类别---->需要进一步处理
movie_comment_xpath = "//ol/li[{}]/div/div/div/p/span/text()"
movie_ratting_xpath = "//ol/li[{}]/div/div/div/div/span[@class='rating_num']/text()"

movie_name_Chineses = []
movie_name_Englishs = []
movie_comments = []
movie_rattings = []
movie_directors = []
movie_actors = []
movie_ages = []
movie_countrys = []
movie_categorys = []

#2. 开始爬取网页内容
while next_pages:
    dom = html.parse(urlopen(next_pages))
    movies = dom.xpath(movie_xpath)
    for i in range(len(movies)):
        movie_name_Chinese = dom.xpath(movie_name_Chinese_xpath.format(i + 1))
        movie_name_English = dom.xpath(movie_name_English_xpath.format(i + 1))  # 去掉斜线空格
        movie_info = dom.xpath(movie_info_xpath.format(i + 1))
        movie_comment = dom.xpath(movie_comment_xpath.format(i + 1))
        movie_ratting = dom.xpath(movie_ratting_xpath.format(i + 1))
        movie_info_detail = regular_expression(movie_info)
        director = movie_info_detail[0]
        list_append(director,movie_directors)

        actor = movie_info_detail[1]
        list_append(actor,movie_actors)

        country = movie_info_detail[2]
        list_append(country,movie_countrys)

        category = movie_info_detail[3]
        list_append(category,movie_categorys)

        age = show_movie_detail(movie_info)
        list_append(age,movie_ages)

        name_Chinese = "中文名:" + movie_name_Chinese[0].encode('utf-8')
        name_English = "外文名:" + movie_name_English[0][3:].encode('utf-8')
        ratting = "评分:" + movie_ratting[0].encode("utf-8")
        list_append(name_Chinese,movie_name_Chineses)
        list_append(name_English,movie_name_Englishs)
        list_append(ratting,movie_rattings)

        if len(movie_comment) >= 1:
            comment = "热门评论:" + movie_comment[0].encode('utf-8')
            movie_comments.append(comment)
        else:
            movie_comments.append("NULL")
        print ratting
        print director
        print actor
        print age
        print country
        print category
        print "****************************"
    next_page = dom.xpath(next_button_xpath)
    if next_page:
        next_pages = base_url.format(next_page[0])
    else:
        print "No next button found"
        next_pages = None
    print "完成了该网页:{}".format(next_pages)
    #sleep(2)

#3. 准备写文件
with open("/Users/leelom/Desktop/DouBan250.txt",'w') as f:
    length = len(movie_rattings)
    f.write("豆瓣电影TOP250"+"\n")
    f.write("********************************************"+"\n")
    for i in range(length):
        data1 = movie_name_Chineses[i]
        data2 = movie_name_Englishs[i]
        data3 = movie_directors[i]
        data4 = movie_actors[i]
        data5 = movie_rattings[i]
        data6 = movie_ages[i]
        data7 = movie_countrys[i]
        data8 = movie_categorys[i]
        data9 = movie_comments[i]
        f.write(data1 + "\n")
        f.write(data2 + "\n")
        f.write(data3 + "\n")
        f.write(data4 + "\n")
        f.write(data5 + "\n")
        f.write(data6 + "\n")
        f.write(data7 + "\n")
        f.write(data8 + "\n")
        f.write(data9 + "\n")
        f.write("********************************************"+"\n")