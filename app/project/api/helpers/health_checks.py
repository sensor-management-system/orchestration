# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

import logging

import requests
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from ..models.base_model import db
from ... import minio
from ...extensions.instances import pid


def health_check_elastic_search():
    """
    Check health status of elastic search server.

    :return: boolean and a message
    """
    try:
        _ = requests.get(current_app.config["ELASTICSEARCH_URL"]).content
        return True, "elastic search ok"

    except requests.exceptions.HTTPError as e:
        logging.error("Error" + repr(e))
        return False, "Error connecting to elastic search server"


def health_check_db():
    """
    Check health status of db.

    :return:boolean and a message
    """
    try:
        db.session.execute("SELECT 1")
        return True, "database ok"
    except SQLAlchemyError as err:
        logging.error("Error" + repr(err))
        return False, "Error connecting to database"


def health_check_migrations():
    """
    Check whether database is up-to-date with migrations.

    :return: boolean and a message
    """

    from alembic.runtime import migration

    with db.engine.begin() as conn:
        context = migration.MigrationContext.configure(conn)
        version_num = (
            db.session.execute("SELECT version_num from alembic_version").fetchone()
        )["version_num"]
        ctx_head = context.get_current_revision()
        if version_num != ctx_head:
            logging.error(
                "Error:  Migration head in Database is: {} But migration version is: {}".format(
                    version_num, ctx_head
                )
            )
            return False, "database out of date with migrations"
        return True, "database up to date with migrations"


def health_check_minio():
    """
    Check health status of minio-server
    and proof if booth connection and the sms-bucket are True.

    :return: boolean and a message
    """

    minio_bucket_name = current_app.config["MINIO_BUCKET_NAME"]
    try:
        minio_is_connected_and_bucket_exist = minio.connection.bucket_exists(
            minio_bucket_name
        )
        if not minio_is_connected_and_bucket_exist:
            return False, "Error No bucket was found."
        else:
            return True, "MinIO is up "
    except requests.exceptions.RequestException as s3err:
        logging.error("Error" + repr(s3err))
        return False, "Error connecting to MinIO server."


def health_check_pid_handler():
    """
    Check health status of the pid-Handler

    :return: boolean and a Message
    """
    try:
        pid.list()
        return True, "Handler server is ok"
    except requests.exceptions.HTTPError as e:
        logging.error("Error" + repr(e))
        return False, "Error connecting to Handler server"
