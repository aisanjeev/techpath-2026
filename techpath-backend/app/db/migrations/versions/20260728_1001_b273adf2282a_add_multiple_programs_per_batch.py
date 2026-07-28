"""Add multiple programs per batch

Revision ID: b273adf2282a
Revises: s1e2l3f4p5a6
Create Date: 2026-07-28 10:01:24.937194+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b273adf2282a'
down_revision: Union[str, None] = 's1e2l3f4p5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create table
    op.create_table('training_batch_programs',
    sa.Column('batch_id', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['batch_id'], ['training_batches.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['program_id'], ['training_programs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('batch_id', 'program_id')
    )

    # 2. Data migration
    op.execute(
        "INSERT INTO training_batch_programs (batch_id, program_id) "
        "SELECT id, program_id FROM training_batches WHERE program_id IS NOT NULL"
    )

    # 3. Drop constraint and column
    op.drop_constraint('training_batches_ibfk_1', 'training_batches', type_='foreignkey')
    op.drop_column('training_batches', 'program_id')


def downgrade() -> None:
    # 1. Recreate column
    op.add_column('training_batches', sa.Column('program_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('training_batches_ibfk_1', 'training_batches', 'training_programs', ['program_id'], ['id'], ondelete='SET NULL')

    # 2. Data migration (restore first mapped program)
    op.execute(
        "UPDATE training_batches tb "
        "JOIN (SELECT batch_id, MIN(program_id) as program_id FROM training_batch_programs GROUP BY batch_id) tbp "
        "ON tb.id = tbp.batch_id "
        "SET tb.program_id = tbp.program_id"
    )

    # 3. Drop table
    op.drop_table('training_batch_programs')
