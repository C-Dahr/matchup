"""empty message

Revision ID: 245f535c8d0a
Revises: e3f11d273495
Create Date: 2020-03-02 12:19:57.504311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '245f535c8d0a'
down_revision = 'e3f11d273495'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bracket', sa.Column('event_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bracket', 'event', ['event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bracket', type_='foreignkey')
    op.drop_column('bracket', 'event_id')
    # ### end Alembic commands ###