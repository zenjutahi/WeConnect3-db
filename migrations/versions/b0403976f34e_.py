"""empty message

Revision ID: b0403976f34e
Revises: 90dfed859bc1
Create Date: 2018-04-10 06:19:07.312447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0403976f34e'
down_revision = '90dfed859bc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokenBlacklists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_identity', sa.String(length=50), nullable=False),
    sa.Column('token', sa.String(length=400), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('blacklisted_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokenBlacklists')
    # ### end Alembic commands ###
