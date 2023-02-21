"""update tables

Revision ID: 47bf26d267ef
Revises: 1e3c68d3bf22
Create Date: 2023-02-21 00:19:34.120931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47bf26d267ef'
down_revision = '1e3c68d3bf22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'customer', ['full_name'])
    op.create_unique_constraint(None, 'product', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='unique')
    op.drop_constraint(None, 'customer', type_='unique')
    # ### end Alembic commands ###
