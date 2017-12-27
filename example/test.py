#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/22 下午4:21
# @Author  : zpy
# @Software: PyCharm

from yspider.spider import BaseSpider, request
from lxml import html as HTML

class TiebaSpider(BaseSpider):

    def req_resp(self):

        @request(retry=3, proxy=True, proxyurl="http://10.10.239.46:8087/proxy?source=pricelineFlight&user=crawler&passwd=spidermiaoji2014")
        def first_page():
            return {
                "request":{
                    'url': 'http://tieba.baidu.com/f?kw=%E5%B1%B1%E8%A5%BF%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=0',
                },
                "response":{
                    "handler": self.parse_data
                }

            }
        return first_page

    def parse_data(self, resp):
        html = resp.content
        res = []
        if html:
            data = HTML.fromstring(html)
            link = None
            title = None
            reqs = None
            author = None
            describe = None
            for i in range(1, 49):
                try:
                    title = data.xpath('//*[@id="thread_list"]/li[{}]/div/div[2]/div[1]/div[1]/a/text()'.format(i))[0]
                    reqs = int(data.xpath('//*[@id="thread_list"]/li[{}]/div/div[1]/span/text()'.format(i))[0])
                    author = data.xpath(
                        '//*[@id="thread_list"]/li[{}]/div/div[2]/div[1]/div[2]/span[1]/span[1]/a/text()'.format(i))[0]
                    describe = \
                    data.xpath('//*[@id="thread_list"]/li[{}]/div/div[2]/div[2]/div[1]/div/text()'.format(i))[0]
                    link = data.xpath('//*[@id="thread_list"]/li[{}]/div/div[2]/div[1]/div[1]/a/@href'.format(i))[0]
                except Exception:
                    print("wtf")
                if title is not None:
                    res.append({
                        "title": title,
                        "reqs": reqs,
                        "author": author,
                        "describe": describe,
                        "link": link,
                    })
        print("result - ", len(res))
        return res


if __name__ == '__main__':
    tieba = TiebaSpider()
    for i in tieba.run():
        print(i)






