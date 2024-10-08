# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Add site usages

Revision ID: c0d89a7e62cc
Revises: 3537e6159bcc
Create Date: 2022-12-16 06:25:17.983796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0d89a7e62cc"
down_revision = "3537e6159bcc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "site", sa.Column("site_usage_uri", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "site", sa.Column("site_usage_name", sa.String(length=256), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("site", "site_usage_name")
    op.drop_column("site", "site_usage_uri")
    # ### end Alembic commands ###
