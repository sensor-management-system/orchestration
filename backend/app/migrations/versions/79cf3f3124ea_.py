# SPDX-FileCopyrightText: 2025
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Migrate the idl data to the backend db.

Revision ID: 79cf3f3124ea
Revises: 6e868471e774
Create Date: 2025-11-03 07:09:16.721613

"""
import os

import requests
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "79cf3f3124ea"
down_revision = "6e868471e774"
branch_labels = None
depends_on = None


def upgrade():
    """Query the idl and include the data here in the database."""
    idl_url = os.environ.get("IDL_URL")
    idl_token = os.environ.get("SMS_IDL_TOKEN")

    if not idl_url or not idl_token:

        return

    all_permission_groups_response = requests.get(
        f"{idl_url}/permission-groups",
        {"itemsPerPage": 100_000},
        headers={"Authorization": f"Bearer {idl_token}"},
    )
    all_permission_groups_response.raise_for_status()
    all_permission_groups = all_permission_groups_response.json()

    all_user_accounts_response = requests.get(
        f"{idl_url}/user-accounts",
        {"itemsPerPage": 100_000},
        headers={"Authorization": f"Bearer {idl_token}"},
    )
    all_user_accounts_response.raise_for_status()
    all_user_accounts = all_user_accounts_response.json()

    connection = op.get_bind()

    largest_id = 1

    for pm in all_permission_groups:
        insert_query = """
        insert into permission_group
        (id, name, entitlement)
        values
        (:id, :name, :entitlement)
        """

        current_id = int(pm["id"])
        connection.execute(
            sa.text(insert_query),
            {"id": current_id, "name": pm["name"], "entitlement": pm["entitlement"]},
        )

        if current_id > largest_id:
            largest_id = current_id

    # The true adds one to the given value.
    sequence_update_query = """
    select setval('permission_group_id_seq', :id, true);
    """
    connection.execute(sa.text(sequence_update_query), {"id": largest_id})

    for ua in all_user_accounts:
        select_query = 'select id from "user" where subject = :name limit 1'
        cursor = connection.execute(sa.text(select_query), {"name": ua["userName"]})
        res = cursor.fetchall()
        user_id = res[0][0]

        idl_groups_to_add_to = set()
        for entry in [
            *ua["administratedPermissionGroups"],
            *ua["memberedPermissionGroups"],
        ]:
            idl_groups_to_add_to.add(entry)

        insert_query = """
        insert into permission_group_membership
        (permission_group_id, user_id)
        values
        (:permission_group_id, :user_id)
        """

        for group_id in idl_groups_to_add_to:
            connection.execute(
                sa.text(insert_query),
                {"permission_group_id": group_id, "user_id": user_id},
            )


def downgrade():
    """Remote the idl data again."""
    connection = op.get_bind()
    connection.execute("delete from permission_group_membership")
    connection.execute("delete from permission_group")
