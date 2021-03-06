"""empty message

Revision ID: 5dde5207e310
Revises: f92eba433058
Create Date: 2021-05-30 12:32:25.162764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dde5207e310'
down_revision = 'f92eba433058'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('translate', sa.Column('transcription', sa.String(length=25), nullable=True))
    op.drop_constraint('translate_ru_key', 'translate', type_='unique')
    op.drop_constraint('translate_translation_key', 'translate', type_='unique')
    op.create_unique_constraint(None, 'translate', ['transcription'])
    op.drop_column('translate', 'translation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('translate', sa.Column('translation', sa.VARCHAR(length=25), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'translate', type_='unique')
    op.create_unique_constraint('translate_translation_key', 'translate', ['translation'])
    op.create_unique_constraint('translate_ru_key', 'translate', ['ru'])
    op.drop_column('translate', 'transcription')
    # ### end Alembic commands ###
