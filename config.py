#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/15 下午6:01
# @Author  : zpy
# @Software: PyCharm

import os

basedir = os.path.abspath(os.path.dirname(__file__))
host = 'http://127.0.0.1:5000/'
redis_host, redis_port = 'localhost', 6379
mongo_host, mongo_port = 'localhost', 27017

class Config:
    SECRET_KEY = 'hard to guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.db')


config = {
    'dev': DevConfig,
}