#!/usr/bin/env python
# @Author  : pengyun

from collections import namedtuple

def p_named(named):
    """
    打印named 中的属性。
    :param named:
    :return:
    """
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

if __name__ == '__main__':
    data = {
        'url':'xxx', # 爬取的url
        'name': 'xxx', # 项目名
        # 要获取的值 对应的是xpath 或者 re 或者。。
        'title': 'xxxxx',
        'describe': 'xxxxxx',
    }
    d = convert(data)
    p_named(d)
