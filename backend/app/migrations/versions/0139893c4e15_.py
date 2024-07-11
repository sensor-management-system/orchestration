# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Set active attribute to True for contacts and users.

Revision ID: 0139893c4e15
Revises: c1d164f8d5d8
Create Date: 2021-09-16 08:35:56.991907

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0139893c4e15"
down_revision = "c1d164f8d5d8"
branch_labels = None
depends_on = None


def upgrade():
    op.execute('UPDATE "user" SET active = true WHERE active IS NULL')
    op.execute('UPDATE "contact" SET active = true WHERE active IS NULL')


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
