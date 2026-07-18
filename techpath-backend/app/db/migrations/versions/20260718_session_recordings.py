"""Add session_recordings table for live classroom VOD/replay

Revision ID: r1e2c3o4r5d6
Revises: m1e2d3i4a5s6
Create Date: 2026-07-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'r1e2c3o4r5d6'
down_revision = 'm1e2d3i4a5s6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'session_recordings',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='processing'),
        sa.Column('recording_path', sa.String(length=255), nullable=True),
        sa.Column('watch_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ondelete='CASCADE'),
    )
    op.create_index(
        op.f('ix_session_recordings_session_id'), 'session_recordings', ['session_id']
    )
    op.create_index(
        op.f('ix_session_recordings_status'), 'session_recordings', ['status']
    )


def downgrade():
    op.drop_index(op.f('ix_session_recordings_status'), table_name='session_recordings')
    op.drop_index(op.f('ix_session_recordings_session_id'), table_name='session_recordings')
    op.drop_table('session_recordings')
