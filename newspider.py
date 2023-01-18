# -*- codeing = utf-8 -*-
# @Time : 2021/5/3 23:00
# @Authon : panxiaolan
# @Sofyware : PyCharm

import json
from bs4 import BeautifulSoup      # 网页解析,获取数据
import re     # 正则表达式,进行文字匹配
import urllib.request,urllib.error # 制定 url,获取网页数据

import sqlite3 # 进行 sqllite 数据库操作


def askURL(url):
    # 用户代理,表示告诉服务器,我们是什么类型的机器或者浏览器
    head = {
        "User-Agent":"Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 90.04430.93 Safari / 537.36"
    }
    request = urllib.request.Request(url,headers=head)

    html=""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("gbk")
       # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

if __name__=="__main__":
    url = "https://search.51job.com/list/010000,000000,0000,00,9,99,UI,2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    html = askURL(url)
    # 正则表达式拿到解析后的内容
    data = re.findall(r'\"engine_search_result\":(.+?),\"jobid_count\"',str(html))
    print(data[0])
    jsonObj = json.loads(data[0])
    for item in jsonObj:
        print(item['job_href'])
        a = askURL(item['job_href'])
        bs =BeautifulSoup(a,"html.parser")
        da = bs.select('.bmsg.job_msg.inbox>p')
        for value in da:
            # 拿到标签中的内容
            print(value.text)
        print(da)
        break
    #main()