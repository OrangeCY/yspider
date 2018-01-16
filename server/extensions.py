#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/16 下午3:20
# @Author  : zpy
# @Software: PyCharm

from flask_caching import Cache
from flask_oauthlib.client import OAuth
from flask_oauthlib.provider import OAuth2Provider
from flask_rq import RQ
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from raven.contrib.flask import Sentry

cache = Cache()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
oauth = OAuth()
rq = RQ()
csrf = CSRFProtect()
oauth_provider = OAuth2Provider()
cors = CORS()
sentry = Sentry()

