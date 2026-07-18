"""Add keep_recording to training_sessions

Revision ID: k1e2e3p4r5e6
Revises: r1e2c3o4r5d6
Create Date: 2026-07-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'k1e2e3p4r5e6'
down_revision = 'r1e2c3o4r5d6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'training_sessions',
        sa.Column('keep_recording', sa.Boolean(), server_default=sa.text('false'), nullable=False)
    )


def downgrade():
    op.drop_column('training_sessions', 'keep_recording')
