"""TransactionHistory amout -> amount

Revision ID: 123ee4b767da
Revises: c3ffb8050d31
Create Date: 2020-12-01 18:24:19.010773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '123ee4b767da'
down_revision = 'c3ffb8050d31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transfer_history', sa.Column('amount', sa.Integer(), nullable=False))
    op.drop_column('transfer_history', 'amout')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transfer_history', sa.Column('amout', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('transfer_history', 'amount')
    # ### end Alembic commands ###