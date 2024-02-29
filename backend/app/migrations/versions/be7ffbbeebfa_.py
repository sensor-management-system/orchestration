# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add image tables for configurations, platforms and sites.

Revision ID: be7ffbbeebfa
Revises: 4be0faa034c9
Create Date: 2024-01-31 08:02:30.131299

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "be7ffbbeebfa"
down_revision = "4be0faa034c9"
branch_labels = None
depends_on = None


def upgrade():
    """Run the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "platform_image",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("platform_id", sa.Integer(), nullable=False),
        sa.Column("attachment_id", sa.Integer(), nullable=False),
        sa.Column("order_index", sa.BigInteger(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["attachment_id"],
            ["platform_attachment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_PlatformImage_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_PlatformImage_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "site_image",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), nullable=False),
        sa.Column("attachment_id", sa.Integer(), nullable=False),
        sa.Column("order_index", sa.BigInteger(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["attachment_id"],
            ["site_attachment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_SiteImage_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["site.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_SiteImage_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "configuration_image",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("configuration_id", sa.Integer(), nullable=False),
        sa.Column("attachment_id", sa.Integer(), nullable=False),
        sa.Column("order_index", sa.BigInteger(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["attachment_id"],
            ["configuration_attachment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["configuration_id"],
            ["configuration.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_ConfigurationImage_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_ConfigurationImage_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    """Undo the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("configuration_image")
    op.drop_table("site_image")
    op.drop_table("platform_image")
    # ### end Alembic commands ###
