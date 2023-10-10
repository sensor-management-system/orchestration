# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0
"""Add some more description fields.

Revision ID: bd274b605cae
Revises: c27a6569c395
Create Date: 2023-09-06 06:26:13.982020

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bd274b605cae"
down_revision = "426aab825deb"
branch_labels = None
depends_on = None


def upgrade():
    """Add the description fields."""
    with op.batch_alter_table("configuration_attachment", schema=None) as batch_op:
        batch_op.add_column(sa.Column("description", sa.Text(), nullable=True))

    with op.batch_alter_table("configuration_custom_field", schema=None) as batch_op:
        batch_op.add_column(sa.Column("description", sa.Text(), nullable=True))

    with op.batch_alter_table("custom_field", schema=None) as batch_op:
        batch_op.add_column(sa.Column("description", sa.Text(), nullable=True))

    with op.batch_alter_table("device_attachment", schema=None) as batch_op:
        batch_op.add_column(sa.Column("description", sa.Text(), nullable=True))

    with op.batch_alter_table("device_property", schema=None) as batch_op:
        batch_op.add_column(sa.Column("description", sa.Text(), nullable=True))

    with op.batch_alter_table("platform_attachment", schema=None) as batch_op:
        batch_op.add_column(sa.Column("description", sa.Text(), nullable=True))

    with op.batch_alter_table("site_attachment", schema=None) as batch_op:
        batch_op.add_column(sa.Column("description", sa.Text(), nullable=True))


def downgrade():
    """Remove the description fields."""
    with op.batch_alter_table("site_attachment", schema=None) as batch_op:
        batch_op.drop_column("description")

    with op.batch_alter_table("platform_attachment", schema=None) as batch_op:
        batch_op.drop_column("description")

    with op.batch_alter_table("device_property", schema=None) as batch_op:
        batch_op.drop_column("description")

    with op.batch_alter_table("device_attachment", schema=None) as batch_op:
        batch_op.drop_column("description")

    with op.batch_alter_table("custom_field", schema=None) as batch_op:
        batch_op.drop_column("description")

    with op.batch_alter_table("configuration_custom_field", schema=None) as batch_op:
        batch_op.drop_column("description")

    with op.batch_alter_table("configuration_attachment", schema=None) as batch_op:
        batch_op.drop_column("description")
