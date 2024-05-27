# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Add {group_ids, is_private, is_superuser} attributes

Revision ID: 12e34f225a6c
Revises: 0139893c4e15
Create Date: 2021-09-29 07:29:59.046318

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "12e34f225a6c"
down_revision = "7b504fcc359b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "configuration", sa.Column("cfg_permission_group", sa.String(), nullable=True)
    )
    op.add_column(
        "configuration", sa.Column("is_internal", sa.Boolean(), nullable=True)
    )
    op.add_column("configuration", sa.Column("is_public", sa.Boolean(), nullable=True))

    op.add_column(
        "device", sa.Column("group_ids", sa.ARRAY(sa.String()), nullable=True)
    )
    op.add_column("device", sa.Column("is_private", sa.Boolean(), nullable=True))
    op.add_column("device", sa.Column("is_internal", sa.Boolean(), nullable=True))
    op.add_column("device", sa.Column("is_public", sa.Boolean(), nullable=True))

    op.add_column(
        "platform", sa.Column("group_ids", sa.ARRAY(sa.String()), nullable=True)
    )
    op.add_column("platform", sa.Column("is_private", sa.Boolean(), nullable=True))
    op.add_column("platform", sa.Column("is_internal", sa.Boolean(), nullable=True))
    op.add_column("platform", sa.Column("is_public", sa.Boolean(), nullable=True))

    op.add_column("user", sa.Column("is_superuser", sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "is_superuser")

    op.drop_column("platform", "is_public")
    op.drop_column("platform", "is_internal")
    op.drop_column("platform", "is_private")
    op.drop_column("platform", "group_ids")

    op.drop_column("device", "is_public")
    op.drop_column("device", "is_internal")
    op.drop_column("device", "is_private")
    op.drop_column("device", "group_ids")

    op.drop_column("configuration", "is_public")
    op.drop_column("configuration", "is_internal")
    op.drop_column("configuration", "cfg_permission_group")
    # ### end Alembic commands ###
