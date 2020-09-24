"""empty message

Revision ID: 485380cc62eb
Revises: df868a68fc52
Create Date: 2020-09-17 13:25:23.879528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '485380cc62eb'
down_revision = 'df868a68fc52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('configuration_device', 'configuration_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('configuration_device', 'device_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('configuration_device', 'platform_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('configuration_platform', 'configuration_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('configuration_platform', 'platform_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('configuration_platform', 'platform_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('configuration_platform', 'configuration_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('configuration_device', 'platform_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('configuration_device', 'device_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('configuration_device', 'configuration_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
