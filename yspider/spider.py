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



class BaseSpider:
    """ yspider base class , 使用的使用继承这个类。"""
    def __init__(self):
        self.header = {}
        self.result = None

    def req_resp(self):
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

class Browser:
    """ 模拟浏览器, 具体的请求依靠这个类来实现 """

    def __init__(self):
        self.session = requests.Session()
        self.header = {}




def request(retry=3, retry_code=3):
    """ 通过装饰器来给出可选的配置。 """
    pass




class ReqParse:
    """ 请求和解析处理
        检查请求的格式是否正确，根据写入的请求来处理。
    """

    def __init__(self, func, retry=3, proxy=False, new_session=False, req_length=0):
        self._req_func = func
        self.retry = retry
        self.proxy = proxy
        self.new_session = new_session
        self.req_length = req_length

    def parse_func(self):
        """ 放置请求的函数和 处理返回的函数
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
        b = Browser()
        return b.session

    def run(self):
        res = []
        self.parse_func()
        self.url = deque(self.url)
        browser = self.get_browser()
        while True:
            u = self.url.popleft()
            resp = browser.get(u)
            parsed = self.handler(resp)
            res.append(parsed)
            yield res
        # todo : 获取更深的链接，加入执行。




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

