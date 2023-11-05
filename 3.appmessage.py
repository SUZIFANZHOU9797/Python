import time
import random
import requests
import pandas as pd

def fetch(num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&createType=0&token=1334340470&lang=zh_CN',
        'cookie': 'appmsglist_action_3863549827=card; pgv_pvid=7415059910; RK=MHF0B13Eml; ptcz=59196f88c9c38017de8b016fddf990c85df36b51e3ceb421fe8558b1ade956a5; ua_id=2uFOPJCW8Sa1VMAtAAAAAD_0xNhaOy_ugxEErHtZ-RI=; wxuin=64551298759064; mm_lang=zh_CN; pac_uid=0_10633b6c7d1d8; _clck=3863549827|1|f6t|0; tvfe_boss_uuid=a1150656daddc62d; rewardsn=; wxtokenkey=777; uuid=b4ad1f37d88b4b0f67f95290b1649a93; rand_info=CAESIEfKONkUHK6mRsfDzjtpm1OTXuxAG7NV9nLkQ7cqDomI; slave_bizuin=3863549827; data_bizuin=3863549827; bizuin=3863549827; data_ticket=QFobv4UEAUyzBATFjFvDljPYUYXFkRxLUz4jhp0vHvWa0xWMOPUD5KNUHHY4d2T6; slave_sid=YjRTajZhM2xSZE8zOWdKUGJFc1RIT3JvdjlNYzZYSXVUb2oyOUdRaEttdlhjbmpvWGlBbThiTkJjTUxOMWF1cmVJOHpVSXNMM003bzhha0xjdXFJZ2pfR0hoQ3AydnU1NDlJWDFNRTJ1WGpKN0k4dk92dHRKaU51NFUybk1iSm1hRlRSaUdxYmlIOVhjTzBL; slave_user=gh_66ebaddd3626; xid=a42ba903d15be9d9c6fda7edaabbf4a4'}
    params = {'action': 'list_ex',
              'fakeid': 'Mzg5MTM5ODU2Mg==',
              'query': '',
              'begin': '0',
              'count': '(num-1)*5',
              'type': '9',
              'need_author_name': '1',
              'token': '1334340470',
              'lang': 'zh_CN',
              'f': 'json',
              'ajax': '1'}
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin='+str((num-1)*5)+'&count=5&fakeid=Mzg5MTM5ODU2Mg==&type=9&query=&token=1334340470&lang=zh_CN&f=json&ajax=1'
    res = requests.get(url, headers=headers, params=params).json()
    t = random.randint(10, 12)
    time.sleep(t)
    list = res.get('app_msg_list')
    file = pd.DataFrame()
    title = []
    link = []
    date = []
    for i in list:
        timestamp = i['create_time']
        timeobject = time.localtime(timestamp)
        timestr = time.strftime('%Y-%m-%d %H:%M', timeobject)
        title.append(i['title'])
        link.append(i['link'])
        date.append(timestr)
    #                                                                   DataFrame可以通过列表、字典或二维数组创建 ！！！
    print(title, link, date)
    file['标题'] = title
    file['链接'] = link
    file['日期'] = date
    return file

file_all = pd.DataFrame()
for k in range(41, 47):
    try:
        result = fetch(k)
        file_all = file_all.append(result)
    except:
        print('第'+str(k-1)+'页爬取失败！！！')
file_all.to_csv('F://Eastmount.csv', encoding='utf_8_sig', mode='a', index=False, sep=',', header=True)