"""empty message

Revision ID: 3b8e64f2b934
Revises: 43afb57cd237
Create Date: 2020-03-30 11:38:17.421953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b8e64f2b934'
down_revision = '43afb57cd237'
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