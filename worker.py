#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/5 下午2:29
# @Author  : zpy
# @Software: PyCharm
import os

from flask_rq import get_worker
from server import create_app

if __name__ == '__main__':
    env = os.environ.get('yspider_env', 'dev')
    app = create_app(env)
    with app.app_context():
        get_worker().work()
