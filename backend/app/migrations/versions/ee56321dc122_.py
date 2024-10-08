# SPDX-FileCopyrightText: 2020
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""empty message

Revision ID: ee56321dc122
Revises: be02e5b01611
Create Date: 2020-09-29 13:43:59.238177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ee56321dc122"
down_revision = "be02e5b01611"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "configuration", sa.Column("status", sa.String(length=256), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("configuration", "status")
    # ### end Alembic commands ###
