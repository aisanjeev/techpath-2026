"""Create pages table for standalone CMS pages."""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "q2r3s4t5u6v7"
down_revision: Union[str, None] = "p1q2r3s4t5u6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "content_type",
            sa.String(20),
            nullable=False,
            server_default="html",
        ),
        sa.Column("excerpt", sa.String(500), nullable=True),
        sa.Column("featured_image", sa.String(500), nullable=True),
        sa.Column(
            "status",
            sa.String(50),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("meta_title", sa.String(255), nullable=True),
        sa.Column("meta_description", sa.String(500), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_pages_slug", "pages", ["slug"], unique=True)
    op.create_index("ix_pages_status", "pages", ["status"])
    op.create_index(
        "ix_pages_status_published_at", "pages", ["status", "published_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_pages_status_published_at", table_name="pages")
    op.drop_index("ix_pages_status", table_name="pages")
    op.drop_index("ix_pages_slug", table_name="pages")
    op.drop_table("pages")
