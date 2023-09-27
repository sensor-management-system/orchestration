# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0


"""Set the organzation names.

Revision ID: 5505aacc0cea
Revises: 0410c9cbc6cf
Create Date: 2023-05-15 12:27:29.978489

"""
import json
import pathlib

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5505aacc0cea"
down_revision = "0410c9cbc6cf"
branch_labels = None
depends_on = None


def upgrade():
    """Set the organzation names."""
    organization_names_file = (
        pathlib.Path(__file__).parent.parent.parent
        / "project"
        / "static"
        / "organization_names.json"
    )
    organization_names = json.load(organization_names_file.open())

    select_query = """
    select id, email
    from contact
    where organization is null or organization = ''
    """

    update_query = """
    update contact
    set organization = :organization
    where id = :id
    """

    conn = op.get_bind()
    for row in conn.execute(sa.text(select_query)):
        id_ = row["id"]
        email = row["email"]
        domain = email.split("@")[-1]
        if domain in organization_names.keys():
            organization = organization_names[domain]
            conn.execute(sa.text(update_query), organization=organization, id=id_)


def downgrade():
    """Don't to anything."""
    pass
