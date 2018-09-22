"""Allow arbitrary length task titles

Revision ID: 56bf3ca5fb5e
Revises: 1ba4ca96664a
Create Date: 2018-09-22 15:47:39.631912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56bf3ca5fb5e'
down_revision = '1ba4ca96664a'
branch_labels = None
depends_on = None


def upgrade():
  op.alter_column(
      'task', 'title', type_=sa.UnicodeText(), existing_nullable=False)


def downgrade():
  op.alter_column(
      'task', 'title', type_=sa.Unicode(length=200), existing_nullable=False)
