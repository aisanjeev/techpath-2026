"""Add graded quiz attempts

Revision ID: z1q2u3i4z5a6
Revises: b1r2o3a4d5c6
Create Date: 2026-07-18

Deliberately dialect-neutral: Text for the JSON payload, no server_default on the
timestamps (TimestampMixin supplies them Python-side), no native JSON column. The same
DDL has to apply on SQLite in dev and MySQL in staging/production.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "z1q2u3i4z5a6"
down_revision = "b1r2o3a4d5c6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "session_quiz_attempts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("answers_json", sa.Text(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("total_questions", sa.Integer(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("attempted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["training_students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["session_id"], ["training_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["asset_id"], ["lecture_assets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "student_id", "asset_id", "attempt_number", name="uq_quiz_attempt_number"
        ),
    )
    op.create_index(
        "ix_quiz_attempts_session_asset",
        "session_quiz_attempts",
        ["session_id", "asset_id"],
        unique=False,
    )
    op.create_index(
        "ix_quiz_attempts_student_session",
        "session_quiz_attempts",
        ["student_id", "session_id"],
        unique=False,
    )


def downgrade():
    # drop_table takes the indexes and constraints with it. Dropping them explicitly
    # first fails on MySQL: ix_quiz_attempts_session_asset leads with session_id, so
    # InnoDB uses it to back that column's foreign key and refuses to drop it
    # ("needed in a foreign key constraint"). SQLite tolerates the explicit drops, so
    # this only reproduces on MySQL.
    op.drop_table("session_quiz_attempts")
