import os
import threading
import time

from elasticsearch import Elasticsearch
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .api.models.base_model import db
from .api.token_checker import jwt
from .urls import api

migrate = Migrate()
base_url = os.getenv("URL_PREFIX", "/rdm/svm-api/v1")


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
    db.init_app(app)
    api.init_app(app, Blueprint("api", __name__, url_prefix=base_url))
    migrate.init_app(app, db)
    jwt.init_app(app)

    # shell context for flask cli
    app.shell_context_processor({"app": app, "db": db})

    # add elasticsearch as mentioned here
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search
    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    # If we have the config to update our jwt config, then we want to do that
    # from time to time - in order to prevent problems on changes of the IDP config
    # (which will make the validation fail).
    # With this code here we start a thread that checks the config every 5 minutes
    # So we will be sure that 5 minutes after a IDP change, we can validate our tokens
    # again.
    # Using a thread here is important as we need to update the app.config dict.
    # Also it is important that we wait from time to time to allow the webserver
    # to run (no real multi-threading in python).
    # (Running web requests to the IDP should allow context switches as well, so we
    # should not expect a huge impact on the performance here).
    # Also this here should not effect our test codes as there is no OIDC_JWT_SERVICE
    # in the test config.
    if app.config.get("OIDC_JWT_SERVICE", None) is not None:

        def update_jwt_settings():
            """Update the JWT settings from the IDP."""
            while True:
                time.sleep(60 * 5)
                oidc_jwt_service = app.config["OIDC_JWT_SERVICE"]
                app.config["JWT_PUBLIC_KEY"] = oidc_jwt_service.get_jwt_public_key()
                app.config["JWT_ALGORITHM"] = oidc_jwt_service.get_jwt_algorithm()

        update_jwt_settings_thread = threading.Thread(
            target=update_jwt_settings,
            args=(),
        )
        update_jwt_settings_thread.start()

    # test to ensure the proper config was loaded
    # import sys
    # print(app.config, file=sys.stderr)

    return app
