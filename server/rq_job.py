#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/4 下午4:29
# @Author  : zpy
# @Software: PyCharm

from flask_rq import job

@job
def _slow_fib(n):
    if n <= 1:
        return 1
    else:
        return _slow_fib(n-1) + _slow_fib(n-2)



def slow_fib(n):
    return _slow_fib.delay(n)
