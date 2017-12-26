#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/26 下午6:30
# @Author  : zpy
# @Software: PyCharm


from yspider.middleware import MiddleSpider
from collections import namedtuple
from flask import Flask, render_template, request
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

def convert(d):
    """ 请求转化为 namedtuple """
    n = namedtuple(d.pop('name'), ['url'])
    n.url = d.pop('url')
    for i in d:
        j = 'handler_' + i
        setattr(n, j, d[i])
    return n

@app.route('/api/spider', methods=['GET', 'POST'])
def index():
    # 直接使用动态的页面来获取请求。
    # name [url, handler_x, handler_x]
    res = []
    n = convert(request.json)
    task = MiddleSpider(n)
    for t in task.run():
        res.extend(t)
    return json.dumps(res)

if __name__ == '__main__':
    app.run(debug=True)