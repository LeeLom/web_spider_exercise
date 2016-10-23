# coding:utf-8
import requests
import re
from time import sleep
import sys
import codecs

reload(sys)

sys.setdefaultencoding('utf-8')#文本输出不乱码

#获得网页信息
def get_page(url):
    print url
    page = requests.get(url, headers=headers, cookies=cookies)
    return page

#利用正则匹配
def get_info(page):
    re_rext = '"albummid":"(.*?)".*?interval":(.*?),.*?"name":"(.*?)".*?songname":"(.*?)".*?in_count":"(.*?)"'
    pattern = re.compile(re_rext)
    match = pattern.findall(page)
    if match:
        for xx in match:
            song_pic.append(xx[0])
            song_time.append(xx[1])
            song_singer.append(xx[2])
            song_name.append(xx[3])
            song_rate.append(xx[4])
    sleep(1.5)
    return [song_pic,song_time,song_singer,song_name,song_rate]

#将小数转为与之对应的百分数
def get_up_number(num):
    num = num[0:4]
    if num[0] == '0':
        num = num[2:4]
        if num[0] != '0':
            return num[0]+num[1]+"%"
        else:
            return num[1] + "%"
    else:
        return num[0]+num[2]+num[3]+"%"

#将秒转为与之对应的分钟
def get_time_in_minute(num):
    minute = int(num) / 60
    seconds = int(num) % 60
    if seconds < 10:
        return "0" + str(minute) + ":0" + str(seconds)
    else:
        return "0" + str(minute) + ":" + str(seconds)

cookies = {
    'pac_uid': '1_771704330',
    'tvfe_boss_uuid': '912d00888269850f',
    'eas_sid': 'Z1g4Q7k4e9Z864D3v6z9Q9j1p0',
    'ptui_loginuin': '771704330',
    'ptcz': 'd77dc48e732e1468919e5db7d33d73b3665605d8ec362c6337cf87817530053a',
    'pt2gguin': 'o0771704330',
    'pgv_pvi': '3190138880',
    'pgv_pvid': '8032537030',
    'o_cookie': '771704330',
    'pgv_si': 's9943211008',
    'ts_refer': 'www.google.com/',
    'ts_last': 'y.qq.com/portal/toplist/4.html',
    'ts_uid': '151718640',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://y.qq.com/portal/toplist/4.html',
    'Connection': 'keep-alive',
}

url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2016-10-21&topid=4&type=top&song_begin={}&song_num=30&g_tk=938407465&jsonpCallback=MusicJsonCallbacktoplist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
url_num = ["0","30","60","90"]
pic_url = "https://y.gtimg.cn/music/photo_new/T002R150x150M000{}.jpg?max_age=2592000"

song_pic = list()
song_time = list()
song_singer = list()
song_name = list()
song_rate = list()

#1. 获得网页信息
for num in url_num:
    page = get_page(url.format(num))
    get_info(page.text)

#2. 写入文本文件
with open("/Users/leelom/Desktop/Ajax_QQMusic.txt",'w') as f:
    f.write(codecs.BOM_UTF8)#添加此行可以让输出的文本文件用Sarifi打开不乱码
    f.write("QQ音乐巅峰榜单"+"\n")
    f.write("*********************************************************************************" + "\n")
    for i in range(len(song_name)):
        f.write("第{}名".format(i + 1) + "\n")
        f.write("歌曲名:{}".format(song_name[i]) + "\n")
        f.write("歌手:{}".format(song_singer[i]) + "\n")
        f.write("飙升指数:{}".format(get_up_number(song_rate[i])) + "\n")
        f.write("歌曲长度:{}".format(get_time_in_minute(song_time[i])) + "\n")
        f.write("图片链接:{}".format(pic_url.format(song_pic[i])) + "\n")
        f.write("*********************************************************************************" + "\n")

print "End"
