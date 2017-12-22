#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/21 下午6:19
# @Author  : zpy
# @Software: PyCharm


from pymongo import MongoClient
from lxml import html as HTML
from multiprocessing.dummy import Pool as ThreadPool
import requests
import time
from yspider.units import simple_get_http_proxy

pool = ThreadPool(2)
session = requests.session()
urls = ['http://yspider.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&pn={}'.format(i*50) for i in range(2001, 3014)]

mongo = MongoClient("mongodb://localhost:27017")
db = mongo.crawl
tieba = db.tieba

def insert_db(data):
    if data:
        tieba.insert_many(data)

def retry(times=3):
    """Retry times"""
    def wrap(func):
        def do(*args, **kwargs):
            t = times
            res = None
            while t > 0:
                try:
                    res = func(*args, **kwargs)
                    break
                except Exception:
                    t -= 1
            return res
        return do
    return wrap


@retry()
def req(url):
    """请求 并将数据拿回来"""
    print("req ", url)
    p = simple_get_http_proxy()
    session.proxies = {
        'http': 'http://' + p,
        'https': 'http://' + p,
    }
    header = {
        # 'Accept-Encoding': 'gzip,deflate, sdch',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,und;q=0.6',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
    }
    time.sleep(3)
    try:
        resp = session.get(url,headers=header, timeout=60)
        return resp.content
    except Exception as e:
        raise parser_except.ParserException(22, "retry !!!")


def parse(html):
    """解析出几个数据"""
    res = []
    print "html-len", len(html)
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
                print "wtf"
            if title is not None:
                res.append({
                    "title": title,
                    "reqs": reqs,
                    "author": author,
                    "describe": describe,
                    "link": link,
                })
    print"result - ", len(res)
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


