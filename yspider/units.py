#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/21 下午6:55
# @Author  : zpy
# @Software: PyCharm

import requests
import os

def simple_get_http_proxy(url=None):
    """获取proxy"""
    if url is None:
        url = os.environ['proxyurl']
    r = requests.get(url)
    proxy = r.content.decode()
    return proxy

def retry(times=3):
    """Retry times"""
    def wrap(func):
        def do(*args, **kwargs):
            t = times
            res = None
            while t > 0:
                try:
                    res = func(*args, **kwargs)
                    break
                except Exception as e:
                    if e.code == 3:
                        t -= 1
                    else:
                        t -= t
            return res
        return do
    return wrap


if __name__ == '__main__':
    simple_get_http_proxy()