"""empty message

Revision ID: ba080fd4c124
Revises: 3b8e64f2b934
Create Date: 2020-04-15 18:13:28.928805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba080fd4c124'
down_revision = '3b8e64f2b934'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'event', ['id'])
    op.create_unique_constraint(None, 'player', ['id'])
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'player', type_='unique')
    op.drop_constraint(None, 'event', type_='unique')
    # ### end Alembic commands ###