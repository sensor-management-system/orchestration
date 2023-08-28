# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Fix the GFZ organization name.

Revision ID: 3dcc10ac1814
Revises: 8edba7b2296a
Create Date: 2023-07-27 13:44:01.938743

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3dcc10ac1814"
down_revision = "8edba7b2296a"
branch_labels = None
depends_on = None


def upgrade():
    """Run the migration."""
    update_query = """
    update contact
    set organization = :new_organization
    where organization = :old_organization
    """

    organization_changes = [
        # (old, new)
        (
            "Helmholtz Centre Potsdam - German Research Centre for Geosciences GFZ",
            "Helmholtz Centre Potsdam German Research Centre for Geosciences GFZ",
        ),
    ]

    conn = op.get_bind()
    for old_organization, new_organization in organization_changes:
        conn.execute(
            sa.text(update_query),
            old_organization=old_organization,
            new_organization=new_organization,
        )


def downgrade():
    """Pass."""
    pass
