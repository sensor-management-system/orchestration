# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Add explicit model for export control and their attachments.

Revision ID: 0a0a316932e7
Revises: be7ffbbeebfa
Create Date: 2024-03-01 08:31:25.201011

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0a0a316932e7"
down_revision = "be7ffbbeebfa"
branch_labels = None
depends_on = None


def upgrade():
    """Run the database structure changes."""
    op.create_table(
        "manufacturer_model",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("manufacturer_name", sa.String(length=256), nullable=False),
        sa.Column("model", sa.String(length=256), nullable=False),
        sa.Column("external_system_name", sa.String(length=256), nullable=True),
        sa.Column("external_system_url", sa.String(length=256), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "export_control",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("dual_use", sa.Boolean(), nullable=True),
        sa.Column(
            "export_control_classification_number", sa.String(length=256), nullable=True
        ),
        sa.Column("customs_tariff_number", sa.String(length=256), nullable=True),
        sa.Column("additional_information", sa.Text(), nullable=True),
        sa.Column("internal_note", sa.Text(), nullable=True),
        sa.Column("manufacturer_model_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_ExportControl_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["manufacturer_model_id"],
            ["manufacturer_model.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_ExportControl_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "export_control_attachment",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("label", sa.String(length=256), nullable=False),
        sa.Column("url", sa.String(length=1024), nullable=False),
        sa.Column("internal_url", sa.String(length=1024), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_export_control_only", sa.Boolean(), nullable=True),
        sa.Column("manufacturer_model_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name="fk_ExportControlAttachment_created_by_id",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(
            ["manufacturer_model_id"],
            ["manufacturer_model.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_id"],
            ["user.id"],
            name="fk_ExportControlAttachment_updated_by_id",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    with op.batch_alter_table("device", schema=None) as batch_op:
        batch_op.drop_column("dual_use")

    # ### end Alembic commands ###
    conn = op.get_bind()
    manufacturer_models_to_check = []
    res = conn.execute("select manufacturer_name, model from device")
    for row in res:
        manufacturer_models_to_check.append((row["manufacturer_name"], row["model"]))
    res = conn.execute("select manufacturer_name, model from platform")
    for row in res:
        manufacturer_models_to_check.append((row["manufacturer_name"], row["model"]))
    for manufacturer_name, model in manufacturer_models_to_check:
        if manufacturer_name and model:
            res = conn.execute(
                sa.text(
                    """
                    select id from manufacturer_model
                    where manufacturer_name = :manufacturer_name
                    and model = :model
                    limit 1
                    """
                ),
                manufacturer_name=manufacturer_name,
                model=model,
            )
            exists_already = False
            for _row in res:
                exists_already = True

            if not exists_already:
                conn.execute(
                    sa.text(
                        """
                        insert into manufacturer_model (manufacturer_name, model)
                        values (:manufacturer_name, :model)
                        """
                    ),
                    manufacturer_name=manufacturer_name,
                    model=model,
                )


def downgrade():
    """Undo the database structure changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("device", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("dual_use", sa.BOOLEAN(), autoincrement=False, nullable=True)
        )

    op.drop_table("export_control_attachment")
    op.drop_table("export_control")
    op.drop_table("manufacturer_model")
    # ### end Alembic commands ###
