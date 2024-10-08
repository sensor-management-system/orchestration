# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""empty message

Revision ID: bc41fd42f238
Revises: 2a72092f5fd2
Create Date: 2022-11-28 10:30:34.644331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bc41fd42f238"
down_revision = "2a72092f5fd2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "configuration_contact_role",
        "contact_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "configuration_contact_role",
        "configuration_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "device_contact_role", "contact_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "device_contact_role", "device_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "platform_contact_role",
        "contact_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "platform_contact_role",
        "platform_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "site_contact_role", "contact_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "site_contact_role", "site_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "site_contact_role", "site_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "site_contact_role", "contact_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "platform_contact_role",
        "platform_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "platform_contact_role", "contact_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "device_contact_role", "device_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "device_contact_role", "contact_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "configuration_contact_role",
        "configuration_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "configuration_contact_role",
        "contact_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    # ### end Alembic commands ###
