# -*- coding: utf-8 -*-
# @Time    : 2020/7/22 17:51
# @Author  : 周勇吉
# @File    : crawler.py
# @Software: PyCharm
import random
import re
import sqlite3
import time

import requests
from bs4 import BeautifulSoup
import lxml

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.89 Safari/537.36 '
}

database_path = "database.db"  # 数据库路径
total_page = 500  # 爬取页数
list_of_jobs = []  # 招牌信息表


def page_crawler(soup):
    global list_of_jobs
    rough_page = soup.find_all('div', class_='e')  # 职位从下标11到30为需求内容
    jobs_data = rough_page[11:30]
    #print(jobs_data)
    for item in jobs_data:
        # 记录单个招聘的信息,包括职位、公司、地点、学历要求、工作经验、公司性质、公司规模、岗位职责
        detail_of_job = []
        # 职位名称与链接
        detail_of_job.append(item.find('span', class_='title').string)
        detail_of_job.append(item.find('span', class_='title').find('a').get('href'))
        # 公司名称与链接
        detail_of_job.append(item.find('a', class_='name').string)
        detail_of_job.append(item.find('a', class_='name').get('href'))
        # 地点、薪资、日期
        # 取地点大头
        location = item.find_all('span', class_='location name')[0].string
        if re.match(".*(?=-)", location):
            location = re.match(".*(?=-)", location).group()
        detail_of_job.append(location)
        if not item.find_all('span', class_='location')[1].string:  # 薪资可能空缺
            detail_of_job.append("")
        else:
            detail_of_job.append(item.find_all('span', class_='location')[1].string)
        detail_of_job.append(item.find('span', class_='time').string)
        # 学历要求、工作经验、公司性质、公司规模
        job_order = item.find('p', class_='order').get_text().split('|')
        for order in job_order:
            # tmpstr = re.match("(?<=：).*", order)
            # detail_of_job.append(tmpstr.group())
            tmp = order.split("：")
            detail_of_job.append(tmp[1])
        # 职位简介
        detail_of_job.append(item.find('p', class_='text').string.replace("\"", " "))

        # 添加到信息表中
        list_of_jobs.append(detail_of_job)
    # print(list_of_jobs)


# 初始化数据库
def init_database(path):
    sql = "create table jobtable (id INTEGER primary key autoincrement, " \
          "job_name varchar, job_link text, company varchar, company_link text, " \
          "location varchar, charts varchar , post_date varchar , demand varchar, exp varchar, " \
          "company_type varchar, company_size varchar, job_info text)"
    conn = sqlite3.connect(path)  # 连接或创建数据库
    cursor = conn.cursor()  # 获取游标
    cursor.execute(sql)  # 执行SQL语句：创建数据表
    conn.commit()  # 事务提交：让操作生效
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接


# 写入数据到数据库
def write_to_database(file):
    init_database(database_path)
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    for job in file:
        for i in range(len(job)):
            job[i] = ("\"" + job[i] + "\"")
        sql = 'INSERT INTO jobtable(job_name,job_link,company,company_link,location,charts,post_date,demand,exp,company_type,company_size,job_info) VALUES(%s)' % ",".join(
            job)
        print(sql)
        cur.execute(sql)
        con.commit()
    cur.close()
    con.close()


# 主函数
if __name__ == '__main__':

    totaltime = 0
    for page in range(total_page):
        url = "https://jobs.51job.com/houduankaifa/p" + str(page + 1)
        print(url)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        page_crawler(soup)
        totaltime += 1
        print(totaltime, "页")
        # randomtime = random.random() * 3
        # time.sleep(randomtime)
        # totaltime += randomtime
        # print("当前休眠", randomtime, "秒,已爬取", page + 1, "页,共计", (page + 1) * 20, "个信息,已用时", totaltime, "秒\t")
    # print("爬取完毕,共计用时", totaltime)
    write_to_database(list_of_jobs)