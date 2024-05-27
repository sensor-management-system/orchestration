# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Add created_at field to the manufacturer models.

This has the reason that we want to keep track when
those entries where added.

Revision ID: f23da62d05a9
Revises: 221f7e772c1f
Create Date: 2024-04-26 09:27:57.084443

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f23da62d05a9"
down_revision = "221f7e772c1f"
branch_labels = None
depends_on = None


def upgrade():
    """Run the database structure migration."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("manufacturer_model", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
        )
    # ### end Alembic commands ###
    # And we also need to set the created_at for the current entries
    conn = op.get_bind()
    conn.execute(
        'update "manufacturer_model" set created_at = now() where created_at is null'
    )


def downgrade():
    """Undo the database structure migration."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("manufacturer_model", schema=None) as batch_op:
        batch_op.drop_column("created_at")
    # ### end Alembic commands ###
