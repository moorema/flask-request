# -*- coding = utf-8 -*-
# @Time : 2022/3/24 20:28
import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import *
import time
import re


def get_sid():
    url = 'http://www.hngp.gov.cn/henan'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
        # 防盗链
        'Referer': url
    }
    resp = requests.get(url, headers=headers)
    cookie = requests.utils.dict_from_cookiejar(resp.cookies)
    sId = cookie['sId']
    return sId, cookie


def get_byg_csv(url, ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
        'Referer': 'http://www.hngp.gov.cn/henan'
    }

    respm = requests.get(url, cookies=ck, headers=headers)
    html = etree.HTML(respm.text)
    lis = html.xpath('/html/body/div[4]/div/div[1]/ul/li')
    yema = html.xpath("//li[@class='pageInfo']/text()")
    numyema = re.findall("\d+", yema[0])
    numyema = int(numyema[0]) + 1
    # 准备写入csv文件
    filename = str(date.today()) + ".河南省.csv"
    f = open('pachong_data/' + filename, mode='a', encoding='utf-8', newline="")
    csvwriter = csv.writer(f)
    for li in lis:
        title = li.xpath('./a/text()')
        gs = li.xpath('./p/span[1]/span/text()')
        timerq = li.xpath('./p/span[2]/text()')
        aurl = li.xpath('./a/@href')

        erurl = 'http://www.hngp.gov.cn' + aurl[0]
        csvwriter.writerow([title[0], gs[0], timerq[0], f'详细连接:{erurl}'])
        print(f'{title} is over!')
    f.close()
    return numyema


def get_xianc(qi, shi, qs):
    with ThreadPoolExecutor(50) as t:
        for i in range(int(qi), int(shi)):
            t.submit(get_byg_csv, f'http://www.hngp.gov.cn/henan/search?pageSize=15&q={qs}&ctk={sId}&pageNo={i}',
                     cookies)
            time.sleep(1)
            print(f"第{i}页爬取完成")




if __name__ == '__main__':
    sId, cookies = get_sid()
    yema = get_byg_csv(f'http://www.hngp.gov.cn/henan/search?pageSize=15&q=焦作市殡仪馆&ctk={sId}&pageNo=1', cookies)
    get_xianc(1, yema, '焦作市殡仪馆')
