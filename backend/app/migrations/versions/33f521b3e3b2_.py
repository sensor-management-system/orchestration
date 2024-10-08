# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Add unique constraints for contact roles.

Revision ID: 33f521b3e3b2
Revises: 245e3bb72f1e
Create Date: 2023-11-14 17:28:09.138133

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "33f521b3e3b2"
down_revision = "245e3bb72f1e"
branch_labels = None
depends_on = None


def upgrade():
    """Add the unique constraints."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("configuration_contact_role", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            None, ["contact_id", "configuration_id", "role_name", "role_uri"]
        )

    with op.batch_alter_table("device_contact_role", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            None, ["contact_id", "device_id", "role_name", "role_uri"]
        )

    with op.batch_alter_table("platform_contact_role", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            None, ["contact_id", "platform_id", "role_name", "role_uri"]
        )

    with op.batch_alter_table("site_contact_role", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            None, ["contact_id", "site_id", "role_name", "role_uri"]
        )
    # ### end Alembic commands ###


def downgrade():
    """Remove the unique constraints."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("site_contact_role", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    with op.batch_alter_table("platform_contact_role", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    with op.batch_alter_table("device_contact_role", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    with op.batch_alter_table("configuration_contact_role", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")
    # ### end Alembic commands ###
