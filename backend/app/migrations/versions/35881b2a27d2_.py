# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""empty message

Revision ID: 35881b2a27d2
Revises: a34dbc35eb6b
Create Date: 2022-10-14 05:42:25.055678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "35881b2a27d2"
down_revision = "a34dbc35eb6b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contact", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "contact", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("contact", sa.Column("created_by_id", sa.Integer(), nullable=True))
    op.add_column("contact", sa.Column("updated_by_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_Contact_updated_by_id",
        "contact",
        "user",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )
    op.create_foreign_key(
        "fk_Contact_created_by_id",
        "contact",
        "user",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_Contact_created_by_id", "contact", type_="foreignkey")
    op.drop_constraint("fk_Contact_updated_by_id", "contact", type_="foreignkey")
    op.drop_column("contact", "updated_by_id")
    op.drop_column("contact", "created_by_id")
    op.drop_column("contact", "updated_at")
    op.drop_column("contact", "created_at")
    # ### end Alembic commands ###
