#!/usr/bin/env python
# @Author  : pengyun

from flask import request, redirect
from flask_rq import get_connection
from server.utils import rq_loads, rq_dumps, suuid
from server.models import User, Task, db

from server.jobs.rq_job import slow_fib, job_spider
from . import main
from flask_login import login_user, logout_user, current_user, login_required
from server import mongo_store, login_manager, redis_store

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
    taskdata = request.json['data']
    taskdata.update({
        'tid': suuid(),
    })
    # 添加到一个列表中
    mongo_store.update({'email': current_user.email}, {'$push': {'task': taskdata}})
    db.session.add(t)
    print(mongo_store.find_one({'email': current_user.email}))
    return 'test'


@main.route('/job/<string:id>')
def job_result(id):
    conn = get_connection()
    return str(rq_loads(conn.hget(id, 'result')))

@main.route('/job/test', methods=['GET', 'POST'])
def test():
    n = request.json['data']
    key = slow_fib(n).key
    # res = None
    # if n in async_result:
    #     res = async_result[n].return_value
    # else:
    #     async_result[n] = slow_fib(n)
    # if res is None:
    #     return "Working...."
    # return jsonify({
    #     'request': n,
    #     'result': res,
    # })
    return key

@main.route('/job/spider', methods=['GET', 'POST'])
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
