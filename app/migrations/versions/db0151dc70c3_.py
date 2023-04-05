# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""empty message

Revision ID: db0151dc70c3
Revises: c608d8fec07d
Create Date: 2022-08-26 11:12:09.630059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "db0151dc70c3"
down_revision = "c608d8fec07d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("apikey", sa.String(length=256), nullable=True))
    op.create_unique_constraint(None, "user", ["apikey"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="unique")
    op.drop_column("user", "apikey")
    # ### end Alembic commands ###
