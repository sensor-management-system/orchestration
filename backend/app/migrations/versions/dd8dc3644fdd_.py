# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Add a model for involved devices in datastream links.

Revision ID: dd8dc3644fdd
Revises: 609c600e4c0f
Create Date: 2024-08-16 06:26:46.741108

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "dd8dc3644fdd"
down_revision = "609c600e4c0f"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "involved_device_for_datastream_link",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("datastream_link_id", sa.Integer(), nullable=False),
        sa.Column("order_index", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["datastream_link_id"],
            ["datastream_link.id"],
        ),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["device.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    """Undo the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("involved_device_for_datastream_link")
    # ### end Alembic commands ###
