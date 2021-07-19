from elasticsearch import Elasticsearch
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .api import minio
from .api.models.base_model import db
from .api.token_checker import jwt
from .api.upload_files import upload_routes
from .config import env
from .urls import api

migrate = Migrate()
base_url = env("URL_PREFIX", "/rdm/svm-api/v1")


def create_app():
    """Return an application
    set up the application in a function
    """
    # init the app
    app = Flask(__name__)

    # enable CORS
    # get space separated list from environment var
    origins_raw = env("HTTP_ORIGINS", None)
    if origins_raw:
        # create a list of origins
        origins = origins_raw.split()
        # initialize cors with list of allowed origins
        CORS(app, origins=origins)

    # set config
    app_settings = env("APP_SETTINGS")
    app.config.from_object(app_settings)

    # instantiate the db
    db.init_app(app)
    api.init_app(app, Blueprint("api", __name__, url_prefix=base_url))
    migrate.init_app(app, db)
    jwt.init_app(app)

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

    # upload_routes
    app.register_blueprint(upload_routes)
    return app
