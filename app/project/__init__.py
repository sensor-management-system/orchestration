import os

from elasticsearch import Elasticsearch
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_migrate import Migrate
from project.api.models.base_model import db
from project.api.token_checker import jwt
from project.urls import api
from project.frj_csv_export.render_csv import render_csv

from project.api import minio

migrate = Migrate()
base_url = os.getenv("URL_PREFIX", "/rdm/svm-api/v1")


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
    db.init_app(app)
    api.init_app(
        app,
        Blueprint(
            "api", __name__, url_prefix=base_url
        ),
        response_renderers={"text/csv": render_csv}
    )
    migrate.init_app(app, db)
    # jwt.init_app(app)

    # instantiate minio client
    minio.init_app(app)

    # shell context for flask cli
    app.shell_context_processor({"app": app, "db": db})

    # add elasticsearch as mentioned here
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search
    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    # test to ensure the proper config was loaded
    # import sys
    # print(app.config, file=sys.stderr)

    # enable CORS
    # initialize cors with list of allowed origins
    CORS(app, origins=app.config["HTTP_ORIGINS"])


    return app
