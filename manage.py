from flask import Flask

from taskapp.app import create_app
from taskapp.extensions import Base, engine
from taskapp.settings import DevConfig, ProdConfig
import os
import sys
import click

if os.environ.get("TASKAPP_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import taskapp.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@click.command()
@click.option('--host', default='127.0.0.1', help='IP address to bind webserver.  Localhost or local IP')
@click.option('--port', default=5000, help='Port number for web-server')
def main_function(host, port):
    app.run(host=host, port=port)

if __name__ == '__main__':

    if len(sys.argv)>1 and sys.argv[1] == 'init_db':
        init_db()

    main_function()