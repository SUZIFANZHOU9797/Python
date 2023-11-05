import re
import os
import time
import random
import requests
import pandas as pd
from fake_useragent import UserAgent

def dd(num):
    url = 'http://bang.dangdang.com/books/childrensbooks/01.41.00.00.00.00-year-2022-0-1-'+str(num)+'-bestsell'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    t = random.randint(3, 6)
    time.sleep(t)
    res = requests.get(url, headers=headers, timeout=120).text

    p_title = '<a href=".*?" target="_blank" title="(.*?)" >.*?</a>'
    p_star = '<span class="level"><span style="width: (.*?)%;">'
    p_comments = '<a href=".*?point=comment_point" target="_blank">(.*?)条评论</a>'
    p_rec = '<span class="tuijian">(.*?)推荐</span>'
    # p_author = '<a href="http://search.dangdang.com/?key=.*?" title="(.*?)" target="_blank">'
    p_time = '</div><div class="publisher_info"><span>(.*?)</span>'
    p_publisher = '<div class="publisher_info"><span>.*?</span>.*?<a href=".*?" target="_blank">(.*?)</a></div>'
    p_price = '<div class="price"><span class="price_n">&yen;(.*?)</span>'
    p_pic = "<div class=.*?>.*?<img src='(.*?)' alt='.*?' />"

    title = re.findall(p_title, res)
    star = re.findall(p_star, res)
    comments = re.findall(p_comments, res)
    rec = re.findall(p_rec, res)
    # author = re.findall(p_author, res)
    publish_time = re.findall(p_time, res)
    publisher = re.findall(p_publisher, res)
    price = re.findall(p_price, res)
    pic = re.findall(p_pic, res)
    for j in range(len(title)):
        pic[j] = pic[j].replace('l_', 'w_')
        cover = requests.get(pic[j], headers=headers, timeout=120)
        time.sleep(t)
        invalid = r"[\/\\\:\*\?\"\<\>\|]"
        title[j] = re.sub(invalid, '', title[j])
        file = open('F://dddd//' + str(20*i+j+1) + '.' + title[j] + '.jpg', 'wb')  # 20*i+j+1
        file.write(cover.content)
        file.close()
    file = pd.DataFrame()
    file['书名'] = title
    file['星级'] = star
    file['评论数'] = comments
    file['推荐度'] = rec
    # file['作者'] = author
    file['出版时间'] = publish_time
    file['出版社'] = publisher
    file['价格'] = price
    return file

file_all = pd.DataFrame(columns=['书名', '星级', '评论数', '推荐度', '出版时间', '出版社', '价格'])
for i in range(25):
    try:
        result = dd(i+1)
        file_all = file_all.append(result)
    except:
        print('第'+str(i+1)+'页打印失败')
file_all.to_excel('F://当当童书top500榜单1111.xlsx', index=False)