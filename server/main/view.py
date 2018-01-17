#!/usr/bin/env python
# @Author  : pengyun

from flask import request, redirect, url_for
from flask_rq import get_connection
from server.utils import rq_loads, rq_dumps, suuid
from server.models import User, Task, db

from server.jobs.rq_job import slow_fib, job_spider
from . import main
from flask_login import login_user, logout_user, current_user, login_required
from server import mongo_store, login_manager, redis_store
import json

async_result = {}


@login_manager.user_loader
def load_user(userid):
    """callback function"""
    return User.query.get(int(userid))

@main.route('/register', methods=['GET', 'POST'])
def register():
    username = request.json['name']
    password = request.json['password']
    email = request.json['email']
    if User.query.filter_by(email=email).first() is None:
        u = User(name=username, email=email)
        # todo 暂时只用一个document
        mongo_store.insert({
            'name': username,
            'email': email,
            'task':[],
        })
        u.password = password
        db.session.add(u)
        return "Success"
    return "Already register..."

@main.route('/login', methods=['GET', 'POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    l_user = User.query.filter_by(email=email).first()
    if l_user and l_user.verify_password(password):
        login_user(l_user)
        return "Success"
    return "Failure"

@main.route('/newtask', methods=['GET', 'POST'])
@login_required
def newtask():
    title = request.json['title']
    describe = request.json['describe']
    t = Task(title=title, describe=describe)
    taskdata = json.loads(request.json['data'])
    data = taskdata
    taskdata.update({
        'tid': suuid(),
    })
    # 添加到一个列表中
    mongo_store.update({'email': current_user.email}, {'$push': {'task': taskdata}})
    db.session.add(t)
    key = job_spider(data).key.decode()
    return redirect(url_for('.job_result', id=key))
    # return 'working'


@main.route('/job/<string:id>')
def job_result(id):
    """ 通过任务id来返回结果 """
    conn = get_connection()
    result = conn.hget(id, 'result')
    if result:
        return rq_loads(result)
    return "Working ..."

@main.route('/job/test', methods=['GET', 'POST'])
def test():
    n = request.json['data']
    key = slow_fib(n).key
    return key

@main.route('/job/spider', methods=['GET', 'POST'])
def job_sp():
    """spider job test.."""
    data = request.json
    key = job_spider(data).key.decode()
    return redirect(url_for('.job_result', id=key))

@main.route('/api/task', methods=['GET', 'POST'])
def index():
    # 直接使用动态的页面来获取请求。
    # name [url, handler_x, handler_x]
    res = []
    # n = convert(request.json)
    # task = MiddleSpider(n)
    # for t in task.run():
    #     res.extend(t)
    # return json.dumps(res)
    return 'x'

@main.route('/analysis')
def analy():
    """ 直接展示图 """
    pass
