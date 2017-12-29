#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/29 上午9:36
# @Author  : zpy
# @Software: PyCharm

# 将获取的数据进行分词 统计。

import csv
import jieba
from yspider.utils import init_db

def split_word(cname):
    coll = init_db(coll=cname)
    with open('./analyresult/describes', 'wb') as f:
        for t in coll.find():
            describe = t['describe'].split() if t['describe'] else None
            if describe:
                for j in jieba.cut(t['describe'], HMM=False):
                    if j.split():
                        f.write((j+'\n').encode())


def word_count(fname):
    res = {}
    with open(fname+'result', 'wb') as w:
        with open(fname, 'rb') as r:
            for i in r.readlines():
                res[i] = res.get(i, 0)+1
        res = sorted(res.items(), key=lambda x:x[1])[::-1]
        for i, j in res:
            w.write(i + (str(j)+'      ').encode())


if __name__ == '__main__':
    # split_word('四川大学')
    word_count('./analyresult/describes')