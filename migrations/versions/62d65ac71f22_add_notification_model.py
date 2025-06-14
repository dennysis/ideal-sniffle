"""Add notification model

Revision ID: 62d65ac71f22
Revises: 3e84a3770bdb
Create Date: 2025-05-26 21:33:48.641579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62d65ac71f22'
down_revision = '3e84a3770bdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('is_read', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('read_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('related_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('related_type', sa.String(length=50), nullable=True))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.alter_column('message',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.drop_constraint('notifications_related_donation_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('notifications_related_orphanage_id_fkey', type_='foreignkey')
        batch_op.drop_column('related_donation_id')
        batch_op.drop_column('notification_type')
        batch_op.drop_column('read')
        batch_op.drop_column('related_orphanage_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('related_orphanage_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('read', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('notification_type', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('related_donation_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('notifications_related_orphanage_id_fkey', 'orphanages', ['related_orphanage_id'], ['id'])
        batch_op.create_foreign_key('notifications_related_donation_id_fkey', 'donations', ['related_donation_id'], ['id'])
        batch_op.alter_column('message',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('title',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('related_type')
        batch_op.drop_column('related_id')
        batch_op.drop_column('read_at')
        batch_op.drop_column('is_read')
        batch_op.drop_column('type')

    # ### end Alembic commands ###
