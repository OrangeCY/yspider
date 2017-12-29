#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/21 下午6:55
# @Author  : zpy
# @Software: PyCharm

import requests
import os
from pymongo import MongoClient
from yspider.logger import logger
import time
from functools import wraps

def func_time_log(func):
    """记录运行时间, 只保存两位小数字"""
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        logger.info("function name［%s］ run %.2f s" % (func.__name__, time.time()-start))
        return res
    return wrap


def simple_get_http_proxy(url=None):
    """获取proxy"""
    if url is None:
        url = os.environ['proxyurl']
    r = requests.get(url)
    proxy = r.content.decode()
    return proxy

def retry(times=3, code=3):
    """如果抛错，重试"""
    def wrap(func):
        def do(*args, **kwargs):
            t = times
            res = None
            while t > 0:
                try:
                    res = func(*args, **kwargs)
                    break
                except Exception as e:
                    if e.code == code:
                        t -= 1
                    else:
                        t -= t
            return res
        return do
    return wrap

def init_db(client="mongodb://localhost:27017", db="crawl", coll='crawl'):
    """初始化mongodb"""
    mongo = MongoClient(client)
    db = mongo[db]
    collection = db[coll]
    return collection

def split_task(task, num):
    """[1,2,3,4,5,6] , 3   [[1,2],[3,4],[5,6]]"""
    lent = len(task)
    num = lent//num
    res = []
    l = 0
    while l < lent:
        res.append(task[l: l+num])
        l += num
    return res

##  test units function

@func_time_log
def func_time_test():
    time.sleep(0.001)

if __name__ == '__main__':
    # simple_get_http_proxy()


    # func_time_test()
    print(split_task(list(range(100)), 7))