"""Add faqs column to services table

Revision ID: j0k1l2m3n4o5
Revises: i9j0k1l2m3n4
Create Date: 2026-01-31 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'j0k1l2m3n4o5'
down_revision: Union[str, None] = 'i9j0k1l2m3n4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add faqs column to services table."""
    op.add_column('services', sa.Column('faqs', sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove faqs column from services table."""
    op.drop_column('services', 'faqs')
