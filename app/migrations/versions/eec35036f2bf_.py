"""empty message

Revision ID: eec35036f2bf
Revises: ee56321dc122
Create Date: 2020-10-16 15:32:30.462300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eec35036f2bf'
down_revision = 'ee56321dc122'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configuration_device', sa.Column('parent_platform_id', sa.Integer(), nullable=False))
    op.drop_constraint('configuration_device_platform_id_fkey', 'configuration_device', type_='foreignkey')
    op.create_foreign_key(None, 'configuration_device', 'platform', ['parent_platform_id'], ['id'])
    op.drop_column('configuration_device', 'platform_id')
    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configuration_device', sa.Column('platform_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'configuration_device', type_='foreignkey')
    op.create_foreign_key('configuration_device_platform_id_fkey', 'configuration_device', 'platform', ['platform_id'], ['id'])
    op.drop_column('configuration_device', 'parent_platform_id')
    # ### end Alembic commands ###
    pass
