"""Add media_broadcasting to training_sessions

Revision ID: b1r2o3a4d5c6
Revises: q1u2e3s4t5i6
Create Date: 2026-07-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1r2o3a4d5c6'
down_revision = 'q1u2e3s4t5i6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'training_sessions',
        sa.Column('media_broadcasting', sa.Boolean(), server_default=sa.text('false'), nullable=False)
    )


def downgrade():
    op.drop_column('training_sessions', 'media_broadcasting')
