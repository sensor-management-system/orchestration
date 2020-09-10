import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_rest_jsonapi import Api
from flask_cors import CORS
from project.urls import create_endpoints
from project.api.token_checker import auth_blueprint

DB = SQLAlchemy()


def create_app():
    """Return an application
    set up the application in a function
    """
    # init the app
    app = Flask(__name__)

    # enable CORS
    # get space separated list from environment var
    origins_raw = os.getenv("HTTP_ORIGINS")
    # create a list of origins
    origins = origins_raw.split()
    # initialize cors with list of allowed origins
    CORS(app, origins=origins)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # instantiate the db
    DB.init_app(app)

    # shell context for flask cli
    app.shell_context_processor({"app": app, "db": DB})

    # Create endpoints
    api = Api(app)
    create_endpoints(api)

    # test to ensure the proper config was loaded
    # import sys
    # print(app.config, file=sys.stderr)

    app.register_blueprint(auth_blueprint)

    return app
