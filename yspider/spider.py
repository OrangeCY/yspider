#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/21 下午6:19
# @Author  : zpy
# @Software: PyCharm

from lxml import html as HTML
from multiprocessing.dummy import Pool as ThreadPool
import requests
import time
from yspider.units import simple_get_http_proxy, func_time_log, split_task
from yspider.exceptions import SpiderException
from functools import wraps
from collections import deque
from yspider.logger import logger
from requests.exceptions import Timeout
from multiprocessing.pool import ThreadPool as Pool
from pymongo import MongoClient

class BaseSpider:
    """ yspider base class , 使用的使用继承这个类。"""
    collection = None
    def __init__(self):
        self.header = {}
        self.result = None
        self.urls = []

    def req_resp(self):
        pass

    def _req_resp(self):
        pass

    def set_db(self,client="mongodb://localhost:27017", db="crawl", coll='crawl'):
        """初始化mongodb"""
        mongo = MongoClient(client)
        db = mongo[db]
        collection = db[coll]
        self.collection = collection

    def run(self):
        func = self.req_resp()
        return func.run()



class Browser:
    """ 模拟浏览器, 具体的请求依靠这个类来实现 """

    def __init__(self):
        self.session = requests.Session()
        self.header = {}


def request(retry=3, retry_code=3, proxy=False, proxyurl=None, buffer=10, concurren=1):
    """ 通过装饰器来给出可选的配置。 """
    def call(func):
        req = ReqParse(func, retry=retry, proxy=proxy, proxyurl=proxyurl, buffer=buffer, concurren=concurren)
        return req
    return call


class ReqParse:
    """ 请求和解析处理
        检查请求的格式是否正确，根据写入的请求来处理。
    """
    def __init__(self, func, retry=3, proxy=False, new_session=False, concurren=1,
                 req_length=0, buffer=10, timeout=30, proxyurl=None):
        """

        :param func: 传入的函数，包含请求信息 和 解析函数
        :param retry: 重试次数
        :param proxy: 代理
        :param new_session: 启用新会话？
        :param req_length: 最小的返回长度，小于这个直接判定位请求失败
        :param buffer:  当前要buffer的解析完成的数据的数量
        :param timeout: 请求超时时间
        """
        self._req_func = func
        self.retry = retry
        self.proxy = proxy
        self.new_session = new_session
        self.req_length = req_length
        self.buffer = buffer
        self.timeout = timeout
        self.proxyurl = proxyurl
        self.concurren = concurren


    def parse_func(self):
        """ 放置请求的函数和处理返回的函数
        self._req_func: {
            "request":{
                "url": http://xxxx,
                "header": xxx,
                ...
            }
            "response":{
                "handler": xxx,  # handler最后返回 dict list（一般用在列表页） str
            }
        }
        """
        r = self._req_func()
        if 'request' in r and 'response' in r:
            _req = r['request']
            _resp = r['response']
            if 'url' not in _req or 'handler' not in _resp:
                raise SpiderException(SpiderException.FUNCERROR)
            else:
                self.urls = _req['url']
                self.handler = func_time_log(_resp['handler'])
                self.insert = func_time_log(_resp['insert'])
        else:
            raise SpiderException(SpiderException.FUNCERROR)


    def get_browser(self):
        """ 获取session"""
        b = Browser()
        self.set_proxy(b)
        return b.session


    def set_proxy(self, browser):
        if self.proxy:
            p = simple_get_http_proxy(self.proxyurl)
            if p.startswith('10'): # 内网转发用socks5
                browser.proxies = {
                    'http': 'socks5://' + p,
                    'https': 'socks5://' + p
                }
            else:
                browser.proxies = {
                    'http': 'http://' + p,
                    'https': 'http://' + p,
                }
            logger.info("使用代理: [%s]" %(p))

    @func_time_log
    def _spider_run(self, url):
        """ 执行真正的请求。控制代理， 超时等设置。。"""
        browser = self.get_browser()
        p = None


        try_times = 0
        while True:
            try:
                resp = browser.get(url, timeout=self.timeout)
                time.sleep(0.1)
                logger.info("请求URL--> {}".format(url))
                return resp
            except Timeout:
                try_times += 1
                # self.set_proxy(b) # 换 ip。。
                logger.info("重试 ip: {} url:{} 第{}次".format(p, url, try_times))
                if try_times >= self.retry:
                    logger.info("超过重试次数 ip: {} url:".format(p, url))
                    break


    def _con_run(self, urls):
        """
        执行整套流程

        test = TestSpider()
        for i in test.run():
            print(i)         # result
        :param urls:
        :return:
        """

        res = []
        if self.buffer <= 0:
            self.buffer = 1

        if isinstance(urls, str):
            urls = deque([urls])
        else:
            urls = deque(urls)

        while True:
            for _ in range(self.buffer):
                u = urls.popleft()
                resp = self._spider_run(u)
                if resp is None:
                    logger.info("请求 {} 无数据返回".format(u))
                else:
                    parsed = self.handler(resp) # handler函数最后可能返回 list str dict
                    if isinstance(parsed, list):
                        res.extend(parsed)
                    else:
                        res.append(parsed)          # 在这里最后返回一层的列表
                if len(urls) == 0:
                    yield res
                    self.get_browser().close() # 释放链接
                    return
            yield res
            res = []

    def fk(self, urls):
        for i in self._con_run(urls):
            self.insert(i)


    def run(self):
        """


        """

        self.parse_func() # 将targets_request中的参数解析出来 url handler

        if self.concurren > 1:
            pool = Pool(self.concurren)
            urls = split_task(self.urls, self.concurren)
            return pool.map(self.fk, urls)  # 这里的每个对象是一个生成器。。 为了和下面同步，直接在这一步执行
        else:
            return self._con_run(self.urls)






        # todo : 获取更深的链接，加入执行。

if __name__ == '__main__':
    # results = pool.map(start, urls)
    # print results
    # for i in urls:
    #     start(i)
    test(10)

