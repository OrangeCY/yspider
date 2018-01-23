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
from server.jobs.data_model import flight, to_dict


def convert_date(d):
    """ 20180101 --> 2018-01-01"""
    return '-'.join([d[:4], d[4:6], d[6:8]])

class CsAirSpider(BaseSpider):

    source = 'CsAir'

    def __init__(self, task):
        super().__init__()
        self.task = task

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

    def get_portname(self, k, ports):
        for port in ports:
            if k in port.values():
                return port['zhName']

    def parse_data(self, data):
        res = []
        data = json.loads(data.content)
        dateflights = data['segment'][0]['dateflight']
        airports = data['airports']
        for f in dateflights:
            _flight = f['flight']
            _prices = f['prices']
            flight.source = self.source

            flight.deptime, flight.arrtime = _flight[0]['deptime'], _flight[-1]['arrtime']
            flight.flight_nos = '_'.join([i['flightNo'] for i in _flight])
            flight.depdate = flight.deptime[:10]
            flight.arrdate = flight.arrtime[:10]
            flight.datetimes = '|'.join(['_'.join([i['deptime'], i['arrtime']]) for i in _flight])
            flight.portnames = '|'.join(['_'.join([self.get_portname(i['depport'], airports),  # 先获取port 再获取portname 再组合
                                                   self.get_portname(i['arrport'], airports)]) for i in _flight])
            flight.ports = '|'.join(['_'.join([i['depport'], i['arrport']]) for i in _flight])
            for p in _prices:
                flight.price = p['adultprice']
                flight.seats = '_'.join([i['type'] for i in p['adultcabins']])
                res.append(to_dict(flight))
        return res


if __name__ == '__main__':
    task = 'PEK&CDG&20180220'
    csair = CsAirSpider(task)
    csair.task = task
    csair.urls = 'https://b2c.csair.com/B2C40/query/jaxb/interDirect/query.ao'
    for i in csair.run():
        print(i)