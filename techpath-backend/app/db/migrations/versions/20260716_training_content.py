"""Create training content tables: programmes, modules, lecture assets

Revision ID: t1a2b3c4d5e6
Revises: m1n2o3p4q5r6
Create Date: 2026-07-16

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 't1a2b3c4d5e6'
down_revision = 'm1n2o3p4q5r6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'training_programs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('summary', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        # Nullable: offline-only training has no public course page.
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('delivery_mode', sa.String(length=20), nullable=False, server_default='offline'),
        sa.Column('level', sa.String(length=20), nullable=True),
        sa.Column('duration', sa.String(length=100), nullable=True),
        sa.Column('cover_image', sa.String(length=500), nullable=True),
        sa.Column('tags_json', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_training_programs_slug', 'training_programs', ['slug'], unique=True)
    op.create_index('ix_training_programs_course_id', 'training_programs', ['course_id'])
    op.create_index('ix_training_programs_status', 'training_programs', ['status'])

    op.create_table(
        'training_modules',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_minutes', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['program_id'], ['training_programs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('program_id', 'slug', name='uq_training_modules_program_slug'),
    )
    op.create_index(
        'ix_training_modules_program_order', 'training_modules', ['program_id', 'display_order']
    )

    op.create_table(
        'lecture_assets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('public_id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('asset_type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        # Payload columns — which one is used is decided by the type's storage kind.
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('media_file_id', sa.Integer(), nullable=True),
        sa.Column('external_url', sa.String(length=1000), nullable=True),
        sa.Column('config_json', sa.Text(), nullable=True),
        # Reserved for html_bundle, which is modelled but not yet enabled.
        sa.Column('bundle_path', sa.String(length=500), nullable=True),
        sa.Column('bundle_entry', sa.String(length=255), nullable=True),
        sa.Column('tags_json', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['media_file_id'], ['media_files.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_lecture_assets_public_id', 'lecture_assets', ['public_id'], unique=True)
    op.create_index('ix_lecture_assets_asset_type', 'lecture_assets', ['asset_type'])
    op.create_index('ix_lecture_assets_type_status', 'lecture_assets', ['asset_type', 'status'])

    op.create_table(
        'training_module_assets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_required', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['module_id'], ['training_modules.id'], ondelete='CASCADE'),
        # RESTRICT: an asset still in use must not vanish from under a module.
        sa.ForeignKeyConstraint(['asset_id'], ['lecture_assets.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('module_id', 'asset_id', name='uq_module_asset'),
    )
    op.create_index(
        'ix_module_assets_module_order', 'training_module_assets', ['module_id', 'display_order']
    )


def downgrade():
    op.drop_table('training_module_assets')
    op.drop_table('lecture_assets')
    op.drop_table('training_modules')
    op.drop_table('training_programs')
