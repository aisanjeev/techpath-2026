"""Create pilot_signups table

Revision ID: d5e6f7g8h9i0
Revises: c3d4e5f6g7h8
Create Date: 2025-01-29

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'd5e6f7g8h9i0'
down_revision = 'c3d4e5f6g7h8'  # Previous courses migration
branch_labels = None
depends_on = None


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def upgrade():
    # Drop existing table if it exists (from partial migration)
    if table_exists('pilot_signups'):
        op.drop_table('pilot_signups')

    # Create pilot_signups table
    op.create_table(
        'pilot_signups',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        
        # Contact Information
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=False),
        
        # Business Information
        sa.Column('business_name', sa.String(length=100), nullable=False),
        sa.Column('industry', sa.String(length=50), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        
        # Status and Admin Notes
        sa.Column('status', sa.String(length=50), server_default='new', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        
        # Metadata
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=func.now(), nullable=False),
        
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for efficient querying
    op.create_index(op.f('ix_pilot_signups_email'), 'pilot_signups', ['email'], unique=False)
    op.create_index(op.f('ix_pilot_signups_status'), 'pilot_signups', ['status'], unique=False)
    op.create_index(op.f('ix_pilot_signups_industry'), 'pilot_signups', ['industry'], unique=False)
    op.create_index(op.f('ix_pilot_signups_created_at'), 'pilot_signups', ['created_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_pilot_signups_created_at'), table_name='pilot_signups')
    op.drop_index(op.f('ix_pilot_signups_industry'), table_name='pilot_signups')
    op.drop_index(op.f('ix_pilot_signups_status'), table_name='pilot_signups')
    op.drop_index(op.f('ix_pilot_signups_email'), table_name='pilot_signups')
    op.drop_table('pilot_signups')
