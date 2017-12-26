#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/21 下午6:19
# @Author  : zpy
# @Software: PyCharm


from lxml import html as HTML
from multiprocessing.dummy import Pool as ThreadPool
import requests
import time
from yspider.units import simple_get_http_proxy, retry
from yspider.exceptions import SpiderException
from functools import wraps
from collections import deque
from yspider.logger import logger
from requests.exceptions import Timeout



class BaseSpider:
    """ yspider base class , 使用的使用继承这个类。"""
    def __init__(self):
        self.header = {}
        self.result = None

    def req_resp(self):
        pass

    def _req_resp(self):
        pass

    def run(self):
        func = self.req_resp()
        return func.run()

class Browser:
    """ 模拟浏览器, 具体的请求依靠这个类来实现 """

    def __init__(self):
        self.session = requests.Session()
        self.header = {}




def request(retry=3, retry_code=3, proxy=False):
    """ 通过装饰器来给出可选的配置。 """
    def call(func):
        req = ReqParse(func, retry=retry, proxy=proxy)
        return req
    return call




class ReqParse:
    """ 请求和解析处理
        检查请求的格式是否正确，根据写入的请求来处理。
    """

    def __init__(self, func, retry=3, proxy=False, new_session=False, req_length=0, buffer=10, timeout=30):
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

    def parse_func(self):
        """ 放置请求的函数和处理返回的函数
        self._req_func: {
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
        r = self._req_func()
        if 'request' in r and 'response' in r:
            _req = r['request']
            _resp = r['response']
            if 'url' not in _req or 'handler' not in _resp:
                raise SpiderException(SpiderException.FUNCERROR)
            else:
                self.url = _req['url']
                self.handler = _resp['handler']
        else:
            raise SpiderException(SpiderException.FUNCERROR)


    def get_browser(self):
        """ 获取session"""
        b = Browser()
        return b.session

    def _spider_run(self, url):
        """ 控制代理， 超时。。"""
        browser = self.get_browser()
        p = None
        if self.proxy:
            p = simple_get_http_proxy()
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

        try_times = 0
        while True:
            try:
                res = browser.get(url, timeout=self.timeout)
                return res
            except Timeout:
                try_times += 1
                logger.info("重试 ip: {} url:{} 第{}次".format(p, url, try_times))
                if try_times >= self.retry:
                    logger.info("超过重试次数 ip: {} url:".format(p, url))
                    break



    def run(self):
        """ 执行整套流程"""
        res = []
        self.parse_func()
        if isinstance(self.url, str):
            self.url = deque([self.url])
        else:
            self.url = deque(self.url)

        while True:
            u = self.url.popleft()
            logger.info("request url -- : {}".format(u))
            resp = self._spider_run(u)
            if resp is None:
                logger.info("请求 {} 无数据返回".format(u))
            else:
                parsed = self.handler(resp)
                res.append(parsed)
            if len(res) >= self.buffer:
                yield res
                res = []
            if len(self.url) == 0:
                return res

        # todo : 获取更深的链接，加入执行。









if __name__ == '__main__':
    # results = pool.map(start, urls)
    # print results
    # for i in urls:
    #     start(i)
    test(10)

