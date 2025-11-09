"""Add MovieDataset model with proper inheritance

Revision ID: 05e898d99ea2
Revises: 53250b584934
Create Date: 2025-11-04 00:12:51.087781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05e898d99ea2'
down_revision = '53250b584934'
branch_labels = None
depends_on = None


def upgrade():
    # Crear tabla movie_dataset con herencia de base_dataset
    op.create_table('movie_dataset',
        # Primary key que es también foreign key a base_dataset
        sa.Column('id', sa.Integer(), nullable=False),
        
        # Campos específicos de películas
        sa.Column('movie_title', sa.String(length=255), nullable=True),
        sa.Column('original_title', sa.String(length=255), nullable=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('country', sa.String(length=255), nullable=True),
        sa.Column('director', sa.String(length=500), nullable=True),
        sa.Column('production_company', sa.String(length=500), nullable=True),
        sa.Column('genre', sa.String(length=255), nullable=True),
        sa.Column('synopsis', sa.Text(), nullable=True),
        sa.Column('imdb_rating', sa.Float(), nullable=True),
        sa.Column('imdb_votes', sa.Integer(), nullable=True),
        sa.Column('poster_url', sa.String(length=500), nullable=True),
        sa.Column('poster_local_path', sa.String(length=500), nullable=True),
        sa.Column('screenplay', sa.JSON(), nullable=True),
        sa.Column('cast', sa.JSON(), nullable=True),
        sa.Column('awards', sa.JSON(), nullable=True),
        
        # Foreign key constraint a base_dataset
        sa.ForeignKeyConstraint(['id'], ['base_dataset.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('movie_dataset')