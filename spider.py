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

jobData = {} # 每一个记录,是一个列表,每个列表中有多个键值对
jobList = [] # 所有的工作岗位信息,放到列表中,每个列表的元素,是上面的元素

dbpath = "job.db"

def main() :
    # i = 1
    # url ="https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    # getLink(url)
    for i in range(9,10):
        time.sleep(1)
        print("第%d页内容正在抓取。。。"%i)
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99," + keyword + ",2," + str(i) + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="

        joblink =  getLink(url)

        for link in joblink:
            s = link[0:23]
            if s != "https://jobs.51job.com/":
                continue
            # if link == "http://campus.51job.com/wicrecend/shezhao.html#131554105" or link == "http://ge.51job.com/sc/jobdetail.html?jobid=129145983":
            #     continue
            # 获取每一个岗位链接里面的详情
            getData(link)
            # break
        for job in jobList:
            print(job)
            # break
        saveDB(jobList)

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
        # time.sleep(1)
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
    links = []
    for item in jsonObj:
        # print(item['job_href'])
        # a = askURL(item['job_href'])
        # bs = BeautifulSoup(a, "html.parser")
        # da = bs.select('.bmsg.job_msg.inbox>p')
        # for value in da:
        #     # 拿到标签中的内容
        #     print(value.text)
        # print(da)

        # 将每个页面的 链接都拿到,之后再解析每个链接后面网页的内容
        links.append(item["job_href"])
        s = item["job_href"][0:23]
        if s != "https://jobs.51job.com/":
            continue
        jobList.append({'link':item["job_href"]})
    # print(jobList)
    # print(jobList)
    return links


# 得到我们需要的数据,将数据保存到数据库中
def getData(linkDetail):
    info = askURL(linkDetail)
    bs = BeautifulSoup(info,"html.parser")
    try:
        for job in jobList:
            if job["link"] == linkDetail:
                # 工作岗位名称
                jname = bs.select(".cn > h1")
                job["jname"] = jname[0].text
                # print(jname[0].text)
                # 公司名称
                cname = bs.select(".catn")
                job["cname"] = cname[0].text
                # print(cname[0].text)
                # 工作地点信息
                addressInfo = bs.select(".msg.ltype")
                address = addressInfo[0].text
                # print(address)
                me = address.split("|")
                # print(me)
                # for message in me:
                #     print(message.strip())

                # 工作地点
                job_address = me[0].strip()
                job["job_address"] = me[0].strip()
                # 工作经验年数
                job_year = me[1].strip()[0:-2]
                job["job_year"] = me[1].strip()[0:-2]
                # print(job_address)
                # print(job_year)
                # 工作学历要求
                job_ins = me[2].strip()
                job["job_ins"] = me[2].strip()
                # 招收人数
                job_num = me[3].strip()
                job["job_num"] = me[3].strip()

                # 薪资
                job_salary = bs.select(".cn > strong")[0].text
                # print(job_salary)
                job["job_salary"] = job_salary

                # 福利
                job_allowance = bs.select(".t1 > span")
                allowance = ""
                for alw in job_allowance:
                    allowance = allowance + alw.text + " "
                # print(allowance)
                job["job_allowance"] = allowance

                # 职能类别
                job_kind = bs.select("a.el.tdn")[0].text
                job["job_kind"] = job_kind
                # 职位信息
                job_info = bs.select(".bmsg.job_msg.inbox")
                i = job_info[0].text.strip().split("\n")
                # print(i[0])
                job["job_info"] = i[0]
                # print(job_info[0].text.strip())
           # print(jobList)
    except UnicodeDecodeError:
        print("..")
    except IndexError:
        print("..")



# 将信息保存到数据库中
def saveDB(jobList):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    for msgList in jobList:
        # sql = '''insert into job_analyse(link,jname,cname,job_address,job_year,job_ins,job_num,job_salary,job_allowance,job_kind,job_info)values('+'msgList['link']'+',msgList['jname'],msgList['cname'],msgList['job_address'],msgList['job_year'],msgList['job_ins'],msgList['job_num'],msgList['job_salary'],msgList['job_allowance'],msgList['job_kind'],msgList['job_info']'''
        # sqlite 占位符进行填充值
        cursor.execute("insert into job_analyse(link,jname,cname,job_address,job_year,job_ins,job_num,job_salary,job_allowance,job_kind,job_info)values(?,?,?,?,?,?,?,?,?,?,?)",(msgList['link'],msgList['jname'],msgList['cname'],msgList['job_address'],msgList['job_year'],msgList['job_ins'],msgList['job_num'],msgList['job_salary'],msgList['job_allowance'],msgList['job_kind'],msgList['job_info']))
        conn.commit()
    cursor.close()
    conn.close()
# 初始化数据库
def init_db(dbpath):

    sql = '''
        create table job_analyse(
            id integer primary key autoincrement,
            link varchar ,
            jname varchar ,
            cname varchar ,
            job_address varchar ,
            job_year numeric ,
            job_ins varchar ,
            job_num varchar ,
            job_salary varchar ,
            job_allowance varchar ,
            job_kind varchar ,
            job_info text 
        )
    '''

    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__=="__main__":
    main()
    # init_db(dbpath)
