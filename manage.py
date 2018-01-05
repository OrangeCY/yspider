#!/usr/bin/env python
# @Author  : pengyun

from server import create_app
from flask_script import Manager, Shell, Server

app = create_app('test')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
