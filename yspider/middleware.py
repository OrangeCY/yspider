#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/26 上午10:58
# @Author  : zpy
# @Software: PyCharm

# web --> here --> framework --> response

# 设置请求的url xpath or re ，以及proxy



from collections import namedtuple
from yspider.spider import BaseSpider, request
from lxml import html as HTML

def convert_handle(res_resp):
    """ 从一个namedtuple中获取处理的方法
        约定格式 handler_xxx = re or xpath
    """
    def handler(data):
        xdata = HTML.fromstring(data)
        for r in dir(res_resp):
            i = r.split('_')
            if i[0] == 'handler':
                try:
                    res_resp['result_'+i[1]] = res_resp[r]

    return handler




def generate_func(res_resp):
    """ 传入一个namedtuple 对象，将其转化为请求函数
        Req = namedtuple('name', [retry, url, handler])
        Req.retry = 3
        Req.url = http://xxx
        Req.handler = {
                'xxx': 're or xpath'
            }

    """
    func = {
            "request":{
                "url": res_resp.url,
            },
            "response":{
                "handler": convert_handle(res_resp.handler),
            }
        }
    if not hasattr(res_resp, 'retry'):
        res_resp.retry = 1
    return request(retry=res_resp.retry)(func)





class MiddleSpider(BaseSpider):















