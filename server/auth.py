#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/16 下午3:26
# @Author  : zpy
# @Software: PyCharm

from flask_login import LoginManager


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/login'