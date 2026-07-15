"""Add bento layout fields to services table

Revision ID: k1l2m3n4o5p6
Revises: j0k1l2m3n4o5
Create Date: 2026-04-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'k1l2m3n4o5p6'
down_revision: Union[str, None] = 'j0k1l2m3n4o5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add bento layout columns to services table."""
    op.add_column('services', sa.Column('layout_size', sa.String(20), nullable=False, server_default='small'))
    op.add_column('services', sa.Column('badge_label', sa.String(50), nullable=True))
    op.add_column('services', sa.Column('tags', sa.Text(), nullable=True))
    op.add_column('services', sa.Column('stat_label', sa.String(100), nullable=True))
    op.add_column('services', sa.Column('stat_value', sa.String(50), nullable=True))
    op.add_column('services', sa.Column('accent_color', sa.String(20), nullable=False, server_default='blue'))
    op.add_column('services', sa.Column('graphic_variant', sa.String(20), nullable=False, server_default='none'))


def downgrade() -> None:
    """Remove bento layout columns from services table."""
    op.drop_column('services', 'graphic_variant')
    op.drop_column('services', 'accent_color')
    op.drop_column('services', 'stat_value')
    op.drop_column('services', 'stat_label')
    op.drop_column('services', 'tags')
    op.drop_column('services', 'badge_label')
    op.drop_column('services', 'layout_size')
