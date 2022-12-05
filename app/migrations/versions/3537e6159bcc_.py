"""empty message

Revision ID: 3537e6159bcc
Revises: bc41fd42f238
Create Date: 2022-12-05 09:59:50.103259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3537e6159bcc'
down_revision = 'bc41fd42f238'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('site', sa.Column('elevation', sa.Float(), nullable=True))
    op.add_column('site', sa.Column('elevation_datum_name', sa.String(length=256), nullable=True))
    op.add_column('site', sa.Column('elevation_datum_uri', sa.String(length=256), nullable=True))
    op.add_column('site', sa.Column('site_type_uri', sa.String(length=256), nullable=True))
    op.add_column('site', sa.Column('site_type_name', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('site', 'site_type_name')
    op.drop_column('site', 'site_type_uri')
    op.drop_column('site', 'elevation_datum_uri')
    op.drop_column('site', 'elevation_datum_name')
    op.drop_column('site', 'elevation')
    # ### end Alembic commands ###
