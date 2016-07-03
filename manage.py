from flask import Flask

from taskapp.app import create_app
from taskapp.extensions import Base, engine
from taskapp.settings import DevConfig, ProdConfig
import os

if os.environ.get("CONTESTAPP_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

app.run()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import taskapp.models
    Base.metadata.create_all(bind=engine)