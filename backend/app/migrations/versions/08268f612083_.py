# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add field to store date when user agreed on terms of use.

Revision ID: 08268f612083
Revises: c0d89a7e62cc
Create Date: 2023-03-03 11:09:31.006359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "08268f612083"
down_revision = "c0d89a7e62cc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "terms_of_use_agreement_date", sa.DateTime(timezone=True), nullable=True
            )
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("terms_of_use_agreement_date")
    # ### end Alembic commands ###