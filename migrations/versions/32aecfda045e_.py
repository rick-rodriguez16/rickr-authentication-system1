"""empty message

Revision ID: 32aecfda045e
Revises: dda5cf14be5c
Create Date: 2024-06-14 06:10:57.290046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32aecfda045e'
down_revision = 'dda5cf14be5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('invoice_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_date', sa.String(length=120), nullable=False),
    sa.Column('invoice_number', sa.String(length=80), nullable=False),
    sa.Column('invoice_amount', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('invoice_table')
    op.drop_table('user_table')
    # ### end Alembic commands ###
