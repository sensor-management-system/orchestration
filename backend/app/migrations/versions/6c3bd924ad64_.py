# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Make attributes mandatory for:
    - label in attachment
    - property_name in device_property

Revision ID: 6c3bd924ad64
Revises: 13e35f226a7c
Create Date: 2022-05-17 10:57:15.784743

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "6c3bd924ad64"
down_revision = "13e35f226a7c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Fill the Empty Field if it needed to make them mandatory.

    op.execute(
        "UPDATE configuration_attachment SET label= 'Please change this label' WHERE label IS NULL"
    )
    op.execute(
        "UPDATE device_attachment SET label='Please change this label' WHERE label IS NULL"
    )
    op.execute(
        "UPDATE platform_attachment SET label='Please change this label' WHERE label IS NULL"
    )
    op.execute(
        "UPDATE device_property SET property_name ='Please change this property' WHERE property_name IS NULL"
    )
    op.alter_column(
        "configuration_attachment",
        "label",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )
    op.alter_column(
        "device_attachment",
        "label",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )
    op.alter_column(
        "device_property",
        "property_name",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )
    op.alter_column(
        "platform_attachment",
        "label",
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "platform_attachment",
        "label",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    op.alter_column(
        "device_property",
        "property_name",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    op.alter_column(
        "device_attachment",
        "label",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    op.alter_column(
        "configuration_attachment",
        "label",
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
    )
    # ### end Alembic commands ###
