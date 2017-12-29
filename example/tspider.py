#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/21 下午6:19
# @Author  : zpy
# @Software: PyCharm

# 从这第一个程序开始，将中间的步骤抽象出来。
# 使用的时候只需要关心如何构造请求 如何解析， 保存数据。



from pymongo import MongoClient
from lxml import html as HTML
from multiprocessing.dummy import Pool as ThreadPool
import requests
import time
from yspider.utils import simple_get_http_proxy, retry
from yspider.exceptions import SpiderException

# db setting
mongo = MongoClient("mongodb://localhost:27017")
db = mongo.crawl
tieba = db.tieba

# task setting
pool = ThreadPool(2)
urls = ['http://yspider.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&pn={}'.format(i*50) for i in range(2001, 3014)]
session = requests.session()


def insert_db(data):
    if data:
        tieba.insert_many(data)



@retry()
def req(url):
    """请求 并将数据拿回来"""
    print("req ", url)
    p = simple_get_http_proxy()
    session.proxies = {
        'http': 'http://' + p,
        'https': 'http://' + p,
    }
    time.sleep(3)
    try:
        resp = session.get(url,headers=header, timeout=60)
        return resp.content
    except Exception as e:
        raise SpiderException(SpiderException.RETRY)


def parse(html):
    """解析出几个数据"""
    res = []
    print("html-len", len(html))
    if html:
        data = HTML.fromstring(html)
        link = None
        title = None
        reqs = None
        author = None
        describe = None
        for i in range(1, 49):
            try:
                title = data.xpath('//*[@id="thread_list"]/li[{}]/div/div[2]/div[1]/div[1]/a/text()'.format(i))[0]
                reqs = int(data.xpath('//*[@id="thread_list"]/li[{}]/div/div[1]/span/text()'.format(i))[0])
                author = data.xpath('//*[@id="thread_list"]/li[{}]/div/div[2]/div[1]/div[2]/span[1]/span[1]/a/text()'.format(i))[0]
                describe = data.xpath('//*[@id="thread_list"]/li[{}]/div/div[2]/div[2]/div[1]/div/text()'.format(i))[0]
                link = data.xpath('//*[@id="thread_list"]/li[{}]/div/div[2]/div[1]/div[1]/a/@href'.format(i))[0]
            except Exception:
                print("wtf")
            if title is not None:
                res.append({
                    "title": title,
                    "reqs": reqs,
                    "author": author,
                    "describe": describe,
                    "link": link,
                })
    print("result - ", len(res))
    return res

def start(url):
    html = req(url)
    pdata = parse(html)
    insert_db(pdata)



if __name__ == '__main__':
    # results = pool.map(start, urls)
    # print results
    for i in urls:
        start(i)


