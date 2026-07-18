"""Create the roster mirror: batches, students, sessions, sync state

Revision ID: t7f8g9h0i1j2
Revises: t1a2b3c4d5e6
Create Date: 2026-07-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 't7f8g9h0i1j2'
down_revision = 't1a2b3c4d5e6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'training_batches',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        # The join key to the external system. Immutable upstream.
        sa.Column('external_id', sa.String(length=128), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=True),
        # Ours, admin-set. The sync preserves this column.
        sa.Column('program_id', sa.Integer(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('timezone', sa.String(length=64), nullable=True),
        sa.Column('schedule_json', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('mode', sa.String(length=20), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('trainer_email', sa.String(length=255), nullable=True),
        sa.Column('trainer_external_id', sa.String(length=128), nullable=True),
        sa.Column('trainer_name', sa.String(length=255), nullable=True),
        sa.Column('student_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('course_ref', sa.String(length=128), nullable=True),
        sa.Column('raw_json', sa.Text(), nullable=True),
        sa.Column('external_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('synced_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['program_id'], ['training_programs.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_training_batches_external_id', 'training_batches', ['external_id'], unique=True)
    op.create_index('ix_training_batches_code', 'training_batches', ['code'])
    op.create_index('ix_training_batches_status', 'training_batches', ['status'])
    op.create_index('ix_training_batches_trainer_email', 'training_batches', ['trainer_email'])

    op.create_table(
        'training_students',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('external_id', sa.String(length=128), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('roll_no', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('photo_url', sa.String(length=500), nullable=True),
        sa.Column('enrolled_on', sa.Date(), nullable=True),
        sa.Column('raw_json', sa.Text(), nullable=True),
        sa.Column('external_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('synced_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_training_students_external_id', 'training_students', ['external_id'], unique=True)
    op.create_index('ix_training_students_email', 'training_students', ['email'])
    op.create_index('ix_training_students_status', 'training_students', ['status'])

    op.create_table(
        'training_batch_students',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('membership_status', sa.String(length=50), nullable=True),
        sa.Column('enrolled_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['batch_id'], ['training_batches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['training_students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('batch_id', 'student_id', name='uq_batch_student'),
    )

    op.create_table(
        'training_sessions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=True),
        sa.Column('trainer_user_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('scheduled_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('scheduled_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='scheduled'),
        sa.Column('join_code', sa.String(length=6), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['batch_id'], ['training_batches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['module_id'], ['training_modules.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['trainer_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_training_sessions_join_code', 'training_sessions', ['join_code'], unique=True)
    op.create_index('ix_training_sessions_status', 'training_sessions', ['status'])
    op.create_index('ix_training_sessions_scheduled_start', 'training_sessions', ['scheduled_start'])
    op.create_index('ix_training_sessions_batch_start', 'training_sessions', ['batch_id', 'scheduled_start'])

    op.create_table(
        'training_sync_state',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('resource', sa.String(length=50), nullable=False),
        sa.Column('cursor_updated_since', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_run_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_success_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_status', sa.String(length=50), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('records_processed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_running', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('run_started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('resource'),
    )


def downgrade():
    op.drop_table('training_sync_state')
    op.drop_table('training_sessions')
    op.drop_table('training_batch_students')
    op.drop_table('training_students')
    op.drop_table('training_batches')
