#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/22 上午11:48
# @Author  : zpy
# @Software: PyCharm


class SpiderException(Exception):
    """ 根据不同的 Error code来进行不同的判断,
        重试 3
        默认三次重试，如果三次后还失败 31
        解析出错 5
    """
    RETRY = 3
    RETRYBAD = 31
    PARSEBDA = 5

    map_error = {
        RETRY: "失败重试",
        RETRYBAD: "重试也失败",
        PARSEBDA: "解析失败"
    }



    def __init__(self, code, msg=None):
        self.code = code
        self.msg = msg if msg else self.map_error[code]

    def __str__(self):
        return "code: %s, msg: %s" % (self.code, self.msg)

    __repr__ = __str__


if __name__ == '__main__':
    s = SpiderException(SpiderException.RETRY)
    raise s

