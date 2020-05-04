import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_rest_jsonapi import Api
from flask_cors import CORS
from project.urls import Create_endpoints

db = SQLAlchemy()


def create_app(script_info=None):
    # init the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # instantiate the db
    db.init_app(app)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})

    # Create endpoints
    api = Api(app)
    Create_endpoints(api)

    # test to ensure the proper config was loaded
    # print(app.config, file=sys.stderr)

    return app
