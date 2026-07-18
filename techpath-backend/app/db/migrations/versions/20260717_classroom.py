"""Create the live classroom: participants, polls, live code state, event outbox

Revision ID: c1r2o3o4m5s6
Revises: t7f8g9h0i1j2
Create Date: 2026-07-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1r2o3o4m5s6'
down_revision = 't7f8g9h0i1j2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'session_participants',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        # Matched by email at identify-time; null for a guest join.
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('participant_key', sa.String(length=36), nullable=False),
        sa.Column('display_name', sa.String(length=200), nullable=False),
        sa.Column('is_guest', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('first_joined_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_seen_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('left_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_online', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('is_confused', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('confused_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['training_students.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id', 'participant_key', name='uq_session_participant_key'),
    )
    op.create_index('ix_session_participants_session', 'session_participants', ['session_id'])

    op.create_table(
        'session_polls',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('question', sa.String(length=500), nullable=False),
        sa.Column('options_json', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='open'),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_session_polls_session', 'session_polls', ['session_id'])
    op.create_index('ix_session_polls_status', 'session_polls', ['status'])

    op.create_table(
        'session_poll_votes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('poll_id', sa.Integer(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=False),
        sa.Column('option_index', sa.Integer(), nullable=False),
        sa.Column('voted_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['poll_id'], ['session_polls.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['participant_id'], ['session_participants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('poll_id', 'participant_id', name='uq_poll_vote_participant'),
    )

    op.create_table(
        'session_code_states',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('language', sa.String(length=50), nullable=False, server_default='python'),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id'),
    )

    # Append-only outbox. `id` is the polling cursor every worker's broadcaster tracks
    # per session — the reason a naive in-memory pub/sub isn't safe under --workers 2.
    op.create_table(
        'classroom_events',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('payload_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_classroom_events_session_id', 'classroom_events', ['session_id', 'id'])


def downgrade():
    op.drop_table('classroom_events')
    op.drop_table('session_code_states')
    op.drop_table('session_poll_votes')
    op.drop_table('session_polls')
    op.drop_table('session_participants')
