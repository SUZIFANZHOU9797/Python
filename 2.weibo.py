import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
def fetch(max_id):
    url = 'https://weibo.com/ajax/statuses/buildComments'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    params = {'flow': 0,
             'is_reload': 1,
             'id': 4811924297221505,
             'is_show_bulletin': 2,
             'is_mix': 0,
             'max_id': max_id,
             'count': 20,
             'uid': 2803301701}
    res = requests.get(url, headers=headers, params=params)
    return res.json()
# y = fetch()
# print(y)
def parse(y):            #y = fetch()=res.json()
    data = y['data']         #y['data']=res.json()['data']
    max_id = y['max_id']
    comment_all = []
    for item in data:
        name = item['user']['screen_name']
        content = BeautifulSoup(item['text'], 'html.parser').text
        date = item['created_at']
        likes = item['like_counts']
        ip = item['user']['location']
        comment_data = [name, content, date, likes, ip]
        comment_all.append(comment_data)
    return comment_all, max_id
def save(data, path, filename):

    if not os.path.exists(path):
        os.makedirs(path)
    df = pd.DataFrame(data)#data参数
    df.to_csv(path+filename, encoding='utf_8_sig', mode='a', index=False, sep=',', header=False)

if __name__ == '__main__':#注意是两个==
    max_id = 0
    path = 'F:/微博/'
    filename = 'weibo.csv'
    csvHeader = [['用户昵称', '评论内容', '评论时间', '被点赞数', '所在城市']] #列表中的列表
    save(csvHeader, path, filename)#csvheader在这里作为data被写入了pd.DateFrame()
    while(True):
        y = fetch(max_id)
        comment_all, max_id = parse(y)
        save(comment_all, path, filename)
        if max_id == 0:
            break