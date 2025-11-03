"""Add dataset_type column to data_set table

Revision ID: 17f1be643b26
Revises: 001
Create Date: 2025-11-03 01:03:15.647208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17f1be643b26'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('data_set', sa.Column("dataset_type", sa.String(length=120), nullable=False, server_default="uvl"))


def downgrade():
    op.drop_column('data_set', 'dataset_type')
