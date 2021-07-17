"""empty message

Revision ID: 35889579cf3f
Revises: 1bb0a5841428
Create Date: 2020-03-12 21:02:52.883410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35889579cf3f'
down_revision = '1bb0a5841428'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Column('password', sa.String(length=256))
    with op.batch_alter_table('pantry', schema=None) as batch_op:
        batch_op.drop_column('units_used')
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pantry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('units_used', sa.VARCHAR(length=64), nullable=False))

    # ### end Alembic commands ###