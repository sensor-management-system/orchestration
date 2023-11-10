# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add a field for the country of devices & platforms.

Revision ID: 245e3bb72f1e
Revises: bd274b605cae
Create Date: 2023-10-11 07:38:44.311107

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "245e3bb72f1e"
down_revision = "3fc79d899f8b"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("device", schema=None) as batch_op:
        batch_op.add_column(sa.Column("country", sa.String(length=256), nullable=True))

    with op.batch_alter_table("platform", schema=None) as batch_op:
        batch_op.add_column(sa.Column("country", sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    """Undo the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("device", schema=None) as batch_op:
        batch_op.drop_column("country")
    with op.batch_alter_table("platform", schema=None) as batch_op:
        batch_op.drop_column("country")
    # ### end Alembic commands ###
