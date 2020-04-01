"""empty message

Revision ID: 67be86d51a00
Revises: 0b2034870e19
Create Date: 2020-03-02 16:38:53.161974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67be86d51a00'
down_revision = '0b2034870e19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bracket', sa.Column('event_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'bracket', 'event', ['event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bracket', type_='foreignkey')
    op.drop_column('bracket', 'event_id')
    # ### end Alembic commands ###
