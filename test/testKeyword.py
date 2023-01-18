# -*- codeing = utf-8 -*-
# @Time : 2021/5/4 9:07
# @Authon : panxiaolan
# @Sofyware : PyCharm

# 中文编码转换
from urllib import parse
# 二次编码
keyword = parse.quote(parse.quote("大数据"))

print(keyword)