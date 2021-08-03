import requests
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from ..models.base_model import db


def health_check_elastic_search():
    """
    Check health status of elastic search server
    :return:
    """
    try:
        _ = requests.get(current_app.config["ELASTICSEARCH_URL"]).content
        return True, "elastic search ok"

    except requests.exceptions.HTTPError:
        return False, "Error connecting to elastic search server"


def health_check_db():
    """
    Check health status of db
    :return:
    """
    try:
        db.session.execute('SELECT 1')
        return True, 'database ok'
    except SQLAlchemyError:

        return False, 'Error connecting to database'


def health_check_migrations():
    """
    Checks whether database is up to date with migrations.
    :return:
    """

    from alembic.runtime import migration

    with db.engine.begin() as conn:
        context = migration.MigrationContext.configure(conn)
        version_num = (db.session.execute('SELECT version_num from alembic_version').fetchone())[
            'version_num']
        if version_num != context.get_current_revision():
            return False, 'database out of date with migrations'
        return True, 'database up to date with migrations'
