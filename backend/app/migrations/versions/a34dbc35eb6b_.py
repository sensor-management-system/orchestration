# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Luca Johannes Nendel <luca-johannes.nendel@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Adjust to match Metadata Schema for the Persistent Identification
of Scientific Measuring Instruments
https://github.com/rdawg-pidinst/schema/blob/master/schema.rst#identtype

Revision ID: a34dbc35eb6b
Revises: a12c9bcfbfdb
Create Date: 2022-07-11 09:30:44.529870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a34dbc35eb6b"
down_revision = "e1cac965237f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "device", sa.Column("identifier_type", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "device", sa.Column("schema_version", sa.String(length=256), nullable=True)
    )
    op.alter_column(
        "device",
        "manufacturer_name",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )

    op.add_column(
        "platform", sa.Column("identifier_type", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "platform", sa.Column("schema_version", sa.String(length=256), nullable=True)
    )
    op.alter_column(
        "platform",
        "manufacturer_name",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "device",
        "manufacturer_name",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    op.drop_column("device", "schema_version")
    op.drop_column("device", "identifier_type")

    op.alter_column(
        "platform",
        "manufacturer_name",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    op.drop_column("platform", "schema_version")
    op.drop_column("platform", "identifier_type")
    # ### end Alembic commands ###
