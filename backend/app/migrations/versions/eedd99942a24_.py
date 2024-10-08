# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Add field for accuracy unit.

Revision ID: eedd99942a24
Revises: 59f942848b0e
Create Date: 2023-12-01 13:10:00.265575

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "eedd99942a24"
down_revision = "59f942848b0e"
branch_labels = None
depends_on = None


def upgrade():
    """Run the database changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("device_property", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("accuracy_unit_uri", sa.String(length=256), nullable=True)
        )
        batch_op.add_column(
            sa.Column("accuracy_unit_name", sa.String(length=256), nullable=True)
        )
    # ### end Alembic commands ###


def downgrade():
    """Undo the database changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("device_property", schema=None) as batch_op:
        batch_op.drop_column("accuracy_unit_name")
        batch_op.drop_column("accuracy_unit_uri")
    # ### end Alembic commands ###
