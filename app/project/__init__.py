"""Application for the sensor management system."""

from elasticsearch import Elasticsearch
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_migrate import Migrate
from healthcheck import HealthCheck

from .api import minio
from .api.auth.permission_manager import permission_manager
from .api.helpers.health_checks import (
    health_check_db,
    health_check_elastic_search,
    health_check_migrations,
    health_check_minio,
)
from .api.models.base_model import db
from .config import env
from .extensions.instances import auth, idl, well_known_url_config_loader
from .urls import api
from .views import upload_routes, docs_routes, login_routes, sensor_ml_routes

migrate = Migrate()
base_url = env("URL_PREFIX", "/rdm/svm-api/v1")
static_url_path = env("STATIC_URL", "/static/backend")
health = HealthCheck()


def create_app():
    """Return an application and set up the application in a function."""
    # init the app
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="static",
        static_url_path=static_url_path,
    )
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
    api.permission_manager(permission_manager)

    # instantiate minio client
    minio.init_app(app)

    well_known_url_config_loader.init_app(app)
    auth.init_app(app)
    idl.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def shell_context():
        return {"app": app, "db": db}

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

    # Health Checks
    health.add_check(health_check_elastic_search)
    health.add_check(health_check_db)
    health.add_check(health_check_migrations)
    health.add_check(health_check_minio)
    app.add_url_rule(base_url + "/health", "health", view_func=lambda: health.run())

    # upload_routes
    app.register_blueprint(upload_routes)
    # docs_routes
    app.register_blueprint(docs_routes)
    # login_routes
    app.register_blueprint(login_routes)
    # sensor_ml_routes
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    app.register_blueprint(sensor_ml_routes)
    return app
