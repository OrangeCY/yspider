#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/26 下午6:30
# @Author  : zpy
# @Software: PyCharm,

import json

from flask import Flask, request, jsonify
from flask_rq import RQ
from server.utils import convert

from web.server.rq_job import slow_fib, job_spider
from yspider.middleware import MiddleSpider

rq = RQ()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
rq.init_app(app)

async_result = {}

# todo fix bug ,

@app.route('/job/test', methods=['GET', 'POST'])
def test():
    n = request.json['data']
    res = None
    if n in async_result:
        res = async_result[n].return_value
    else:
        async_result[n] = slow_fib(n)
    if res is None:
        return "Working...."
    return jsonify({
        'request': n,
        'result': res,
    })

@app.route('/job/spider', methods=['GET', 'POST'])
def job_sp():
    """spider job test.."""
    data = request.json
    name = data['name']
    res = None
    if name in async_result:
        res = async_result[name].return_value
    else:
        async_result[name] = job_spider(data)
    if res is None:
        return "Working..."
    return res

@app.route('/api/task', methods=['GET', 'POST'])
def index():
    # 直接使用动态的页面来获取请求。
    # name [url, handler_x, handler_x]
    res = []
    n = convert(request.json)
    task = MiddleSpider(n)
    for t in task.run():
        res.extend(t)
    return json.dumps(res)

@app.route('/analysis')
def analy():
    """ 直接展示图 """
    pass



if __name__ == '__main__':
    app.run(debug=True)