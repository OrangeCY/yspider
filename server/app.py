#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/26 下午6:30
# @Author  : zpy
# @Software: PyCharm


from yspider.middleware import MiddleSpider
from collections import namedtuple
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

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
        print("t", t)
        res.extend(t)
    return json.dumps(res)





#
# tieba = namedtuple('tieba', ['url', 'handler_x'])
# tieba.url = 'http://tieba.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&ie=utf-8&pn=500'
# tieba.handler_url = '//*[@id="thread_list"]/li[{}]/div/div[2]/div[1]/div[1]/a/@href/text()'
# s = MiddleSpider(tieba)
# for i in s.run():
#     print(i)


if __name__ == '__main__':
    app.run(debug=True)