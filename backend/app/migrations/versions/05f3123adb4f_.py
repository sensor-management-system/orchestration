# SPDX-FileCopyrightText: 2025
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Update the GFZ contact entries.

Revision ID: 05f3123adb4f
Revises: dd8dc3644fdd
Create Date: 2025-01-31 14:37:57.336145

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "05f3123adb4f"
down_revision = "dd8dc3644fdd"
branch_labels = None
depends_on = None


def upgrade():
    """Do the data upgrade."""
    op.execute(
        """
        update "contact"
        set organization = 'GFZ Helmholtz Centre for Geosciences'
        where organization = 'Helmholtz Centre Potsdam - German Research Centre for Geosciences GFZ'
        """
    )
    op.execute(
        r"""
        update "contact"
        set email = replace(email, 'gfz-potsdam.de', 'gfz.de')
        where email like '%@gfz-potsdam.de'
        and replace(email, 'gfz-potsdam.de', 'gfz.de') not in (
            select email from "contact"
        )
        """
    )


def downgrade():
    """Can't undo the db changes."""
    pass
