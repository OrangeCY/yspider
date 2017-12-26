#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/22 下午4:21
# @Author  : zpy
# @Software: PyCharm

from yspider.spider import BaseSpider, request


class TiebaSpider(BaseSpider):

    def req_resp(self):

        @request(retry=3)
        def first_page():
            return {
                "request":{
                    'url': 'http://tieba.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&pn=100',
                },
                "response":{
                    "handler": self.parse_data
                }

            }
        return first_page

    def parse_data(self, resp):
        print(resp.content)


if __name__ == '__main__':
    tieba = TiebaSpider()
    for i in tieba.run():
        print(i)






