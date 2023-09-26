# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
This migration add created_by & updated_by user to table device_property_calibration.

Revision ID: 6668dbc28346
Revises: 8f2088ecddea
Create Date: 2021-03-19 08:28:36.695420

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6668dbc28346"
down_revision = "8f2088ecddea"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "device_property_calibration",
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "device_property_calibration",
        sa.Column("created_by_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "device_property_calibration",
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "device_property_calibration",
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_DevicePropertyCalibration_created_by_id",
        "device_property_calibration",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_DevicePropertyCalibration_updated_by_id",
        "device_property_calibration",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "fk_DevicePropertyCalibration_updated_by_id",
        "device_property_calibration",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_DevicePropertyCalibration_created_by_id",
        "device_property_calibration",
        type_="foreignkey",
    )
    op.drop_column("device_property_calibration", "updated_by_id")
    op.drop_column("device_property_calibration", "updated_at")
    op.drop_column("device_property_calibration", "created_by_id")
    op.drop_column("device_property_calibration", "created_at")
    # ### end Alembic commands ###
