"""Add media files and usages tables

Revision ID: a1b2c3d4e5f6
Revises: 17f104595fa0
Create Date: 2025-12-19 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '17f104595fa0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create media_files table
    op.create_table(
        'media_files',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('stored_path', sa.String(length=500), nullable=False),
        sa.Column('file_hash', sa.String(length=64), nullable=False),
        sa.Column('content_type', sa.String(length=100), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('alt_text', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('stored_path')
    )
    op.create_index('ix_media_files_file_hash', 'media_files', ['file_hash'], unique=False)

    # Create media_file_usages table
    op.create_table(
        'media_file_usages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('field_name', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['file_id'], ['media_files.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_media_file_usages_entity', 'media_file_usages', ['entity_type', 'entity_id'], unique=False)
    op.create_index('ix_media_file_usages_file_entity', 'media_file_usages', ['file_id', 'entity_type', 'entity_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_media_file_usages_file_entity', table_name='media_file_usages')
    op.drop_index('ix_media_file_usages_entity', table_name='media_file_usages')
    op.drop_table('media_file_usages')
    op.drop_index('ix_media_files_file_hash', table_name='media_files')
    op.drop_table('media_files')

