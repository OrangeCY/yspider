#!/usr/bin/env python
# @Author  : pengyun

from collections import namedtuple

def convert(d):
    """ web请求 --》 convert --》framework --》 work --》response"""
    n = namedtuple(d.pop('name'), ['url'])
    n.url = d.pop('url')
    for i in d:
        j = 'handler_' + i
        setattr(n, j, d[i])
    return n