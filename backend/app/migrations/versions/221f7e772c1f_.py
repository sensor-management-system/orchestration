# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add campaign field to configurations.

Revision ID: 221f7e772c1f
Revises: 57a2cf393a6b
Create Date: 2024-04-05 05:55:52.491783

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "221f7e772c1f"
down_revision = "57a2cf393a6b"
branch_labels = None
depends_on = None


def upgrade():
    """Do the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("configuration", schema=None) as batch_op:
        batch_op.add_column(sa.Column("campaign", sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    """Undo the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("configuration", schema=None) as batch_op:
        batch_op.drop_column("campaign")
    # ### end Alembic commands ###
