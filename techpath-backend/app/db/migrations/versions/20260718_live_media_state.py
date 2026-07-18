"""Add media_mic_muted/media_camera_off/media_screen_sharing to training_sessions

Revision ID: m1e2d3i4a5s6
Revises: l1i2v3e4m5e6
Create Date: 2026-07-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'm1e2d3i4a5s6'
down_revision = 'l1i2v3e4m5e6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'training_sessions',
        sa.Column('media_mic_muted', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        'training_sessions',
        sa.Column('media_camera_off', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        'training_sessions',
        sa.Column(
            'media_screen_sharing', sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )


def downgrade():
    op.drop_column('training_sessions', 'media_screen_sharing')
    op.drop_column('training_sessions', 'media_camera_off')
    op.drop_column('training_sessions', 'media_mic_muted')
