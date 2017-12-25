#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/22 下午4:21
# @Author  : zpy
# @Software: PyCharm

from yspider.spider import BaseSpider


class TiebaSpider(BaseSpider):

    def req_resp(self):
        return {
            "request":{
                'url': 'http://tieba.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&pn=100',
            },
            "response":{
                "handler": self.parse_data
            }

        }

    def parse_data(self, resp):
        print(resp)


if __name__ == '__main__':
    tieba = TiebaSpider()
    tieba.run()






