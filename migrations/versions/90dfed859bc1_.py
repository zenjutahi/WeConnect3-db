"""empty message

Revision ID: 90dfed859bc1
Revises: ad25fd2cc00a
Create Date: 2018-04-09 19:52:30.121279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90dfed859bc1'
down_revision = 'ad25fd2cc00a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_username', table_name='users')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    # ### end Alembic commands ###
