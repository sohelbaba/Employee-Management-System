"""empty message

Revision ID: 1304fd78880f
Revises: cf0f5e708685
Create Date: 2021-03-03 21:20:11.803897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1304fd78880f'
down_revision = 'cf0f5e708685'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('salary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('month', sa.String(length=10), nullable=False),
    sa.Column('generateddate', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Float(precision=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('salary')
    # ### end Alembic commands ###
