# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Set default values:
 - {configuration, device, platform} is_internal -> True
 - {configuration, device, platform} is_public -> False
 - {device, platform} is_private -> False
 - {user} is_superuser -> False

Revision ID: 13e35f226a7c
Revises: 12e34f225a6c
Create Date: 2021-09-29 07:29:59.046318

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "13e35f226a7c"
down_revision = "12e34f225a6c"
branch_labels = None
depends_on = None


def upgrade():
    op.execute('UPDATE "user" SET is_superuser = false WHERE is_superuser IS NULL')

    op.execute(
        'UPDATE "configuration" SET is_internal = true WHERE is_internal IS NULL'
    )
    op.execute('UPDATE "device" SET is_internal = true WHERE is_internal IS NULL')
    op.execute('UPDATE "platform" SET is_internal = true WHERE is_internal IS NULL')

    op.execute('UPDATE "device" SET is_private = false WHERE is_private IS NULL')
    op.execute('UPDATE "platform" SET is_private = false WHERE is_private IS NULL')

    op.execute('UPDATE "configuration" SET is_public = false WHERE is_public IS NULL')
    op.execute('UPDATE "device" SET is_public = false WHERE is_public IS NULL')
    op.execute('UPDATE "platform" SET is_public = false WHERE is_public IS NULL')


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###