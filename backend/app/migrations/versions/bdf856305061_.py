# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Remove all permission group membership duplicates.

Revision ID: bdf856305061
Revises: 6dd344b64fa2
Create Date: 2026-08-04 06:53:47.021648

"""
import dataclasses

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bdf856305061"
down_revision = "6dd344b64fa2"
branch_labels = None
depends_on = None


@dataclasses.dataclass(frozen=True)
class PermissionGroupMembershipRow:
    """Data class for a set of id combinations."""

    user_id: int
    permission_group_id: int


def upgrade():
    """Remove the duplicated group memberships and add a constraint."""
    connection = op.get_bind()

    select_query = """
    select id, user_id, permission_group_id
    from permission_group_membership
    """

    rows_to_keep = set()
    ids_to_delete = set()
    for res in connection.execute(sa.text(select_query)).fetchall():
        row = PermissionGroupMembershipRow(
            user_id=res["user_id"],
            permission_group_id=res["permission_group_id"],
        )
        if row not in rows_to_keep:
            rows_to_keep.add(row)
        else:
            ids_to_delete.add(res["id"])

    for id in ids_to_delete:
        delete_query = "delete from permission_group_membership where id = :id"
        connection.execute(sa.text(delete_query), {"id": id})

    with op.batch_alter_table("permission_group_membership", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["user_id", "permission_group_id"])


def downgrade():
    """Remove the constraint."""
    with op.batch_alter_table("permission_group_membership", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")
