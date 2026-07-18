"""Add live_stream_path to training_sessions for live classroom audio/video

Revision ID: l1i2v3e4m5e6
Revises: s1t2u3d4e5n6
Create Date: 2026-07-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'l1i2v3e4m5e6'
down_revision = 's1t2u3d4e5n6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'training_sessions',
        sa.Column('live_stream_path', sa.String(length=64), nullable=True),
    )
    op.create_index(
        op.f('ix_training_sessions_live_stream_path'),
        'training_sessions',
        ['live_stream_path'],
        unique=True,
    )


def downgrade():
    op.drop_index(op.f('ix_training_sessions_live_stream_path'), table_name='training_sessions')
    op.drop_column('training_sessions', 'live_stream_path')
