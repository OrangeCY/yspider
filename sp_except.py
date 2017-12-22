#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/22 上午11:48
# @Author  : zpy
# @Software: PyCharm


class SpiderException(Exception):
    """ 根据不同的 Error code来进行不同的判断"""

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "code: %s, msg: %s" % (self.code, self.msg)

    __repr__ = __str__


if __name__ == '__main__':
    s = SpiderException(1, 'fx')
    raise s

