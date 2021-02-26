"""empty message

Revision ID: cf0f5e708685
Revises: 476960e873cd
Create Date: 2021-02-26 16:00:06.344290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf0f5e708685'
down_revision = '476960e873cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authentication', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=35), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authentication', schema=None) as batch_op:
        batch_op.drop_column('email')

    # ### end Alembic commands ###