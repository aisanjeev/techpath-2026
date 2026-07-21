"""Add self-paced training support

Revision ID: s1e2l3f4p5a6
Revises: z1q2u3i4z5a6
Create Date: 2026-07-21

Adds:
- is_self_paced flag on training_batches
- student_module_progress table for tracking self-paced study
- module_id column on session_quiz_attempts (nullable, for self-paced quiz context)
- Makes session_id nullable on session_quiz_attempts (self-paced has no session)
"""

from alembic import op
import sqlalchemy as sa


revision = "s1e2l3f4p5a6"
down_revision = "z1q2u3i4z5a6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "training_batches",
        sa.Column(
            "is_self_paced",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )

    op.create_table(
        "student_module_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("module_id", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_accessed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_asset_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["student_id"], ["training_students.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["module_id"], ["training_modules.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_id", "module_id", name="uq_student_module_progress"),
    )
    op.create_index(
        "ix_student_module_progress_student",
        "student_module_progress",
        ["student_id"],
        unique=False,
    )

    # Self-paced quiz attempts have no session. The existing unique constraint
    # (student_id, asset_id, attempt_number) already excludes session_id, so
    # making it nullable is safe.
    with op.batch_alter_table("session_quiz_attempts") as batch_op:
        batch_op.alter_column("session_id", existing_type=sa.Integer(), nullable=True)
        batch_op.add_column(
            sa.Column("module_id", sa.Integer(), nullable=True),
        )
        batch_op.create_foreign_key(
            "fk_quiz_attempts_module_id",
            "training_modules",
            ["module_id"],
            ["id"],
            ondelete="CASCADE",
        )
        batch_op.create_index(
            "ix_quiz_attempts_student_module",
            ["student_id", "module_id"],
        )


def downgrade():
    with op.batch_alter_table("session_quiz_attempts") as batch_op:
        batch_op.drop_index("ix_quiz_attempts_student_module")
        batch_op.drop_constraint("fk_quiz_attempts_module_id", type_="foreignkey")
        batch_op.drop_column("module_id")
        batch_op.alter_column("session_id", existing_type=sa.Integer(), nullable=False)

    op.drop_index("ix_student_module_progress_student", table_name="student_module_progress")
    op.drop_table("student_module_progress")

    op.drop_column("training_batches", "is_self_paced")
