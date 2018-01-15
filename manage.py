#!/usr/bin/env python
# @Author  : pengyun

from server import create_app
from server.models import User, Task, db

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('dev')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Task=Task)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def createdb():
    """ create datebase"""
    db.create_all()

if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)