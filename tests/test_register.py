#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/15 下午7:19
# @Author  : zpy
# @Software: PyCharm

import requests
from config import host

data = {
    'name': 'test',
    'email': 'test@qq.com',
    'password': 'wtf',
}

print(requests.post(host + 'register', json=data).content == b'Success')
print(requests.post(host + 'register', json=data).content == b'Already register...')