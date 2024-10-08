# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Add created & updated info to device properties.

Revision ID: aa0dc5b7060d
Revises: 0ab9f982e07c
Create Date: 2023-04-05 11:34:58.596439

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "aa0dc5b7060d"
down_revision = "0ab9f982e07c"
branch_labels = None
depends_on = None


def upgrade():
    """Introduce the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("device_property", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
        )
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
        )
        batch_op.add_column(sa.Column("created_by_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("updated_by_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_DeviceProperty_updated_by_id",
            "user",
            ["updated_by_id"],
            ["id"],
            use_alter=True,
        )
        batch_op.create_foreign_key(
            "fk_DeviceProperty_created_by_id",
            "user",
            ["created_by_id"],
            ["id"],
            use_alter=True,
        )
    # Set the created by field automatically.
    conn = op.get_bind()

    conn.execute(
        text(
            """
            update device_property
            set created_at = now()
            where created_at is null
            """
        )
    )
    # ### end Alembic commands ###


def downgrade():
    """Undo the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("device_property", schema=None) as batch_op:
        batch_op.drop_constraint("fk_DeviceProperty_created_by_id", type_="foreignkey")
        batch_op.drop_constraint("fk_DeviceProperty_updated_by_id", type_="foreignkey")
        batch_op.drop_column("updated_by_id")
        batch_op.drop_column("created_by_id")
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")
    # ### end Alembic commands ###
