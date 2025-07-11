"""Add donation model and relationships

Revision ID: 3e84a3770bdb
Revises: be19b7f7e8dd
Create Date: 2025-05-26 21:08:56.567238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e84a3770bdb'
down_revision = 'be19b7f7e8dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donations', schema=None) as batch_op:
        batch_op.alter_column('currency',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=3),
               existing_nullable=True)
        batch_op.alter_column('transaction_id',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=50),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donations', schema=None) as batch_op:
        batch_op.alter_column('transaction_id',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('currency',
               existing_type=sa.String(length=3),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###
