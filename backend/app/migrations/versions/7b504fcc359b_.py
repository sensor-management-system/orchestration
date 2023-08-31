# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add contact roles

Revision ID: 7b504fcc359b
Revises: 0139893c4e15
Create Date: 2022-03-15 12:02:28.389582

"""
import os

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from project.api.models.base_model import db
from sqlalchemy import MetaData, Table

# revision identifiers, used by Alembic.

revision = "7b504fcc359b"
down_revision = "aa89a10ad413"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "device_contact_role",
        sa.Column("role_name", sa.String(), nullable=False),
        sa.Column("role_uri", sa.String(length=256), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=True),
        sa.Column("device_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
        ),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["device.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "platform_contact_role",
        sa.Column("role_name", sa.String(), nullable=False),
        sa.Column("role_uri", sa.String(length=256), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=True),
        sa.Column("platform_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "configuration_contact_role",
        sa.Column("role_name", sa.String(), nullable=False),
        sa.Column("role_uri", sa.String(length=256), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=True),
        sa.Column("configuration_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["configuration_id"],
            ["configuration.id"],
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # Fill contact_role tables with default role.
    cv_url = os.environ.get("CV_URL")
    # a default role should be listed in our controlled vocabulary!
    default_role = "Operator"
    # If you are willing to change the default role please be attention to change the uri also ;)
    default_role_uri = f"{cv_url}/contactroles/3/"
    add_device_contact_role(default_role, default_role_uri)
    add_platform_contact_role(default_role, default_role_uri)
    add_configuration_contact_role(default_role, default_role_uri)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("configuration_contact_role")
    op.drop_table("platform_contact_role")
    op.drop_table("device_contact_role")
    # ### end Alembic commands ###


def add_device_contact_role(default_role, default_role_uri):
    """
    Method To fill the device contact role table with default role.

    :param string default_role: default role name.
    :param default_role_uri: URI of the default role.
    """
    try:
        device_contacts = db.session.query(db.metadata.tables["device_contacts"]).all()
        data_list = []
        for device_contact in device_contacts:
            data = {
                "device_id": device_contact[0],
                "contact_id": device_contact[1],
                "role_name": default_role,
                "role_uri": default_role_uri,
            }
            data_list.append(data)
        meta = MetaData(bind=op.get_bind())
        meta.reflect(only=("device_contact_role",))
        device_contact_role = Table("device_contact_role", meta)
        op.bulk_insert(device_contact_role, data_list)
    except (sa.exc.ProgrammingError, sa.exc.InternalError):
        pass


def add_platform_contact_role(default_role, default_role_uri):
    """
    Method To fill the platform contact role table with default role.

    :param string default_role: default role name.
    :param default_role_uri: URI of the default role.
    """
    try:
        platform_contacts = db.session.query(
            db.metadata.tables["platform_contacts"]
        ).all()
        data_list = []
        for platform_contact in platform_contacts:
            data = {
                "platform_id": platform_contact[0],
                "contact_id": platform_contact[1],
                "role_name": default_role,
                "role_uri": default_role_uri,
            }
            data_list.append(data)
        meta = MetaData(bind=op.get_bind())
        meta.reflect(only=("platform_contact_role",))
        platform_contact_role = Table("platform_contact_role", meta)
        op.bulk_insert(platform_contact_role, data_list)
    except (sa.exc.ProgrammingError, sa.exc.InternalError):
        pass


def add_configuration_contact_role(default_role, default_role_uri):
    """
    Method To fill the configuration contact role table with default role.

    :param string default_role: default role name.
    :param default_role_uri: URI of the default role.
    """
    try:
        configuration_contacts = db.session.query(
            db.metadata.tables["configuration_contacts"]
        ).all()
        data_list = []
        for configuration_contact in configuration_contacts:
            data = {
                "configuration_id": configuration_contact[0],
                "contact_id": configuration_contact[1],
                "role_name": default_role,
                "role_uri": default_role_uri,
            }
            data_list.append(data)
        meta = MetaData(bind=op.get_bind())
        meta.reflect(only=("configuration_contact_role",))
        configuration_contact_role = Table("configuration_contact_role", meta)
        op.bulk_insert(configuration_contact_role, data_list)
    except (sa.exc.ProgrammingError, sa.exc.InternalError):
        pass