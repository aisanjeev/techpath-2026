"""Add firebase_uid to users and make password_hash nullable."""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = 'p1q2r3s4t5u6'
down_revision: Union[str, None] = 'j0k1l2m3n4o5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('firebase_uid', sa.String(128), nullable=True))
        batch_op.alter_column('password_hash', existing_type=sa.String(255), nullable=True)
        batch_op.create_unique_constraint('uq_users_firebase_uid', ['firebase_uid'])
        batch_op.create_index('ix_users_firebase_uid', ['firebase_uid'])


def downgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_index('ix_users_firebase_uid')
        batch_op.drop_constraint('uq_users_firebase_uid', type_='unique')
        batch_op.drop_column('firebase_uid')
        batch_op.alter_column('password_hash', existing_type=sa.String(255), nullable=False)
