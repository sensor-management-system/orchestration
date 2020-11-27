import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from project.api.token_checker import auth_blueprint
from project.frj_monkey_patching.api import Api
from project.frj_monkey_patching.render_csv import render_csv
from project.urls import create_endpoints

from elasticsearch import Elasticsearch

DB = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Return an application
    set up the application in a function
    """
    # init the app
    app = Flask(__name__)

    # enable CORS
    # get space separated list from environment var
    origins_raw = os.getenv("HTTP_ORIGINS", None)
    if origins_raw:
        # create a list of origins
        origins = origins_raw.split()
        # initialize cors with list of allowed origins
        CORS(app, origins=origins)

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
    api = Api(app, response_renderers={"text/csv": render_csv})
    create_endpoints(api)

    # test to ensure the proper config was loaded
    # import sys
    # print(app.config, file=sys.stderr)

    app.register_blueprint(auth_blueprint)

    return app
