"""Create course management tables

Revision ID: c3d4e5f6g7h8
Revises: b2c3d4e5f6g7
Create Date: 2025-12-19

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'c3d4e5f6g7h8'
down_revision = 'b2c3d4e5f6g7'  # Previous blog categories migration
branch_labels = None
depends_on = None


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def upgrade():
    # Drop existing tables if they exist (from partial migration)
    for table in ['course_enrollments', 'course_skills', 'courses', 'course_categories', 'skills']:
        if table_exists(table):
            op.drop_table(table)

    # Create skills table
    op.create_table(
        'skills',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_skills_slug'), 'skills', ['slug'], unique=True)

    # Create course_categories table (with self-referential FK inline)
    op.create_table(
        'course_categories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('icon', sa.String(length=100), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug'),
        sa.ForeignKeyConstraint(['parent_id'], ['course_categories.id'], ondelete='SET NULL')
    )
    op.create_index(op.f('ix_course_categories_slug'), 'course_categories', ['slug'], unique=True)

    # Create courses table (with FK inline)
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('short_description', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        
        # Pricing
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('original_price', sa.Float(), nullable=True),
        sa.Column('emi_available', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('emi_amount', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(length=3), server_default='INR', nullable=False),
        
        # Course Details
        sa.Column('duration', sa.String(length=50), nullable=False),
        sa.Column('duration_hours', sa.Integer(), nullable=True),
        sa.Column('batch_size', sa.Integer(), server_default='20', nullable=False),
        sa.Column('level', sa.String(length=20), server_default='beginner', nullable=False),
        
        # Stats
        sa.Column('rating', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('review_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('enrollment_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('placement_rate', sa.Integer(), nullable=True),
        
        # Media
        sa.Column('featured_image', sa.String(length=500), nullable=True),
        sa.Column('video_url', sa.String(length=500), nullable=True),
        
        # Instructor
        sa.Column('instructor_name', sa.String(length=255), nullable=True),
        sa.Column('instructor_title', sa.String(length=255), nullable=True),
        sa.Column('instructor_bio', sa.Text(), nullable=True),
        sa.Column('instructor_image', sa.String(length=500), nullable=True),
        
        # JSON fields (stored as Text)
        sa.Column('curriculum', sa.Text(), nullable=True),
        sa.Column('learning_outcomes', sa.Text(), nullable=True),
        sa.Column('prerequisites', sa.Text(), nullable=True),
        sa.Column('projects', sa.Text(), nullable=True),
        
        # Certification
        sa.Column('certification_name', sa.String(length=255), nullable=True),
        sa.Column('certification_authority', sa.String(length=255), nullable=True),
        
        # SEO
        sa.Column('meta_title', sa.String(length=255), nullable=True),
        sa.Column('meta_description', sa.String(length=500), nullable=True),
        
        # Batch info
        sa.Column('next_batch_date', sa.DateTime(timezone=True), nullable=True),
        
        # Status
        sa.Column('status', sa.String(length=50), server_default='draft', nullable=False),
        sa.Column('featured', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=func.now(), nullable=False),
        
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
        sa.ForeignKeyConstraint(['category_id'], ['course_categories.id'], ondelete='RESTRICT')
    )
    op.create_index(op.f('ix_courses_slug'), 'courses', ['slug'], unique=True)

    # Create course_skills association table
    op.create_table(
        'course_skills',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('course_id', 'skill_id'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE')
    )

    # Create course_enrollments table
    op.create_table(
        'course_enrollments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        
        # Student Info
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        
        # Optional Info
        sa.Column('education', sa.String(length=255), nullable=True),
        sa.Column('experience', sa.String(length=100), nullable=True),
        sa.Column('current_role', sa.String(length=255), nullable=True),
        sa.Column('linkedin_url', sa.String(length=500), nullable=True),
        
        # Course Interest
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('preferred_batch', sa.String(length=100), nullable=True),
        
        # Source tracking
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('utm_campaign', sa.String(length=255), nullable=True),
        sa.Column('utm_source', sa.String(length=100), nullable=True),
        sa.Column('utm_medium', sa.String(length=100), nullable=True),
        
        # Message
        sa.Column('message', sa.Text(), nullable=True),
        
        # Status tracking
        sa.Column('status', sa.String(length=50), server_default='new', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('assigned_to', sa.String(length=255), nullable=True),
        
        # Follow-up tracking
        sa.Column('last_contacted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('next_followup_at', sa.DateTime(timezone=True), nullable=True),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=func.now(), nullable=False),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='SET NULL')
    )
    op.create_index(op.f('ix_course_enrollments_email'), 'course_enrollments', ['email'], unique=False)

    # Insert default course categories
    op.execute("""
        INSERT INTO course_categories (name, slug, description, icon, display_order, is_active, created_at, updated_at)
        VALUES 
        ('Data Science & Analytics', 'data-science', 'Learn data analysis, visualization, and machine learning', 'chart-bar', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('Cloud & DevOps', 'cloud', 'Master cloud platforms and DevOps practices', 'cloud', 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('AI & Machine Learning', 'ai-ml', 'Dive into AI, deep learning, and generative AI', 'brain', 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('Full Stack Development', 'fullstack', 'Build modern web and mobile applications', 'code', 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('Business & Leadership', 'business', 'Develop business and management skills', 'briefcase', 5, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)


def downgrade():
    op.drop_index(op.f('ix_course_enrollments_email'), table_name='course_enrollments')
    op.drop_table('course_enrollments')
    op.drop_table('course_skills')
    op.drop_index(op.f('ix_courses_slug'), table_name='courses')
    op.drop_table('courses')
    op.drop_index(op.f('ix_course_categories_slug'), table_name='course_categories')
    op.drop_table('course_categories')
    op.drop_index(op.f('ix_skills_slug'), table_name='skills')
    op.drop_table('skills')
