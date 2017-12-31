#!/usr/bin/env python
# @Author  : pengyun

from collections import namedtuple

def convert(d):
    """ 将通过接口拿过来的请求转化为 namedtuple，传入 """
    n = namedtuple(d.pop('name'), ['url'])
    n.url = d.pop('url')
    for i in d:
        j = 'handler_' + i
        setattr(n, j, d[i])
    return n