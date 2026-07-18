"""Add hand-raise, kick, quiz-poll, and timer columns for classroom interactivity

Revision ID: c3i4n5t6r7a8
Revises: c2u3r4r5e6n7
Create Date: 2026-07-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3i4n5t6r7a8'
down_revision = 'c2u3r4r5e6n7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'session_participants',
        sa.Column('hand_raised', sa.Boolean(), nullable=False, server_default='0'),
    )
    op.add_column(
        'session_participants',
        sa.Column('hand_raised_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        'session_participants',
        sa.Column('is_removed', sa.Boolean(), nullable=False, server_default='0'),
    )
    op.add_column(
        'session_polls',
        sa.Column('correct_option_index', sa.Integer(), nullable=True),
    )
    op.add_column(
        'training_sessions',
        sa.Column('timer_started_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        'training_sessions',
        sa.Column('timer_duration_seconds', sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column('training_sessions', 'timer_duration_seconds')
    op.drop_column('training_sessions', 'timer_started_at')
    op.drop_column('session_polls', 'correct_option_index')
    op.drop_column('session_participants', 'is_removed')
    op.drop_column('session_participants', 'hand_raised_at')
    op.drop_column('session_participants', 'hand_raised')
