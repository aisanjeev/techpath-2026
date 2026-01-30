"""Alter blog_posts.content to MEDIUMTEXT for MySQL (WordPress long posts)

Revision ID: f6g7h8i9j0k1
Revises: e5f6g7h8i9j0
Create Date: 2026-01-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = "f6g7h8i9j0k1"
down_revision: Union[str, None] = "e5f6g7h8i9j0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "mysql":
        op.alter_column(
            "blog_posts",
            "content",
            existing_type=sa.Text(),
            type_=mysql.MEDIUMTEXT(),
            existing_nullable=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "mysql":
        op.alter_column(
            "blog_posts",
            "content",
            existing_type=mysql.MEDIUMTEXT(),
            type_=sa.Text(),
            existing_nullable=False,
        )
