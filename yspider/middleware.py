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
from pprint import pprint
from yspider.logger import logger

def convert_handle(res_resp):
    """ 从一个namedtuple中获取处理的方法
        约定格式 handler_xxx = re or xpath
    """
    def handler(data):
        """ 三种类型的 html json xpath"""
        data = data.content
        xdata = HTML.fromstring(data)
        for r in dir(res_resp):
            i = r.split('_')
            if i[0] == 'handler':
                try: # 先只考虑xpath的
                    name = 'result_' + i[1]
                    _res = "_".join(xdata.xpath(getattr(res_resp, r)))
                    pprint(_res)
                    setattr(res_resp, name, _res)
                except Exception as e:
                    logger.info('parse handler -- {}'.format(e))
                    setattr(res_resp, name, None)
        return res_resp

    return handler




def generate_func(res_resp):
    pass





class MiddleSpider(BaseSpider):

    def __init__(self, res_resp):
        super(MiddleSpider, self).__init__()
        self.res_resp = res_resp

    def req_resp(self):
        """ 传入一个namedtuple 对象，将其转化为请求函数
                Req = namedtuple('name', [retry, url, handler])
                Req.retry = 3
                Req.url = http://xxx
                Req.handler = {
                        'xxx': 're or xpath'
                    }

            """
        res_resp = self.res_resp
        def func():
            page_parse = {
                "request": {
                    "url": res_resp.url,
                },
                "response": {
                    "handler": convert_handle(res_resp),
                }
            }
            return page_parse
        if not hasattr(res_resp, 'retry'):
            res_resp.retry = 10
        return request(retry=res_resp.retry)(func)


if __name__ == '__main__':
    tieba = namedtuple('tieba', ['url', 'handler_x'])
    tieba.url = 'http://tieba.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&ie=utf-8&pn=500'
    tieba.handler_url = '//*[@id="thread_list"]/li[{}]/div/div[2]/div[1]/div[1]/a/@href/text()'
    s = MiddleSpider(tieba)
    for i in s.run():
        print(i)













