from flask import Flask


from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand
from taskapp.app import create_app
from taskapp.tasks.worker import nestPoll
from taskapp.extensions import db
from taskapp.settings import DevConfig, ProdConfig


if os.environ.get("CONTESTAPP_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

manager = Manager(app)
manager.add_command('db', MigrateCommand)