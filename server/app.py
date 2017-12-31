#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/26 下午6:30
# @Author  : zpy
# @Software: PyCharm





from yspider.middleware import MiddleSpider
from flask import Flask, render_template, request
import json
from server.utils import convert

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'


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