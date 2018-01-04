#!/usr/bin/env python
# @Author  : pengyun

from flask import Flask, request, render_template, g
from flask_rq import RQ


def create_app(config_name):
    app = Flask(__name__)
    RQ().init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app