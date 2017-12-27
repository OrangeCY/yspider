#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/22 下午4:21
# @Author  : zpy
# @Software: PyCharm

from yspider.spider import BaseSpider, request
from lxml import html as HTML
from yspider.logger import logger
from yspider.units import init_db
from urllib.parse import quote

class TiebaSpider(BaseSpider):


    def req_resp(self):

        @request(retry=3, proxy=True,
                 )
        def first_page():
            return {
                "request":{
                    'url': self.urls,
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
                    pass
                if title is not None:
                    res.append({
                        "title": title,
                        "reqs": reqs,
                        "author": author,
                        "describe": describe,
                        "link": link,
                    })
        logger.info("解析成功 {}/48".format(len(res)))

        return res

def generate_url(name, num):
    name = quote(name)
    return ['http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(name, i * 50) for i in range(num)]


collection = init_db(coll='山西大学')

def insert_db(data):
    if data:
        logger.info("Insert db : {}".format(len(data)))
        collection.insert_many(data)


def main(urls):
    tieba = TiebaSpider()
    tieba.urls = urls
    for i in tieba.run():
        insert_db(i)



if __name__ == '__main__':
    from multiprocessing.pool import ThreadPool as Pool
    import time
    pool = Pool(8)
    urls = generate_url('山西大学', 100)
    start = time.time()
    pool.map(main, urls)








