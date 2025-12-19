# SPDX-FileCopyrightText: 2025
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Remove a possible existing non null check for manufacturer names.

Revision ID: bd8274140ca7
Revises: a57af9d062a7
Create Date: 2025-12-18 14:36:31.347486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bd8274140ca7"
down_revision = "a57af9d062a7"
branch_labels = None
depends_on = None


def upgrade():
    """Remove the non null constraint."""
    with op.batch_alter_table("device", schema=None) as batch_op:
        batch_op.alter_column(
            "manufacturer_name", existing_type=sa.VARCHAR(length=256), nullable=True
        )

    with op.batch_alter_table("platform", schema=None) as batch_op:
        batch_op.alter_column(
            "manufacturer_name", existing_type=sa.VARCHAR(length=256), nullable=True
        )


def downgrade():
    """Do nothing."""
    pass
