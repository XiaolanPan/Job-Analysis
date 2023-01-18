# -*- codeing = utf-8 -*-
# @Time : 2021/5/4 9:19
# @Authon : panxiaolan
# @Sofyware : PyCharm

from bs4 import BeautifulSoup

html = open("detail.html","r")
bs = BeautifulSoup(html,"html.parser")

returnList = bs.select("#tHeader_mkr")
