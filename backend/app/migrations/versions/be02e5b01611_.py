# SPDX-FileCopyrightText: 2020
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""empty message

Revision ID: be02e5b01611
Revises: 485380cc62eb
Create Date: 2020-09-29 12:34:57.019786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "be02e5b01611"
down_revision = "485380cc62eb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "configuration", sa.Column("label", sa.String(length=256), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("configuration", "label")
    # ### end Alembic commands ###
