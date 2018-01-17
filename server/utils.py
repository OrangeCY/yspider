#!/usr/bin/env python
# @Author  : pengyun

from collections import namedtuple
import time

try:
    import cPickle as pickle
except ImportError:
    import pickle

from functools import partial

#　直接使用ｒｑ中带的两个函数
rq_dumps = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)
rq_loads = pickle.loads

def p_named(named):
    """
    打印named 中的属性。
    :param named:
    :return:
    """
    print("namedtuple --> {}".format(named.__name__))
    for i in dir(named):
        if not i.startswith('_'):
            print(i)

def convert(d):
    """ web请求 --》 convert --》framework --》 work --》response"""
    n = namedtuple(d.pop('name'), ['url'])
    n.url = d.pop('url')
    for i in d:
        j = 'handler_' + i
        setattr(n, j, d[i])
    return n

def suuid():
    """ 时间戳加随机数"""
    import random
    s = str(time.time()).split('.')
    s[1] = str(random.randrange(10, 100))
    return ''.join(s)

if __name__ == '__main__':
    data = {
        'url':'xxx', # 爬取的url
        'name': 'wtf', # 项目名
        # 要获取的值 对应的是xpath 或者 re 或者。。
        'title': 'xxxxx',
        'describe': 'xxxxxx',
    }
    d = convert(data)
    p_named(d)
    print([suuid() for _ in range(100)])
