#!/usr/bin/env python
# @Author  : pengyun

from flask import Flask, request, render_template, g
from flask_rq import RQ
from config import config


def create_app(config_name):
    from server.models import db
    app = Flask(__name__)
    RQ().init_app(app)
    db.init_app(app)
    config[config_name].init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app