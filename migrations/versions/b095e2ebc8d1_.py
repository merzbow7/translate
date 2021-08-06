"""empty message

Revision ID: b095e2ebc8d1
Revises: 109fafe841a3
Create Date: 2021-07-02 18:29:39.477247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b095e2ebc8d1'
down_revision = '109fafe841a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('english_words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word'),
    sa.UniqueConstraint('word')
    )
    op.create_table('russian_words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word'),
    sa.UniqueConstraint('word')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('russian_words')
    op.drop_table('english_words')
    # ### end Alembic commands ###