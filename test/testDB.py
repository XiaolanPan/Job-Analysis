# -*- codeing = utf-8 -*-
# @Time : 2021/5/3 20:50
# @Authon : panxiaolan
# @Sofyware : PyCharm

import sqlite3


dbpath = "job.db"

maps = {"name": "lisi", "age": 12}

'''
    连接数据库,如果给出的地址中有这个数据库,则连接该数据库,
    如果没有,则在给出的目录中创建该数据库。
    若只给出了数据库的名字,则会在项目的同级目录中创建该数据
    库。

'''
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()

# sql = "insert into tes(name, age) VALUES ('wef',12)"

# cursor.execute(sql)

cursor.execute("insert into tes(name, age) VALUES (?,?)",(maps['name'],maps['age']))

conn.commit()
cursor.close()
conn.close()
