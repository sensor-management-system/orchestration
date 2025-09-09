# SPDX-FileCopyrightText: 2025
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Update the urls for the gfz sms instance.

Revision ID: a57af9d062a7
Revises: 158e84e3bc41
Create Date: 2025-09-08 07:55:26.560280

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "a57af9d062a7"
down_revision = "158e84e3bc41"
branch_labels = None
depends_on = None


def upgrade():
    """Update the internal urls so that they point to the gfz without -potsdam."""
    for table in [
        "device_attachment",
        "platform_attachment",
        "configuration_attachment",
        "site_attachment",
        "export_control_attachment",
    ]:
        op.execute(
            f"""
            update "{table}"
            set url = replace(url, 'gfz-potsdam.de', 'gfz.de')
            where url ilike '%gfz-potsdam.de%'
            """
        )


def downgrade():
    """Skip the downgrade."""
    pass
