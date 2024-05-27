# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Allow parent devices for device mount actions.

Revision ID: 5ada23855e3c
Revises: bd274b605cae
Create Date: 2023-10-26 06:33:56.652219

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5ada23855e3c"
down_revision = "bd274b605cae"
branch_labels = None
depends_on = None


def upgrade():
    """Run the database structure changes."""
    with op.batch_alter_table("device_mount_action", schema=None) as batch_op:
        batch_op.add_column(sa.Column("parent_device_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, "device", ["parent_device_id"], ["id"])


def downgrade():
    """Undo the database structure changes."""
    with op.batch_alter_table("device_mount_action", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("parent_device_id")
