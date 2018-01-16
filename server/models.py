#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/9 下午6:53
# @Author  : zpy
# @Software: PyCharm

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
import functools
import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Model(db.Model):
    """ 一套基类方法，支持将数据库的数据导出为csv, 转为字典，通过字典插入数据库"""
    __abstract__ = True

    created = db.Column(db.DateTime(timezone=True),
                        server_default=db.func.now(), nullable=False)

    def __repr__(self):
        """ 易于调试 """
        if hasattr(self, 'id'):
            key_val = self.id
        else:
            pk = self.__mapper__.primary_key
            if type(pk) == tuple:
                key_val = pk[0].name
            else:
                key_val = self.__mapper__.primary_key._list[0].name
        return '<{0} {1}>'.format(self.__class__.__name__, key_val)

    @classmethod
    def can(cls, obj, user, action):
        if user.is_admin:
            return True
        return False

    @hybrid_property
    def export(self):
        """ 转为csv """
        if not hasattr(self, 'export_items'):
            return {}
        return {k: v for k, v in self.as_dict().items() if k in self.export_items}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def from_dict(self, dict):
        for c in self.__table__.columns:
            if c.name in dict:
                setattr(self, c.name, dict[c.name])
        return self

def transaction(f):
    """ 用来提交数据"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            value = f(*args, **kwargs)
            db.session.commit()
            return value
        except:
            db.session.rollback()
            raise

    return wrapper

class User(Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    is_admin = db.Column(db.Boolean(), default=False)
    password_hash = db.Column(db.String(128))

    export_items = ('email', 'name')

    def __repr__(self):
        return "<User {0}>".format(self.email)

    @staticmethod
    def get_by_id(uid):
        return User.query.get(uid)

    @property
    def password(self):
        return "You can't see you password"

    @password.setter
    def password(self, psd):
        self.password_hash = generate_password_hash(psd)

    def verify_password(self, psd):
        return check_password_hash(self.password_hash, psd)

class Task(Model):
    """ 用户创建的任务 ，通过这个id来从mongodb 获取任务的结果"""
    id = db.Column(db.Integer, primary_key=True) # 生成一个唯一的tid来查询任务
    title = db.Column(db.String(255))
    describe = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('task', uselist=False))

    def __repr__(self):
        return "{} --> {}".format(self.user, self.title)

