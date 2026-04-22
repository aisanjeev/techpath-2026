"""Create app_settings table for configurable settings.

Revision ID: e5f6g7h8i9j0
Revises: d4e5f6g7h8i9
Create Date: 2025-12-19
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "e5f6g7h8i9j0"
down_revision = "d4e5f6g7h8i9"  # Previous secrets migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create app_settings table with initial seed data."""
    
    # Create app_settings table
    op.create_table(
        "app_settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("key", sa.String(100), nullable=False),
        sa.Column("value", sa.Text(), nullable=True),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("value_type", sa.String(20), nullable=False, server_default="string"),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["updated_by_id"], ["users.id"], ondelete="SET NULL"),
    )
    
    # Create indexes
    op.create_index("ix_app_settings_key", "app_settings", ["key"], unique=True)
    op.create_index("ix_app_settings_category", "app_settings", ["category"])
    
    # Seed initial settings
    settings_table = sa.table(
        "app_settings",
        sa.column("key", sa.String),
        sa.column("value", sa.Text),
        sa.column("display_name", sa.String),
        sa.column("description", sa.Text),
        sa.column("category", sa.String),
        sa.column("value_type", sa.String),
        sa.column("display_order", sa.Integer),
    )
    
    initial_settings = [
        # Email Settings
        {
            "key": "admin_notification_email",
            "value": "admin@techpath.biz",
            "display_name": "Admin Notification Email",
            "description": "Email address to receive form submissions and notifications",
            "category": "email",
            "value_type": "email",
            "display_order": 1,
        },
        {
            "key": "contact_form_recipients",
            "value": "admin@techpath.biz",
            "display_name": "Contact Form Recipients",
            "description": "Comma-separated email addresses for contact form notifications",
            "category": "email",
            "value_type": "string",
            "display_order": 2,
        },
        {
            "key": "enrollment_notification_email",
            "value": "training@techpath.biz",
            "display_name": "Course Enrollment Notifications",
            "description": "Email address for course enrollment notifications",
            "category": "email",
            "value_type": "email",
            "display_order": 3,
        },
        
        # Company Info
        {
            "key": "company_name",
            "value": "TechPath Professional Services",
            "display_name": "Company Name",
            "description": "Your company name displayed across the site",
            "category": "general",
            "value_type": "string",
            "display_order": 1,
        },
        {
            "key": "company_email",
            "value": "info@techpath.biz",
            "display_name": "Company Email",
            "description": "Public contact email displayed on the website",
            "category": "general",
            "value_type": "email",
            "display_order": 2,
        },
        {
            "key": "company_phone",
            "value": "",
            "display_name": "Company Phone",
            "description": "Public phone number displayed on the website",
            "category": "general",
            "value_type": "string",
            "display_order": 3,
        },
        {
            "key": "company_address",
            "value": "",
            "display_name": "Company Address",
            "description": "Business address for footer/contact page",
            "category": "general",
            "value_type": "string",
            "display_order": 4,
        },
        
        # Social Media
        {
            "key": "social_linkedin",
            "value": "",
            "display_name": "LinkedIn URL",
            "description": "Your company LinkedIn page URL",
            "category": "general",
            "value_type": "string",
            "display_order": 10,
        },
        {
            "key": "social_twitter",
            "value": "",
            "display_name": "Twitter/X URL",
            "description": "Your company Twitter/X profile URL",
            "category": "general",
            "value_type": "string",
            "display_order": 11,
        },
        {
            "key": "social_facebook",
            "value": "",
            "display_name": "Facebook URL",
            "description": "Your company Facebook page URL",
            "category": "general",
            "value_type": "string",
            "display_order": 12,
        },
        
        # SEO Settings
        {
            "key": "seo_default_title",
            "value": "TechPath - IT Services & Gen AI Solutions",
            "display_name": "Default Page Title",
            "description": "Default title for pages without a specific title",
            "category": "seo",
            "value_type": "string",
            "display_order": 1,
        },
        {
            "key": "seo_default_description",
            "value": "Professional IT services and Generative AI solutions for modern businesses",
            "display_name": "Default Meta Description",
            "description": "Default meta description for SEO",
            "category": "seo",
            "value_type": "string",
            "display_order": 2,
        },
        {
            "key": "google_analytics_id",
            "value": "",
            "display_name": "Google Analytics ID",
            "description": "Your GA4 measurement ID (e.g., G-XXXXXXXXXX)",
            "category": "seo",
            "value_type": "string",
            "display_order": 3,
        },
        {
            "key": "gtm_id",
            "value": "",
            "display_name": "Google Tag Manager ID",
            "description": "GTM container ID (e.g. GTM-XXXXXXX). Leave blank to disable.",
            "category": "seo",
            "value_type": "string",
            "display_order": 4,
        },
    ]
    
    op.bulk_insert(settings_table, initial_settings)


def downgrade() -> None:
    """Drop app_settings table."""
    op.drop_index("ix_app_settings_category", table_name="app_settings")
    op.drop_index("ix_app_settings_key", table_name="app_settings")
    op.drop_table("app_settings")

