"""empty message

Revision ID: 670761818108
Revises: ec85b60dc58b
Create Date: 2021-05-21 23:32:33.848491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '670761818108'
down_revision = 'ec85b60dc58b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('song',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('lirics', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('song')
    # ### end Alembic commands ###
