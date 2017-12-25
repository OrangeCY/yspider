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
from yspider.units import simple_get_http_proxy, retry
from yspider.exceptions import SpiderException

pool = ThreadPool(2)
session = requests.session()
urls = ['http://yspider.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&pn={}'.format(i*50) for i in range(2001, 3014)]

mongo = MongoClient("mongodb://localhost:27017")
db = mongo.crawl
tieba = db.tieba


class BaseSpider:
    """ yspider base class , 使用的使用继承这个类。"""
    def __init__(self):
        self.session = requests.Session()
        self.header = {}
        self.result = None

    def req_resp(self):
        """ 放置请求的函数和 处理返回的函数
        ex: {
            "request":{
                "url": http://xxxx,
                "header": xxx,
                ...
            }
            "response":{
                "handler": xxx,
            }
        }
        """
        pass

    def _req_resp(self):
        spider_info = self.req_resp()
        req = spider_info.get('request', '')
        if not req:
            raise SpiderException(SpiderException.TASKERROR)
        url = req.get('url', '')
        if not url:
            raise SpiderException(SpiderException.TASKERROR)
        header = req.get('header', {})
        handler = spider_info['response']['handler']
        print(url)
        resp = self.session.get(url, headers=header)

        self.result = handler(resp)

    def run(self):
        self._req_resp()



@retry()
def test(x):
    print(x)
    for i in range(x):
        if i == 3:
            raise SpiderException(3)




if __name__ == '__main__':
    # results = pool.map(start, urls)
    # print results
    # for i in urls:
    #     start(i)
    test(10)

