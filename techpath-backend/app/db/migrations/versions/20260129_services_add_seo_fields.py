"""Add SEO fields to services table

Revision ID: i9j0k1l2m3n4
Revises: h8i9j0k1l2m3
Create Date: 2026-01-29 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'i9j0k1l2m3n4'
down_revision: Union[str, None] = 'h8i9j0k1l2m3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add SEO columns to services table."""
    op.add_column('services', sa.Column('meta_title', sa.String(length=255), nullable=True))
    op.add_column('services', sa.Column('meta_description', sa.String(length=500), nullable=True))
    op.add_column('services', sa.Column('og_image', sa.String(length=500), nullable=True))
    op.add_column('services', sa.Column('canonical_url', sa.String(length=500), nullable=True))
    op.add_column('services', sa.Column('no_index', sa.Boolean(), nullable=False, server_default='0'))


def downgrade() -> None:
    """Remove SEO columns from services table."""
    op.drop_column('services', 'no_index')
    op.drop_column('services', 'canonical_url')
    op.drop_column('services', 'og_image')
    op.drop_column('services', 'meta_description')
    op.drop_column('services', 'meta_title')
