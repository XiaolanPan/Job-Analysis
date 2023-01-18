# -*- codeing = utf-8 -*-
# @Time : 2021/5/3 17:07
# @Authon : panxiaolan
# @Sofyware : PyCharm


# 爬取页面信息存储到数据库
import time

from bs4 import BeautifulSoup      # 网页解析,获取数据
import re     # 正则表达式,进行文字匹配
import urllib.request,urllib.error # 制定 url,获取网页数据
# import xlwt   # 进行excel 操作
import sqlite3 # 进行 sqllite 数据库操作

import json


# 中文编码转换
from urllib import parse


# 二次编码
kw = input("请输入你要搜索的岗位关键字:")
keyword = parse.quote(parse.quote(kw))

jobList = [] # 所有的工作岗位信息,放到列表中,每个列表的元素,是上面的元素

def main() :
    # i = 1
    # url ="https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    # getLink(url)
    for i in range(1,2):
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99," + keyword + ",2," + str(i) + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="

        joblink = getLink(url)
        for link in joblink:
            # 获取每一个岗位链接里面的详情
            getData(link)
    #print(jobList)
# 获取网页
def askURL(url):
    # 用户代理,表示告诉豆瓣服务器,我们是什么类型的机器或者浏览器
    head = {
        "User-Agent":"Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 90.04430.93 Safari / 537.36"
    }
    request = urllib.request.Request(url,headers=head)

    html=""

    try:
        response = urllib.request.urlopen(request)
        time.sleep(1)
        html = response.read().decode("gbk")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


# 获取到所有的工作岗位链接
def getLink(url):
    link = askURL(url)
    # 正则表达式拿到解析后的内容
    data = re.findall(r'\"engine_search_result\":(.+?),\"jobid_count\"', str(link))
    # print(data[0])
    jsonObj = json.loads(data[0])
    for item in jsonObj:
        jobList.append({"link":item["job_href"]})
    print(jobList)
    return jobList


# 得到我们需要的数据,将数据保存到数据库中
def getData(linkDetail):
    info = askURL(linkDetail)
    bs = BeautifulSoup(info,"html.parser")



# 将信息保存到数据库中
def saveDB(dataList):
    print("..")

# 初始化数据库
def init_db(dbpath):
    print("..")


if __name__=="__main__":
    main()
