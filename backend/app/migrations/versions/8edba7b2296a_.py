# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2
"""Create table for site attachments.

Revision ID: 8edba7b2296a
Revises: 8ee5de834c21
Create Date: 2023-07-21 07:24:56.201176

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8edba7b2296a"
down_revision = "8ee5de834c21"
branch_labels = None
depends_on = None


def upgrade():
    """Run the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "site_attachment",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=256), nullable=False),
        sa.Column("url", sa.String(length=1024), nullable=False),
        sa.Column("internal_url", sa.String(length=1024), nullable=True),
        sa.Column("site_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_SiteAttachment_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["site.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_SiteAttachment_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    """Undo the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("site_attachment")
    # ### end Alembic commands ###
