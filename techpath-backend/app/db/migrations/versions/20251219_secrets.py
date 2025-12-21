"""Create secret_metadata table for Key Vault secret management.

Revision ID: d4e5f6g7h8i9
Revises: c3d4e5f6g7h8
Create Date: 2025-12-19
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = "d4e5f6g7h8i9"
down_revision = "c3d4e5f6g7h8"  # Previous courses migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create secret_metadata table and seed default secrets."""
    
    # Create the secret_metadata table
    op.create_table(
        "secret_metadata",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("key_name", sa.String(length=100), nullable=False, comment="Environment variable name"),
        sa.Column("display_name", sa.String(length=200), nullable=False, comment="Human-readable name"),
        sa.Column("description", sa.Text(), nullable=True, comment="Description of the secret"),
        sa.Column("category", sa.String(length=50), nullable=False, comment="Category: azure_openai, storage, email"),
        sa.Column("is_required", sa.Boolean(), nullable=False, default=False, comment="Whether required"),
        sa.Column("is_set", sa.Boolean(), nullable=False, default=False, comment="Whether set in Key Vault"),
        sa.Column("display_order", sa.Integer(), nullable=False, default=0, comment="Display order in UI"),
        sa.Column("updated_by_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["updated_by_id"], ["users.id"], ondelete="SET NULL"),
    )
    
    # Create indexes
    op.create_index("ix_secret_metadata_key_name", "secret_metadata", ["key_name"], unique=True)
    op.create_index("ix_secret_metadata_category", "secret_metadata", ["category"], unique=False)
    
    # Seed default secrets
    now = datetime.utcnow().isoformat()
    
    secrets_data = [
        # Email (Azure Communication Services)
        {
            "key_name": "AZURE_COMMUNICATION_EMAIL_CONNECTION_STRING",
            "display_name": "Azure Communication Email Connection String",
            "description": "Connection string for Azure Communication Services email",
            "category": "email",
            "is_required": True,
            "is_set": False,
            "display_order": 1,
        },
        {
            "key_name": "SENDER_ADDRESS",
            "display_name": "Email Sender Address",
            "description": "The email address to send emails from (e.g., noreply@techpath.biz)",
            "category": "email",
            "is_required": True,
            "is_set": False,
            "display_order": 2,
        },
        # Azure OpenAI
        {
            "key_name": "AZURE_OPENAI_ENDPOINT",
            "display_name": "Azure OpenAI Endpoint",
            "description": "The endpoint URL for Azure OpenAI service",
            "category": "azure_openai",
            "is_required": True,
            "is_set": False,
            "display_order": 1,
        },
        {
            "key_name": "AZURE_OPENAI_KEY",
            "display_name": "Azure OpenAI API Key",
            "description": "API key for Azure OpenAI service",
            "category": "azure_openai",
            "is_required": True,
            "is_set": False,
            "display_order": 2,
        },
        {
            "key_name": "AZURE_OPENAI_DEPLOYMENT",
            "display_name": "Azure OpenAI Deployment Name",
            "description": "The deployment name for the OpenAI model (e.g., gpt-4)",
            "category": "azure_openai",
            "is_required": True,
            "is_set": False,
            "display_order": 3,
        },
        {
            "key_name": "AZURE_OPENAI_API_VERSION",
            "display_name": "Azure OpenAI API Version",
            "description": "API version for Azure OpenAI (e.g., 2024-02-15-preview)",
            "category": "azure_openai",
            "is_required": False,
            "is_set": False,
            "display_order": 4,
        },
        # Azure Storage
        {
            "key_name": "AZURE_STORAGE_CONNECTION_STRING",
            "display_name": "Azure Storage Connection String",
            "description": "Connection string for Azure Blob Storage",
            "category": "storage",
            "is_required": True,
            "is_set": False,
            "display_order": 1,
        },
        {
            "key_name": "AZURE_BLOB_CONTAINER",
            "display_name": "Azure Blob Container Name",
            "description": "The container name in Azure Blob Storage",
            "category": "storage",
            "is_required": True,
            "is_set": False,
            "display_order": 2,
        },
        {
            "key_name": "STORAGE_TYPE",
            "display_name": "Storage Type",
            "description": "Storage type: 'local' or 'azure'",
            "category": "storage",
            "is_required": False,
            "is_set": False,
            "display_order": 3,
        },
    ]
    
    # Insert seed data
    for secret in secrets_data:
        op.execute(
            sa.text(
                """
                INSERT INTO secret_metadata 
                (key_name, display_name, description, category, is_required, is_set, display_order, created_at, updated_at)
                VALUES (:key_name, :display_name, :description, :category, :is_required, :is_set, :display_order, :created_at, :updated_at)
                """
            ).bindparams(
                key_name=secret["key_name"],
                display_name=secret["display_name"],
                description=secret["description"],
                category=secret["category"],
                is_required=secret["is_required"],
                is_set=secret["is_set"],
                display_order=secret["display_order"],
                created_at=now,
                updated_at=now,
            )
        )


def downgrade() -> None:
    """Drop secret_metadata table."""
    op.drop_index("ix_secret_metadata_category", table_name="secret_metadata")
    op.drop_index("ix_secret_metadata_key_name", table_name="secret_metadata")
    op.drop_table("secret_metadata")

