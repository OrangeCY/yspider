#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/4 下午4:31
# @Author  : zpy
# @Software: PyCharm

from flask_rq import get_worker

from web.server import app

with app.app_context():
    get_worker().work()


