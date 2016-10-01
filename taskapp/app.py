"""The app module contains the app factory function."""
import os

from flask import Flask, url_for

from . import extensions
from . import settings
from . import api, user, public


def create_app(config=settings.ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extentions(app)
    register_blueprints(app)
    return app


def register_extentions(app):
    extensions.login_manager.init_app(app)
    extensions.csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
