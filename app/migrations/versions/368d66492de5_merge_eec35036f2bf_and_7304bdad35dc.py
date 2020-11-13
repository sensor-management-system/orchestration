"""merge eec35036f2bf and 7304bdad35dc

Revision ID: 368d66492de5
Revises: eec35036f2bf, 7304bdad35dc
Create Date: 2020-11-13 11:02:55.778234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '368d66492de5'
down_revision = ('eec35036f2bf', '7304bdad35dc')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
