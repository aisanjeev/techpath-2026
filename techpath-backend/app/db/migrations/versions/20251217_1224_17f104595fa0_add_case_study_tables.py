"""add case study tables

Revision ID: 17f104595fa0
Revises: 
Create Date: 2025-12-17 12:24:34.553975+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17f104595fa0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Initial migration - all tables already exist via SQLAlchemy create_all.
    This migration documents the schema for case_studies, case_study_tag, 
    and case_study_tags tables.
    
    Tables created:
    - case_studies: Main case study records
    - case_study_tag: Tags for categorizing case studies  
    - case_study_tags: Many-to-many association table
    """
    # Tables already created by SQLAlchemy Base.metadata.create_all()
    # This is the initial migration marking current schema state
    pass


def downgrade() -> None:
    """Drop case study tables if rolling back to before this migration."""
    op.drop_table('case_study_tags')
    op.drop_table('case_study_tag')
    op.drop_table('case_studies')
