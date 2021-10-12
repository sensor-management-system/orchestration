"""Add {groups_ids, is_private, is_superuser} attributes

Revision ID: 12e34f225a6c
Revises: 0139893c4e15
Create Date: 2021-09-29 07:29:59.046318

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '12e34f225a6c'
down_revision = '0139893c4e15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configuration', sa.Column('groups_ids', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('configuration', sa.Column('is_internal', sa.Boolean(), nullable=False))
    op.add_column('configuration', sa.Column('is_public', sa.Boolean(), nullable=False))
    op.add_column('configuration', sa.Column('is_private', sa.Boolean(), nullable=False))

    op.add_column('device', sa.Column('groups_ids', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('device', sa.Column('is_private', sa.Boolean(), nullable=False))
    op.add_column('device', sa.Column('is_internal', sa.Boolean(), nullable=False))
    op.add_column('device', sa.Column('is_public', sa.Boolean(), nullable=False))

    op.add_column('platform', sa.Column('groups_ids', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('platform', sa.Column('is_private', sa.Boolean(), nullable=False))
    op.add_column('platform', sa.Column('is_internal', sa.Boolean(), nullable=False))
    op.add_column('platform', sa.Column('is_public', sa.Boolean(), nullable=False))

    op.add_column('user', sa.Column('is_superuser', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_superuser')

    op.drop_column('platform', 'is_public')
    op.drop_column('platform', 'is_internal')
    op.drop_column('platform', 'is_private')
    op.drop_column('platform', 'groups_ids')

    op.drop_column('device', 'is_public')
    op.drop_column('device', 'is_internal')
    op.drop_column('device', 'is_private')
    op.drop_column('device', 'groups_ids')

    op.drop_column('configuration', 'is_public')
    op.drop_column('configuration', 'is_internal')
    op.drop_column('configuration', 'groups_ids')
    # ### end Alembic commands ###
