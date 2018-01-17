#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/16 下午6:58
# @Author  : zpy
# @Software: PyCharm

import requests
from config import host

data = {
    'email': 'test@qq.com',
    'password': 'wtf',
}

resp = requests.post(host + 'login', json=data)
print(requests.post(host + 'login', json=data).content)

task = {
    'title': 'the first test.',
    'describe': 'wtf',
    'data':{
        'testdata':'teststestesstesa',
    }
}

print(requests.post(host + 'newtask', json=task, cookies=resp.cookies).content)
