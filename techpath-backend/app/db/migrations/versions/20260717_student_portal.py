"""Add firebase_uid to training_students and materials-publish columns to training_sessions

Revision ID: s1t2u3d4e5n6
Revises: c3i4n5t6r7a8
Create Date: 2026-07-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 's1t2u3d4e5n6'
down_revision = 'c3i4n5t6r7a8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'training_students',
        sa.Column('firebase_uid', sa.String(length=128), nullable=True),
    )
    op.create_index(
        op.f('ix_training_students_firebase_uid'),
        'training_students',
        ['firebase_uid'],
        unique=True,
    )
    op.add_column(
        'training_sessions',
        sa.Column('materials_published_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        'training_sessions',
        sa.Column('materials_published_by_user_id', sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        'fk_training_sessions_materials_published_by',
        'training_sessions',
        'users',
        ['materials_published_by_user_id'],
        ['id'],
        ondelete='SET NULL',
    )


def downgrade():
    op.drop_constraint(
        'fk_training_sessions_materials_published_by', 'training_sessions', type_='foreignkey'
    )
    op.drop_column('training_sessions', 'materials_published_by_user_id')
    op.drop_column('training_sessions', 'materials_published_at')
    op.drop_index(op.f('ix_training_students_firebase_uid'), table_name='training_students')
    op.drop_column('training_students', 'firebase_uid')
