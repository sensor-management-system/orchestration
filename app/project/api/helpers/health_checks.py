import logging

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

    except requests.exceptions.HTTPError as e:
        logging.error('Error' + str(e))
        return False, "Error connecting to elastic search server"


def health_check_db():
    """
    Check health status of db
    :return:
    """
    try:
        db.session.execute('SELECT 1')
        return True, 'database ok'
    except SQLAlchemyError as err:
        logging.error('Error' + str(err))
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
        ctx_head = context.get_current_revision()
        if version_num != ctx_head:
            logging.error(
                'Error:  Migration head in Database is: {} But migration version is: {}'.format(
                    version_num,
                    ctx_head))
            return False, 'database out of date with migrations'
        return True, 'database up to date with migrations'


def health_check_minio():
    """
    Check health status of minio
    :return:
    """

    try:
        _ = requests.get("http://minio:9000/minio/health/live").content
        return True, 'minio is up'
    except requests.exceptions.RequestException as s3err:
        logging.error('Error' + str(s3err))
        return False, 'Error connecting to minio'
