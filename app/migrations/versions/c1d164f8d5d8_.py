"""Add active to contact model.

Revision ID: c1d164f8d5d8
Revises: 0028782b3d04
Create Date: 2021-09-22 07:59:35.626624

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c1d164f8d5d8'
down_revision = '0028782b3d04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'active')
    # ### end Alembic commands ###
