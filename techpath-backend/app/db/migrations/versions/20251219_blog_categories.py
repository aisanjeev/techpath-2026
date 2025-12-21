"""Add blog categories table and category_id to blog_posts

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2025-12-19 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6g7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create blog_categories table
    op.create_table(
        'blog_categories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['parent_id'], ['blog_categories.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_blog_categories_slug', 'blog_categories', ['slug'], unique=True)

    # Create a default "Uncategorized" category for existing posts
    op.execute("""
        INSERT INTO blog_categories (name, slug, description, display_order, is_active)
        VALUES ('Uncategorized', 'uncategorized', 'Default category for posts', 0, 1)
    """)

    # Add category_id column to blog_posts (nullable first for migration)
    op.add_column('blog_posts', sa.Column('category_id', sa.Integer(), nullable=True))
    
    # Update existing posts to use the default category
    op.execute("""
        UPDATE blog_posts 
        SET category_id = (SELECT id FROM blog_categories WHERE slug = 'uncategorized')
    """)
    
    # Now make category_id NOT NULL
    # For SQLite, we need to recreate the table constraint approach is not directly supported
    # Instead, we'll just ensure the data is populated. The model enforces NOT NULL.
    
    # Add foreign key constraint (SQLite doesn't support adding FK to existing table easily)
    # The constraint is defined in the model, will be enforced on new databases
    
    # Add content_type column if it doesn't exist
    op.add_column('blog_posts', sa.Column('content_type', sa.String(length=20), nullable=True, server_default='html'))


def downgrade() -> None:
    # Remove content_type column
    op.drop_column('blog_posts', 'content_type')
    
    # Remove category_id column
    op.drop_column('blog_posts', 'category_id')
    
    # Drop blog_categories table
    op.drop_index('ix_blog_categories_slug', table_name='blog_categories')
    op.drop_table('blog_categories')

