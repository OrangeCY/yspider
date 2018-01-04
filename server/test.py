#!/usr/bin/env python
# @Author  : pengyun


import requests


data = {
    'name': 'tieba',
    'url': ['http://tieba.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&ie=utf-8&pn=500',
            'http://tieba.baidu.com/f?kw=%E8%BF%90%E5%9F%8E%E5%AD%A6%E9%99%A2&ie=utf-8&pn=550',
            ],
    'title': '//*[@id="thread_list"]/li[5]/div/div[2]/div[1]/div[1]/a/text()',
}
resp = requests.post('http://127.0.0.1:5000/job/spider', json=data)
