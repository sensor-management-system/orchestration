import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_rest_jsonapi import Api
from flask_cors import CORS
from project.urls import create_endpoints
from project.api.token_checker import auth_blueprint

DB = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Return an application
    set up the application in a function
    """
    # init the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # instantiate the db
    DB.init_app(app)
    migrate.init_app(app, DB)

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
