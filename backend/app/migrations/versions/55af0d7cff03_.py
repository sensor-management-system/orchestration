# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""empty message

Revision ID: 55af0d7cff03
Revises: db0151dc70c3
Create Date: 2022-09-16 07:14:42.471569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "55af0d7cff03"
down_revision = "db0151dc70c3"
branch_labels = None
depends_on = None

fields_to_migrate = {
    "configuration": ["created_at", "updated_at", "start_date", "end_date"],
    "device_calibration_action": [
        "current_calibration_date",
        "next_calibration_date",
        "created_at",
        "updated_at",
    ],
    "device_property_calibration": [
        "created_at",
        "updated_at",
    ],
    "configuration_static_location_begin_action": [
        "begin_date",
        "created_at",
        "updated_at",
        "end_date",
    ],
    "configuration_dynamic_location_begin_action": [
        "begin_date",
        "end_date",
        "created_at",
        "updated_at",
    ],
    "device": [
        "created_at",
        "updated_at",
    ],
    "generic_platform_action": [
        "begin_date",
        "end_date",
        "created_at",
        "updated_at",
    ],
    "generic_device_action": [
        "begin_date",
        "end_date",
        "created_at",
        "updated_at",
    ],
    "generic_configuration_action": [
        "begin_date",
        "end_date",
        "created_at",
        "updated_at",
    ],
    "platform_mount_action": [
        "begin_date",
        "end_date",
        "created_at",
        "updated_at",
    ],
    "device_mount_action": [
        "begin_date",
        "end_date",
        "created_at",
        "updated_at",
    ],
    "platform": [
        "created_at",
        "updated_at",
    ],
    "device_software_update_action": [
        "update_date",
        "created_at",
        "updated_at",
    ],
    "platform_software_update_action": [
        "update_date",
        "created_at",
        "updated_at",
    ],
}


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    for table, list_of_fields in fields_to_migrate.items():
        for field in list_of_fields:
            op.alter_column(table, field, type_=sa.DateTime(timezone=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    for table, list_of_fields in fields_to_migrate.items():
        for field in list_of_fields:
            op.alter_column(table, field, type_=sa.DateTime(timezone=False))
    # ### end Alembic commands ###
