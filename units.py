#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/21 下午6:55
# @Author  : zpy
# @Software: PyCharm

import requests

def simple_get_http_proxy():
    r = requests.get('http://10.10.239.46:8087/proxy?user=crawler&passwd=spidermiaoji2014&source={0}'.
                     format('testHttpProxyOnly'))
    proxy = r.content.decode()
    print(proxy)
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
                except Exception:
                    t -= 1
            return res
        return do
    return wrap


if __name__ == '__main__':
    simple_get_http_proxy()