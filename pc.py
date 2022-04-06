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
    #     url = f'http://www.hngp.gov.cn/henan/search?pageSize=50&ctk={sId}&q=殡&pageNo=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
        'Referer': 'http://www.hngp.gov.cn/henan'
    }

    respm = requests.get(url, cookies=ck, headers=headers)
    # 解析html
    html = etree.HTML(respm.text)
    # 拿到数据的所有li
    lis = html.xpath('/html/body/div[4]/div/div[1]/ul/li')
    # 根据查询关键字自动判断页码总数
    yema = html.xpath("//li[@class='pageInfo']/text()")
    numyema = re.findall("\d+", yema[0])
    numyema = int(numyema[0]) + 1
    # 准备写入csv文件
    filename = str(date.today()) + ".河南省.csv"
    f = open('pachong_data/' + filename, mode='a', encoding='utf-8', newline="")
    csvwriter = csv.writer(f)
    # 遍历每一个li
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


# 普通爬取
# time_start = time.time()
# for i in range(1, 123):
#     try:
#         madata = get_byg_csv(f'http://www.hngp.gov.cn/henan/search?ctk={sId}&q=殡仪馆&pageNo={i}')
#         print(f"第{i}页爬取成功!")
#         time.sleep(2)
#     except Exception as e:
#         print(f"error is {e}")
# print("所有页数爬取成功!")
# time_stop = time.time()
# print(f"爬取完成需要的时间是(秒): {time_stop - time_start} s")


if __name__ == '__main__':
    sId, cookies = get_sid()
    yema = get_byg_csv(f'http://www.hngp.gov.cn/henan/search?pageSize=15&q=焦作市殡仪馆&ctk={sId}&pageNo=1', cookies)
    get_xianc(1, yema, '焦作市殡仪馆')
