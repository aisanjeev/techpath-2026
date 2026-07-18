"""Add live questions

Revision ID: q1u2e3s4t5i6
Revises: k1e2e3p4r5e6
Create Date: 2026-07-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'q1u2e3s4t5i6'
down_revision = 'k1e2e3p4r5e6'
branch_labels = None
depends_on = None


def upgrade():
    # Add questions_are_public to training_sessions
    op.add_column(
        'training_sessions',
        sa.Column('questions_are_public', sa.Boolean(), server_default=sa.text('true'), nullable=False)
    )

    # Create training_session_questions table
    op.create_table(
        'training_session_questions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.String(length=500), nullable=False),
        sa.Column('is_answered', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('upvotes', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['training_students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_session_questions_session_id'), 'training_session_questions', ['session_id'], unique=False)
    op.create_index(op.f('ix_training_session_questions_student_id'), 'training_session_questions', ['student_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_training_session_questions_student_id'), table_name='training_session_questions')
    op.drop_index(op.f('ix_training_session_questions_session_id'), table_name='training_session_questions')
    op.drop_table('training_session_questions')
    op.drop_column('training_sessions', 'questions_are_public')
