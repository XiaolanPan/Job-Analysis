# -*- codeing = utf-8 -*-
# @Time : 2021/5/3 10:39
# @Authon : panxiaolan
# @Sofyware : PyCharm

# import jieba  # 分词

# from matplotlip import pyplot as plt # 绘图,数据可视化
# from wordcloud import Wordcloud      # 词云
# from PIL import  Image               # 图片处理
# import numpy as np                   # 矩阵运算

import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np

import sqlite3

# 准备词云所需的文字
con = sqlite3.connect('job.db')
cur = con.cursor()
sql = 'select job_allowance from job_analyse'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
    # print(item[0])
print(text)
cur.close()
con.close()

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)

print(string)
print(len(string))


img = Image.open(r'.\static\img\word.jpg')
img_array = np.array(img) # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path='msyh.ttc'
)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off') #是否显示坐标轴

# plt.show()  # 显示生成的词云图片

# 输出词云图片到文件
plt.savefig(r'.\static\img\allowance.jpg',dpi=500)