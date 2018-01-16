#!/usr/bin/env python
# @Author  : pengyun

import redis
from flask import Flask
from pymongo import MongoClient

from config import config, redis_host, redis_port, mongo_host, mongo_port
from server.auth import login_manager
from .extensions import (cache, bootstrap, mail, moment, cors,
                         oauth, rq, csrf, sentry)

redis_store = redis.StrictRedis(host=redis_host, port=redis_port)
_mongo = MongoClient(host=mongo_host, port=mongo_port)
db = _mongo['yspider']
mongo_store = db['crawl']

def create_app(config_name):
    from server.models import db
    app = Flask(__name__)
    rq.init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app