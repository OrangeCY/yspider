#!/usr/bin/env python
# @Author  : pengyun

from flask import Flask, Blueprint

main = Blueprint('main', __name__)
from . import view
