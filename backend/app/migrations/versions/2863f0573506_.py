# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add tables for parameters & change actions for devices & configurations.

Revision ID: 2863f0573506
Revises: 89b77ad855f5
Create Date: 2023-04-19 08:49:17.260791

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2863f0573506"
down_revision = "3dcc10ac1814"
branch_labels = None
depends_on = None


def upgrade():
    """Do the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "device_parameter",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=256), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("unit_uri", sa.String(length=256), nullable=True),
        sa.Column("unit_name", sa.String(length=256), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_DeviceParameter_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["device.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_DeviceParameter_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "configuration_parameter",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("configuration_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=256), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("unit_uri", sa.String(length=256), nullable=True),
        sa.Column("unit_name", sa.String(length=256), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["configuration_id"],
            ["configuration.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_ConfigurationParameter_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_ConfigurationParameter_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "device_parameter_value_change_action",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("device_parameter_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_DeviceParameterValueChangeAction_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["device_parameter_id"],
            ["device_parameter.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_DeviceParameterValueChangeAction_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "configuration_parameter_value_change_action",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("configuration_parameter_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["configuration_parameter_id"],
            ["configuration_parameter.id"],
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_ConfigurationParameterValueChangeAction_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_ConfigurationParameterValueChangeAction_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    """Undo the database changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("configuration_parameter_value_change_action")
    op.drop_table("device_parameter_value_change_action")
    op.drop_table("configuration_parameter")
    op.drop_table("device_parameter")
    # ### end Alembic commands ###