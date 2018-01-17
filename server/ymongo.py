#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/15 下午5:46
# @Author  : zpy
# @Software: PyCharm

# 将数据保存到这里。  传入一个mongo对象，直接给爬虫框架哪里处理。

def save_data(tid):
    pass

def find_data(tid):
    pass

if __name__ == '__main__':
    from pymongo import MongoClient
    db = MongoClient()
    test = db.test.test

    test.insert({
        'email':'xxxxxx',
        'task':[],
    })
    task = {
        'title':'xxx',
        'tid':'123131313',
        'body':'yyy',
    }
    task_append(test, {'email': 'xxxxxx'}, task)

    print(test.find_one())
