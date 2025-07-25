"""empty message

Revision ID: e84b9bd3e641
Revises: cd0794d46d69
Create Date: 2025-06-20 14:24:03.965227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e84b9bd3e641'
down_revision = 'cd0794d46d69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Genres')
    # ### end Alembic commands ###
