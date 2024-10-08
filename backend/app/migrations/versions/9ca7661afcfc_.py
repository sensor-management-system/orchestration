# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""empty message

Revision ID: 9ca7661afcfc
Revises: 910f941f151b
Create Date: 2022-10-27 10:38:03.327788

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2.types


# revision identifiers, used by Alembic.
revision = "9ca7661afcfc"
down_revision = "910f941f151b"
branch_labels = None
depends_on = None

# See https://geoalchemy-2.readthedocs.io/en/latest/alembic.html#alembic-use


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "site",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("label", sa.String(length=256), nullable=True),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(
                geometry_type="POLYGON", from_text="ST_GeomFromEWKT", name="geometry"
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("site")
    # ### end Alembic commands ###
