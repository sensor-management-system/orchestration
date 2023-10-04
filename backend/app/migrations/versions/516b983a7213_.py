# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Migrate the sampling media weather to air.

Revision ID: 516b983a7213
Revises: c27a6569c395
Create Date: 2023-09-28 12:28:58.638341

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "516b983a7213"
down_revision = "c27a6569c395"
branch_labels = None
depends_on = None


def upgrade():
    """Update the sampling media name value to Air."""
    op.execute(
        "UPDATE device_property set sampling_media_name='Air' where sampling_media_name='Weather'"
    )


def downgrade():
    """Reset the sampling media name value to Weather."""
    op.execute(
        "UPDATE device_property set sampling_media_name='Weather' where sampling_media_name='Air'"
    )
