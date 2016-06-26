"""Extensions module.

Each extension is initialized in the app factory located in app.py
"""
from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.mail import Mail
mail = Mail()

from flask.ext.admin import Admin
admin = Admin()

from flask.ext.migrate import Migrate
migrate = Migrate()