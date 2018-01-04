#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/4 下午4:29
# @Author  : zpy
# @Software: PyCharm

import json

from flask_rq import job

from web.server import convert
from yspider.middleware import MiddleSpider


@job
def _spider(data):
    res = []
    n = convert(data)
    task = MiddleSpider(n)
    for t in task.run():
        res.extend(t)
    return json.dumps(res)

def job_spider(data):
    return _spider.delay(data)


@job
def _slow_fib(n):
    if n <= 1:
        return 1
    else:
        return _slow_fib(n-1) + _slow_fib(n-2)



def slow_fib(n):
    return _slow_fib.delay(n)


