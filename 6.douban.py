import re
import os
import time
import random
import pandas as pd
from selenium import webdriver

browser = webdriver.Chrome()

def get(num):
    url = 'http://www.douban.com/group/726558/discussion?start='+str(num*25)+'&type=new'
    t = random.randint(3, 6)
    time.sleep(t)
    browser.get(url)
    res = browser.page_source
    return res

def parse(res):
    p_title = '<a href=".*?" title="(.*?)" class="">'
    p_author = '<a href=".*?" class="">(.*?)</a>'
    p_comments = '<td nowrap="nowrap" class="r-count ">(.*?)</td>'
    p_ctime = '<td nowrap="nowrap" class="time">(.*?)</td>'
    p_link = '<a href="(.*?)" title=".*?" class="">'
    title = re.findall(p_title, res)
    author = re.findall(p_author, res)
    comments = re.findall(p_comments, res)
    ctime = re.findall(p_ctime, res)
    link = re.findall(p_link, res)
    print(title, author, comments, ctime, link)
    data = [title, author, comments, ctime, link]
    return data

def save(data, path, filename):
    if not os.path.exists(path):
        os.makedirs(path)
    df = pd.DataFrame(data)
    df = df.T
    df.to_csv(path+filename, encoding='utf_8_sig', index=False, mode='a')

if __name__ == '__main__':
    path = 'F:/douban/'
    filename = 'data.csv'
    header = [['标题'], ['作者'], ['评论数量'], ['评论时间'], ['网页链接']]
    save(header, path, filename)
    for i in range(11, 12):
        res = get(i)
        time.sleep(30)
        # browser.find_element().click()
        # browser.find_element().click()
        # browser.find_element().send_keys()
        # browser.find_element().send_keys()
        # browser.find_element().click()
    for i in range(1, 11):
        try:
            res = get(i)
            data = parse(res)
            otc = save(data, path, filename)
        except:
            print(str(i) + 'error')