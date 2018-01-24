#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/22 下午5:46
# @Author  : zpy
# @Software: PyCharm

import time
from yspider.spider import BaseSpider, request
from lxml import html as HTML
from yspider.logger import logger
from yspider.exceptions import SpiderException
from urllib.parse import quote
import json
from server.jobs.data_model import flight, to_dict
import random
import re
from multiprocessing.pool import ThreadPool as Pool


def convert_date(d):
    """ 20180101 --> 2018-01-01"""
    return '-'.join([d[:4], d[4:6], d[6:8]])

class CsAirSpider(BaseSpider):

    source = 'CsAir'

    def req_resp(self):
        data = {"depcity": 'PEK', "arrcity": 'CDG', "flightdate": '20180302', "adultnum": "1", "childnum": "0",
                    "infantnum": "0", "cabinorder": "0", "airline": "1", "flytype": "0", "international": "1",
                    "action": "0", "segtype": "1", "cache": "0", "preUrl": ""}

        data = self.parse_task(self.task, data)

        @request(retry=3)
        def first_page():
            return {
                "request": {
                    'url': 'https://b2c.csair.com/B2C40/query/jaxb/interDirect/query.ao',
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
        if 'message' in data:
            raise SpiderException(7)
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


class FliggySpider(BaseSpider):

    source = 'Fliggy'

    to_json = re.compile(b'\((.*)\)')

    def req_resp(self):
        @request(retry=3)
        def first_page():
            self.urls = self.parse_task(self.task)
            return {
                "request": {
                    'url': self.urls,
                    'kw': {
                        'headers': {
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0'},
                    }
                },
                "response": {
                    "handler": self.parse_data,
                }

            }

        return first_page

    def parse_task(self, task):

        try:
            dep, arr, date = task.split('&')
        except ValueError:
            raise SpiderException(12, 'check task')

        date = convert_date(date)
        rand = random.randint(3000, 4000)
        _timestamp = str(time.time()).replace('.', '')[:13]

        fex = quote('[{"depCityCode":"%s","arrCityCode":"%s","depDate":"%s"}]' % (dep, arr, date))

        base_url = 'https://sijipiao.fliggy.com/ie/flight_search_result_poller.do?src=filter&_ksTS={}_{}&callback=jsonp' \
                   '{}&supportMultiTrip=true&searchBy=1280&searchJourney='.format(_timestamp, str(rand), str(rand + 1))

        fex2 = '&tripType=0&searchCabinType=0&agentId=-1&searchMode=0&b2g=0&formNo=-1&cardId=&needMemberPrice='

        return base_url+fex+fex2

    def parse_data(self, resp):
        """将数据解析出来"""
        res = []
        resp = resp.content.replace(b'{0:', b'{"0":', 1000) # 替换，变成可以loads的
        data = json.loads(self.to_json.search(resp).group(1))
        try:
            _flights = data['data']['flightItems']
        except:
            raise SpiderException(22, "被封掉了。。。")

        flight.source = self.source
        for f in _flights:
            finfo = f['flightInfo'][0]
            segments = finfo['flightSegments']

            arrs, deps = [ i['arrTimeStr'] for i in segments],[ i['depTimeStr'] for i in segments]
            arrportnames, depportnames = [ i['arrAirportName'] for i in segments],[ i['depAirportName'] for i in segments]
            arrports, depports = [ i['arrAirportCode'] for i in segments],[ i['depAirportCode'] for i in segments]

            flight.deptime, flight.arrtime = finfo['depTimeStr'], finfo['arrTimeStr']
            flight.depdate = flight.deptime[:10]
            flight.arrdate = flight.arrtime[:10]
            flight.datetimes = '|'.join(['_'.join([i,j]) for i, j in zip(arrs, deps)])
            flight.flight_nos = '_'.join([i['marketingFlightNo'] for i in segments])
            flight.seats = finfo.get('cabinClassName', '经济舱')
            flight.ports = '|'.join(['_'.join([i,j]) for i, j in zip(arrports, depports)])
            flight.portnames = '|'.join(['_'.join([i, j]) for i, j in zip(arrportnames, depportnames)])
            flight.price  = f['cardTotalPrice'] // 100

            res.append(to_dict(flight))
        return res

def start(spider):
    return next(spider.run())

def run(task):
    """ test demo, 多线程跑。 响应时间取决于最慢的
    """
    # todo 用更好的方式管理
    s = time.time()
    csair = CsAirSpider()
    csair.task = task
    fliggy = FliggySpider()
    fliggy.task = task
    pool = Pool(4)
    res = pool.map(start, [csair, fliggy])
    print("Cost time", time.time()-s)
    return res

if __name__ == '__main__':
    task = 'BJS&PAR&20180220'
    run(task)