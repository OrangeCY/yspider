#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/9 下午6:51
# @Author  : zpy
# @Software: PyCharm

# 对rq进行一层包装。增加额外功能。

from flask_rq import get_connection, get_queue
import redis.exceptions
import rq
import functools
# todo 将job和user 绑定起来。并且将job 对应的数据保存起来。
def background_job(f):
    @functools.wraps(f)
    def job_handler(*args, **kwargs):
        pass