# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add update_description to [device, platform, configuration]

Revision ID: 91a9445513c0
Revises: 13e35f226a7c
Create Date: 2022-06-24 12:10:41.159803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "91a9445513c0"
down_revision = "2c77c77a37cb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "configuration",
        sa.Column("update_description", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "device", sa.Column("update_description", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "platform",
        sa.Column("update_description", sa.String(length=256), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("platform", "update_description")
    op.drop_column("device", "update_description")
    op.drop_column("configuration", "update_description")
    # ### end Alembic commands ###