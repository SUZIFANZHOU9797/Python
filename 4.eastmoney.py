import os
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)

df = pd.read_csv('F:/eastmoney/hs300_plus.csv', usecols=['链接'], squeeze=True)
# print(df.head())
links = df.tolist()
links = links[1:5]  # 在这里修改爬取的范围 ！！！
print(links)
#
def get(i):
    url = i
    browser.get(url)
    t = random.randint(3, 5)
    time.sleep(t)
    res = browser.page_source
    return res

def parse(res):
    soup = BeautifulSoup(res, 'html.parser')
    title = soup.select('.newstitle')
    author = soup.select('.newsauthor .name')
    date = soup.select('.time')
    content = soup.select('.newstext')
    data = []
    for i in range(1):
        row = [title[i].text, author[i].text, date[i].text, content[i].text]
        data.append(row) # 通过嵌套列表创建df [[小明, 18],[小红, 20]]
    print(data)
    return data

def save(data, path, filename):
    if not os.path.exists(path):
        os.makedirs(path)
    df = pd.DataFrame(data)
    df.to_csv(path+filename, encoding='utf_8_sig', mode='a', index=False, header=False)

if __name__ == '__main__':
    path = 'F:/eastmoney/'
    filename = 'post.csv'
    Header = [['标题', '作者', '发布时间', '正文内容']]
    save(Header, path, filename)
    for i in links:
        try:
            res = get(i)
            data = parse(res)
            otc = save(data, path, filename)
        except:
            print(str(i)+'error')
