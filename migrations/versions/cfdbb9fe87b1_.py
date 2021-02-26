"""empty message

Revision ID: cfdbb9fe87b1
Revises: b507332f87b9
Create Date: 2021-02-24 14:16:53.420190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfdbb9fe87b1'
down_revision = 'b507332f87b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('grade', schema=None) as batch_op:
        batch_op.alter_column('end_date',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('grade', schema=None) as batch_op:
        batch_op.alter_column('end_date',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)

    # ### end Alembic commands ###
