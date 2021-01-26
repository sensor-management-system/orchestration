import os

from elasticsearch import Elasticsearch
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_rest_jsonapi import Api
from flask_sqlalchemy import SQLAlchemy
from project.api.token_checker import auth_blueprint
from project.api.upload_files import upload_blueprint
from project.urls import create_endpoints

from project.api import minio

DB = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Return an application
    set up the application in a function
    """
    # init the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # instantiate the db
    DB.init_app(app)
    migrate.init_app(app, DB)

    # shell context for flask cli
    app.shell_context_processor({"app": app, "db": DB})

    # add elasticsearch as mentioned here
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search
    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    # Create endpoints
    api = Api(app)
    create_endpoints(api)

    # instantiate minio client
    minio.init_app(app)

    # enable CORS
    # initialize cors with list of allowed origins
    CORS(app, origins=app.config["HTTP_ORIGINS"])

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(upload_blueprint)

    return app
