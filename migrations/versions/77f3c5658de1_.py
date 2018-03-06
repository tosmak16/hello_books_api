"""empty message

Revision ID: 77f3c5658de1
Revises: 29ea461ab6df
Create Date: 2018-03-06 11:25:40.265138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77f3c5658de1'
down_revision = '29ea461ab6df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('title', sa.String(length=80), nullable=False))
    op.drop_column('books', 'titles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('titles', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_column('books', 'title')
    # ### end Alembic commands ###
