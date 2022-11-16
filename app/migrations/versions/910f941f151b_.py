"""empty message

Revision ID: 910f941f151b
Revises: 35881b2a27d2
Create Date: 2022-10-27 08:23:38.036478

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '910f941f151b'
down_revision = 'd5148bc31abd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    conn.execute(text("create extension if not exists postgis"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    conn.execute(text("drop extension postgis"))
    # ### end Alembic commands ###
