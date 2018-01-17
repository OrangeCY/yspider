#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/15 下午7:19
# @Author  : zpy
# @Software: PyCharm

import requests
from config import host
import json

data = {
    'name': 'test',
    'email': 'test@qq.com',
    'password': 'wtf',
}

print(requests.post(host + 'register', json=data).content == b'Success')
print(requests.post(host + 'register', json=data).content == b'Already register...')

data = {
    'email': 'test@qq.com',
    'password': 'wtf',
}

resp = requests.post(host + 'login', json=data)
print(requests.post(host + 'login', json=data).content)

data =  {
        'name': 'tieba',
        'url': ['http://tieba.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&ie=utf-8&pn=200',
                'http://tieba.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&ie=utf-8&pn=250',
                ],
        'title': '//*[@id="thread_list"]/li[5]/div/div[2]/div[1]/div[1]/a/text()',
        }


task = {
    'title': 'the first test.',
    'describe': 'wtf',
    'data': json.dumps(data),
}

print(requests.post(host + 'newtask', json=task, cookies=resp.cookies).content)
