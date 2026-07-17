"""Baseline: create the original core tables

Historically these tables were only ever created by ``Base.metadata.create_all()`` at
application startup, so no migration ever created them. That let the migration history
drift (and silently branch) while ``create_all`` quietly conjured whatever was missing.
Now that ``init_db()`` no longer calls ``create_all``, the chain has to be able to build
a database from empty, which means these tables need a real migration.

This sits at the root of the chain, before 17f104595fa0. It is a point-in-time snapshot:
columns added by later migrations are deliberately absent here, and are added further up
the chain as they always were. Specifically NOT included:

  users        — firebase_uid, and password_hash is still NOT NULL  (20260419)
  services     — pricing_plans (20260129), SEO fields (20260129), faqs (20260131),
                 bento layout fields (20260430)
  blog_posts   — category_id, content_type (20251219_blog_categories)

Every step is guarded by an existence check so this is a no-op on databases that
``create_all`` already populated. Existing deployments are stamped at descendants of
this revision, so Alembic treats it as applied and never runs it there anyway; the
guards are belt-and-braces for a DB that was never stamped.

Revision ID: a0b0c0d0e0f0
Revises:
Create Date: 2025-12-16

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'a0b0c0d0e0f0'
down_revision = None
branch_labels = None
depends_on = None


def _table_exists(table_name: str) -> bool:
    return table_name in inspect(op.get_bind()).get_table_names()


def upgrade():
    if not _table_exists('users'):
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('name', sa.String(length=255), nullable=False),
            # Made nullable later by 20260419 when Firebase auth landed.
            sa.Column('password_hash', sa.String(length=255), nullable=False),
            sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('avatar_url', sa.String(length=500), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_users_email', 'users', ['email'], unique=True)

    if not _table_exists('services'):
        op.create_table(
            'services',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('slug', sa.String(length=255), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('short_description', sa.String(length=500), nullable=True),
            sa.Column('icon', sa.String(length=255), nullable=True),
            sa.Column('image_url', sa.String(length=500), nullable=True),
            sa.Column('features', sa.Text(), nullable=True),
            sa.Column('price', sa.String(length=100), nullable=True),
            sa.Column('cta_text', sa.String(length=100), nullable=False, server_default='Learn More'),
            sa.Column('cta_url', sa.String(length=500), nullable=True),
            sa.Column('featured', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_services_slug', 'services', ['slug'], unique=True)

    if not _table_exists('blog_tags'):
        op.create_table(
            'blog_tags',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('slug', sa.String(length=100), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name'),
        )
        op.create_index('ix_blog_tags_slug', 'blog_tags', ['slug'], unique=True)

    if not _table_exists('blog_posts'):
        op.create_table(
            'blog_posts',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('slug', sa.String(length=255), nullable=False),
            sa.Column('excerpt', sa.String(length=500), nullable=True),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('featured_image', sa.String(length=500), nullable=True),
            sa.Column('author_id', sa.Integer(), nullable=True),
            sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
            sa.Column('featured', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('reading_time', sa.Integer(), nullable=True),
            sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('meta_title', sa.String(length=255), nullable=True),
            sa.Column('meta_description', sa.String(length=500), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='SET NULL'),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_blog_posts_slug', 'blog_posts', ['slug'], unique=True)

    if not _table_exists('blog_post_tags'):
        op.create_table(
            'blog_post_tags',
            sa.Column('post_id', sa.Integer(), nullable=False),
            sa.Column('tag_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['post_id'], ['blog_posts.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['tag_id'], ['blog_tags.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('post_id', 'tag_id'),
        )

    if not _table_exists('contact_inquiries'):
        op.create_table(
            'contact_inquiries',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('name', sa.String(length=255), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('phone', sa.String(length=50), nullable=True),
            sa.Column('company', sa.String(length=255), nullable=True),
            sa.Column('subject', sa.String(length=255), nullable=True),
            sa.Column('message', sa.Text(), nullable=False),
            sa.Column('service_interest', sa.String(length=255), nullable=True),
            sa.Column('status', sa.String(length=50), nullable=False, server_default='new'),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('ip_address', sa.String(length=50), nullable=True),
            sa.Column('user_agent', sa.String(length=500), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_contact_inquiries_email', 'contact_inquiries', ['email'])
        op.create_index('ix_contact_inquiries_status', 'contact_inquiries', ['status'])

    if not _table_exists('newsletter_subscribers'):
        op.create_table(
            'newsletter_subscribers',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('name', sa.String(length=255), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('source', sa.String(length=100), nullable=True),
            sa.Column('ip_address', sa.String(length=50), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index(
            'ix_newsletter_subscribers_email', 'newsletter_subscribers', ['email'], unique=True
        )

    # 17f104595fa0 documents these but its upgrade() is a no-op, so they belong here.
    if not _table_exists('case_studies'):
        op.create_table(
            'case_studies',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('slug', sa.String(length=255), nullable=False),
            sa.Column('client_name', sa.String(length=255), nullable=False),
            sa.Column('industry', sa.String(length=100), nullable=False),
            sa.Column('excerpt', sa.String(length=500), nullable=True),
            sa.Column('challenge', sa.Text(), nullable=False),
            sa.Column('solution', sa.Text(), nullable=False),
            sa.Column('results', sa.Text(), nullable=False),
            sa.Column('content', sa.Text(), nullable=True),
            sa.Column('featured_image', sa.String(length=500), nullable=True),
            sa.Column('stat_value', sa.String(length=50), nullable=True),
            sa.Column('stat_label', sa.String(length=100), nullable=True),
            sa.Column('additional_stats', sa.Text(), nullable=True),
            sa.Column('testimonial_quote', sa.Text(), nullable=True),
            sa.Column('testimonial_author', sa.String(length=255), nullable=True),
            sa.Column('testimonial_role', sa.String(length=255), nullable=True),
            sa.Column('author_id', sa.Integer(), nullable=True),
            sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
            sa.Column('featured', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('meta_title', sa.String(length=255), nullable=True),
            sa.Column('meta_description', sa.String(length=500), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='SET NULL'),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_case_studies_slug', 'case_studies', ['slug'], unique=True)

    if not _table_exists('case_study_tag'):
        op.create_table(
            'case_study_tag',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('slug', sa.String(length=100), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name'),
        )
        op.create_index('ix_case_study_tag_slug', 'case_study_tag', ['slug'], unique=True)

    if not _table_exists('case_study_tags'):
        op.create_table(
            'case_study_tags',
            sa.Column('case_study_id', sa.Integer(), nullable=False),
            sa.Column('tag_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['case_study_id'], ['case_studies.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['tag_id'], ['case_study_tag.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('case_study_id', 'tag_id'),
        )


def downgrade():
    # 17f104595fa0.downgrade() already drops the case_study_* tables, so guard everything.
    for table in (
        'case_study_tags',
        'case_study_tag',
        'case_studies',
        'newsletter_subscribers',
        'contact_inquiries',
        'blog_post_tags',
        'blog_posts',
        'blog_tags',
        'services',
        'users',
    ):
        if _table_exists(table):
            op.drop_table(table)
