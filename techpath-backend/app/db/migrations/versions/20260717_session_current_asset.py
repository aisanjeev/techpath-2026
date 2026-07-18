"""Add current_asset_id to training_sessions for live classroom slide sync

Revision ID: c2u3r4r5e6n7
Revises: c1r2o3o4m5s6
Create Date: 2026-07-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2u3r4r5e6n7'
down_revision = 'c1r2o3o4m5s6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'training_sessions',
        sa.Column('current_asset_id', sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        'fk_training_sessions_current_asset',
        'training_sessions',
        'lecture_assets',
        ['current_asset_id'],
        ['id'],
        ondelete='SET NULL',
    )


def downgrade():
    op.drop_constraint('fk_training_sessions_current_asset', 'training_sessions', type_='foreignkey')
    op.drop_column('training_sessions', 'current_asset_id')
