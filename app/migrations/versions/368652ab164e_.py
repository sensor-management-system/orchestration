"""Add organization to contact

Revision ID: 368652ab164e
Revises: 08268f612083
Create Date: 2023-03-13 07:51:59.607926

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "368652ab164e"
down_revision = "08268f612083"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("contact", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("organization", sa.String(length=1024), nullable=True)
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("contact", schema=None) as batch_op:
        batch_op.drop_column("organization")
    # ### end Alembic commands ###
