# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Merge Configuration begin and end Location Action

Revision ID: 2c77c77a37cb
Revises: a12c9bcfbfdb
Create Date: 2022-07-18 08:32:04.003052

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2c77c77a37cb"
down_revision = "a12c9bcfbfdb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "configuration_dynamic_location_begin_action",
        "description",
        new_column_name="begin_description",
    )
    op.drop_constraint(
        "configuration_dynamic_location_begin_action_contact_id_fkey",
        "configuration_dynamic_location_begin_action",
        type_="foreignkey",
    )
    op.alter_column(
        "configuration_dynamic_location_begin_action",
        "contact_id",
        new_column_name="begin_contact_id",
    )
    op.add_column(
        "configuration_dynamic_location_begin_action",
        sa.Column("end_date", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "configuration_dynamic_location_begin_action",
        sa.Column("end_description", sa.Text(), nullable=True),
    )
    op.add_column(
        "configuration_dynamic_location_begin_action",
        sa.Column("end_contact_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        None,
        "configuration_dynamic_location_begin_action",
        "contact",
        ["end_contact_id"],
        ["id"],
    )
    op.create_foreign_key(
        None,
        "configuration_dynamic_location_begin_action",
        "contact",
        ["begin_contact_id"],
        ["id"],
    )

    op.alter_column(
        "configuration_static_location_begin_action",
        "description",
        new_column_name="begin_description",
    )
    op.drop_constraint(
        "configuration_static_location_begin_action_contact_id_fkey",
        "configuration_static_location_begin_action",
        type_="foreignkey",
    )
    op.alter_column(
        "configuration_static_location_begin_action",
        "contact_id",
        new_column_name="begin_contact_id",
    )
    op.add_column(
        "configuration_static_location_begin_action",
        sa.Column("end_date", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "configuration_static_location_begin_action",
        sa.Column("end_description", sa.Text(), nullable=True),
    )
    op.add_column(
        "configuration_static_location_begin_action",
        sa.Column("end_contact_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        None,
        "configuration_static_location_begin_action",
        "contact",
        ["end_contact_id"],
        ["id"],
    )
    op.create_foreign_key(
        None,
        "configuration_static_location_begin_action",
        "contact",
        ["begin_contact_id"],
        ["id"],
    )

    # And now we migrate our existing end location actions data to the begin location actions entries
    # The overall idea is to find the latest begin action before the current end action, so
    # that we then can fill the (new) end fields in the begin actions.
    conn = op.get_bind()

    static_begin_lookup = {}
    configuration_static_location_begin_actions = conn.execute(
        text(
            "select id, configuration_id, begin_date from configuration_static_location_begin_action"
        )
    )
    for row in configuration_static_location_begin_actions:
        key = row["configuration_id"]
        static_begin_lookup.setdefault(key, [])
        static_begin_lookup[key].append(row)

    # Now we can go through the end dates, find the associated start action & then
    # update it accordingly.
    configuration_static_location_end_actions = conn.execute(
        text(
            "select configuration_id, end_date, description, contact_id from configuration_static_location_end_action order by end_date"
        )
    )
    for row in configuration_static_location_end_actions:
        key = row["configuration_id"]
        # Find the begin action for our configuration.
        begin_actions = static_begin_lookup.get(key, [])
        begin_actions = [x for x in begin_actions if x["begin_date"] <= row["end_date"]]
        # Sort them from the earliest to the latest.
        begin_actions.sort(key=lambda x: x["begin_date"])
        if begin_actions:
            begin_action = begin_actions[-1]
            update_query = text(
                """
            update configuration_static_location_begin_action
            set end_date = :end_date,
                end_contact_id = :contact_id,
                end_description = :description
            where id = :id
            """
            )
            conn.execute(
                update_query,
                {
                    "id": begin_action["id"],
                    "end_date": row["end_date"],
                    "contact_id": row["contact_id"],
                    "description": row["description"],
                },
            )

    dynamic_begin_lookup = {}
    configuration_dynamic_location_begin_actions = conn.execute(
        text(
            "select id, configuration_id, begin_date from configuration_dynamic_location_begin_action"
        )
    )
    for row in configuration_dynamic_location_begin_actions:
        key = row["configuration_id"]
        dynamic_begin_lookup.setdefault(key, [])
        dynamic_begin_lookup[key].append(row)

    # Now we can go through the end dates, find the associated start action & then
    # update it accordingly.
    configuration_dynamic_location_end_actions = conn.execute(
        text(
            "select configuration_id, end_date, description, contact_id from configuration_dynamic_location_end_action order by end_date"
        )
    )
    for row in configuration_dynamic_location_end_actions:
        key = row["configuration_id"]
        begin_actions = dynamic_begin_lookup.get(key, [])
        begin_actions = [x for x in begin_actions if x["begin_date"] <= row["end_date"]]
        begin_actions.sort(key=lambda x: x["begin_date"])
        if begin_actions:
            begin_action = begin_actions[-1]
            update_query = text(
                """
            update configuration_dynamic_location_begin_action
            set end_date = :end_date,
                end_contact_id = :contact_id,
                end_description = :description
            where id = :id
            """
            )
            conn.execute(
                update_query,
                {
                    "id": begin_action["id"],
                    "end_date": row["end_date"],
                    "contact_id": row["contact_id"],
                    "description": row["description"],
                },
            )

    op.drop_table("configuration_static_location_end_action")
    op.drop_table("configuration_dynamic_location_end_action")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Recreate the configuration_dynamic_location_end_action table
    # and the configuration_static_location_end_action table
    op.create_table(
        "configuration_dynamic_location_end_action",
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "configuration_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "end_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("contact_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("created_by_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("updated_by_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["configuration_id"],
            ["configuration.id"],
            name="configuration_dynamic_location_end_action_configuration_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
            name="configuration_dynamic_location_end_action_contact_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_ConfigurationDynamicLocationEndAction_created_by_id",
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_ConfigurationDynamicLocationEndAction_updated_by_id",
        ),
        sa.PrimaryKeyConstraint(
            "id", name="configuration_dynamic_location_end_action_pkey"
        ),
    )
    op.create_table(
        "configuration_static_location_end_action",
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "configuration_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "end_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("contact_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("created_by_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("updated_by_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["configuration_id"],
            ["configuration.id"],
            name="configuration_static_location_end_action_configuration_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
            name="configuration_static_location_end_action_contact_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_ConfigurationStaticLocationEndAction_created_by_id",
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_ConfigurationStaticLocationEndAction_updated_by_id",
        ),
        sa.PrimaryKeyConstraint(
            "id", name="configuration_static_location_end_action_pkey"
        ),
    )
    conn = op.get_bind()
    insert_query = text(
        """
    insert into configuration_static_location_end_action (
        configuration_id, end_date,
        contact_id, description
    )
    select configuration_id, end_date, end_contact_id, end_description
    from configuration_static_location_end_action
    where end_date is not null and end_contact_id is not null
    """
    )
    conn.execute(insert_query)
    insert_query = text(
        """
    insert into configuration_dynamic_location_end_action (
        configuration_id, end_date,
        contact_id, description
    )
    select configuration_id, end_date, end_contact_id, end_description
    from configuration_dynamic_location_end_action
    where end_date is not null and end_contact_id is not null
    """
    )
    conn.execute(insert_query)

    # Alter the column names:
    # - begin_description to description
    # - begin_contact_id to contact_id
    op.drop_constraint(
        None, "configuration_static_location_begin_action", type_="foreignkey"
    )
    op.drop_constraint(
        None, "configuration_dynamic_location_begin_action", type_="foreignkey"
    )
    op.alter_column(
        "configuration_static_location_end_action",
        "begin_contact_id",
        new_column_name="contact_id",
    )
    op.alter_column(
        "configuration_dynamic_location_end_action",
        "begin_contact_id",
        new_column_name="contact_id",
    )
    op.alter_column(
        "configuration_static_location_end_action",
        "begin_description",
        new_column_name="description",
    )
    op.alter_column(
        "configuration_dynamic_location_end_action",
        "begin_description",
        new_column_name="description",
    )
    op.create_foreign_key(
        "configuration_static_location_begin_action_contact_id_fkey",
        "configuration_static_location_begin_action",
        "contact",
        ["contact_id"],
        ["id"],
    )
    op.create_foreign_key(
        "configuration_dynamic_location_begin_action_contact_id_fkey",
        "configuration_dynamic_location_begin_action",
        "contact",
        ["contact_id"],
        ["id"],
    )
    op.drop_column("configuration_static_location_begin_action", "end_contact_id")
    op.drop_column("configuration_static_location_begin_action", "end_description")
    op.drop_column("configuration_static_location_begin_action", "end_date")

    op.drop_column("configuration_dynamic_location_begin_action", "end_contact_id")
    op.drop_column("configuration_dynamic_location_begin_action", "end_description")
    op.drop_column("configuration_dynamic_location_begin_action", "end_date")

    # ### end Alembic commands ###