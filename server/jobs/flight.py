#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/22 下午5:46
# @Author  : zpy
# @Software: PyCharm


from yspider.spider import BaseSpider, request
from lxml import html as HTML
from yspider.logger import logger
from yspider.exceptions import SpiderException
from urllib.parse import quote
import json

class CsAirSpider(BaseSpider):

    def req_resp(self):
        data = {"depcity": 'PEK', "arrcity": 'CDG', "flightdate": '20180302', "adultnum": "1", "childnum": "0",
                    "infantnum": "0", "cabinorder": "0", "airline": "1", "flytype": "0", "international": "1",
                    "action": "0", "segtype": "1", "cache": "0", "preUrl": ""}

        data = self.parse_task(self.task, data)

        @request(retry=3)
        def first_page():
            return {
                "request": {
                    'url': self.urls,
                    'methods': 'post',
                    'postdata': data,
                },
                "response": {
                    "handler": self.parse_data,
                }

            }
        return first_page

    def parse_task(self, task, data):
        try:
            dep, arr, date = task.split('&')
        except ValueError:
            raise SpiderException(12, 'check task')

        data['depcity'] = dep
        data['arrcity'] = arr
        data['flightdate'] = date

        data = 'json=' + quote(json.dumps(data))
        return data

    def parse_data(self, data):
        print('>')
        print(data.content)


if __name__ == '__main__':
    task = 'PEK&CDG&20180220'
    csair = CsAirSpider()
    csair.task = task
    csair.urls = 'https://b2c.csair.com/B2C40/query/jaxb/interDirect/query.ao'
    for i in csair.run():
        print(i)