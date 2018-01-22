#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/22 下午6:41
# @Author  : zpy
# @Software: PyCharm

from collections import namedtuple


def p_named(named):
    """
    打印namedtuple 中的属性。
    :param named:
    :return:
    """
    print(named.__dict__['_fields'])

def to_dict(named):
    res = []
    for i in named.__dict__['_fields']:
        if isinstance(getattr(named, i), property):
            res.append('Null')
        else:
            res.append(getattr(named, i))
    return {named.__name__: res}

# 主要是source 名字， 出发日期，到达日期，具体的出发时间， 到达时间，出发城市，到达城市 价格
# 对于有转机的下划线添加出来。
flight = namedtuple('Flight', ['source', 'depdate', 'arrdate','deptime', 'arrtime', 'depcity', 'arrcity', 'price'])


if __name__ == '__main__':
    flight.source = 'x'
    flight.depdate = '2048'
    flight.arrdate = '123456'
    flight.deptime = '1221'
    flight.arrtime = '12342314'
    flight.depcity = 'abc'
    # flight.arrcity = 'cba'
    flight.price = 100
    print(to_dict(flight))


