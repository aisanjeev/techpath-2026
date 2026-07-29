"""Add session_asset_releases table for per-asset material publishing

Revision ID: c4e8f1a2b3d9
Revises: b273adf2282a
Create Date: 2026-07-29 10:00:00.000000+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'c4e8f1a2b3d9'
down_revision: Union[str, None] = 'b273adf2282a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'session_asset_releases',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('released_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('released_by_user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['asset_id'], ['lecture_assets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['released_by_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id', 'asset_id', name='uq_session_asset_release'),
    )
    op.create_index('ix_session_asset_releases_session', 'session_asset_releases', ['session_id'])


def downgrade() -> None:
    op.drop_index('ix_session_asset_releases_session', table_name='session_asset_releases')
    op.drop_table('session_asset_releases')
