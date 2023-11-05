# -*- coding: utf-8 -*-

import os
import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


headers = {'User-Agent': str(UserAgent().random),
           'cookie': '_zap=7c4ad76e-20ca-47c4-a26c-17547630185d; d_c0=AFBTLRgPjxWPTvemIC4lsUJvVYWNoKKnwoc=|1663157777; __snaker__id=Wz2OcmmLbHuodKTf; _9755xjdesxxd_=32; YD00517437729195:WM_TID=r6yHQW7ZPpBEVVARFVLFGh7P6KOfzW9l; q_c1=d8863e3b26d146d0aa8343ed246c7262|1663157786000|1663157786000; YD00517437729195:WM_NI=jkreJ9EhpLEC4fuJa9L0/Ra2Pb76a3rTE/vhWfTudqbknZze2o9UpqpSD5Z99XKfJLxcogedorw6O7sIEQGjOXwYBBtS233InyPY3pBiL5tToDZfR1GK9trzJ+x/2Zu+ZkQ=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6ee89fc5f928a97b6b57bb7968aa2c44b969e9eadd84393a6aed0eb4fbce9aab4f52af0fea7c3b92aaab5be86c93387b8c0adc849f8babbabe43390f0e1b3e43a94bef9d7e439b28c8bd0f56495ba9c96e77ba2b5a2bbf96ff2b1f7b6f37bb48d8cd6d933fb888587c948bcbda188e870adaeb9d7ce3db1978bb2c6628d88b9bac14ab88dfed4b243aea7a0bab27c82b784d6f760ad9c9687d13b8595f795f1728af5b8d0b152b7f5968cd437e2a3; _xsrf=7SUPSZzuPIsNw1kFHyWHnkpxDZwBahSV; q_c1=d8863e3b26d146d0aa8343ed246c7262|1679451588000|1663157786000; __utma=51854390.1318917439.1679451591.1679451591.1679451591.1; __utmz=51854390.1679451591.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/63014725; __utmv=51854390.100--|2=registration_date=20171218=1^3=entry_date=20171218=1; z_c0=2|1:0|10:1681694304|4:z_c0|80:MS4xdWQzd0JnQUFBQUFtQUFBQVlBSlZUVDhTSm1XMFhvcDk3X2dtNjQ3UjB3Z3BzMXdFcENMd0tRPT0=|796b4863eaccfda0b101d78691101a057947978d3f1b7adcfcd494f9d5c2b57a; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1681820678,1681865904,1681903826,1681956665; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1681956673; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1681956693|1681956662'}

def fetch(url):
    reconnect = 0
    while reconnect < 4:
        try:
            res = requests.get(url, headers=headers, timeout=120)
            res.encoding = 'utf-8'
            html = res.text
            info = json.loads(html)
            return info
        except (requests.exceptions.RequestException, ValueError):
            time.sleep(200)
            print('except中')
            reconnect += 1
    return '3次都没连上？给你机会，你不中用啊！！！'

def parse(info):
    url = info['paging']['next']
    otc = info.get('data')
    all_in = []
    for i in otc:
        author = i['target']['author']['name']
        likes = i['target']['voteup_count']
        answer = BeautifulSoup(i['target']['content'], 'html.parser').text
        genders = i['target']['author']['gender']
        comments = i['target']['comment_count']
        timestamp = i['target']['created_time']
        time_object = time.localtime(timestamp)
        time_str = time.strftime('%Y-%m-%d', time_object)
        date = time_str
        print(author, answer, likes, comments, date, genders)
        summary = [author, answer, likes, comments, date, genders]
        all_in.append(summary)
    return url, all_in

def save(path, filename, data):

    if not os.path.exists(path):
        os.makedirs(path)
    df = pd.DataFrame(data)
    df.to_csv(path+filename, encoding='utf_8_sig', mode='a', index=False, header=False)

if __name__ == '__main__':
    url = 'https://www.zhihu.com/api/v4/questions/63014725/feeds?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&offset=0&limit=5&order=updated'
    path = 'F://知乎//'
    filename = 'zhihu.csv'
    csvHeader = [['用户昵称', '回答内容', '点赞数', '评论数', '发布日期', '性别']]
    save(path, filename, csvHeader)
    while True:
        y = fetch(url)
        url, all_in = parse(y)
        save(path, filename, all_in)
        if url == 0:
            break