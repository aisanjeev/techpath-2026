"""Pydantic schemas for secret management."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SecretMetadataBase(BaseModel):
    """Base schema for secret metadata."""
    
    key_name: str = Field(..., max_length=100, description="Environment variable name")
    display_name: str = Field(..., max_length=200, description="Human-readable name")
    description: Optional[str] = Field(None, description="Description of the secret")
    category: str = Field(..., max_length=50, description="Category: azure_openai, storage, email")
    is_required: bool = Field(default=False, description="Whether this secret is required")
    display_order: int = Field(default=0, description="Display order in UI")


class SecretMetadataResponse(SecretMetadataBase):
    """Response schema for secret metadata."""
    
    id: int
    is_set: bool = Field(..., description="Whether the secret is set in Key Vault")
    updated_by_id: Optional[int] = None
    updated_by_name: Optional[str] = Field(None, description="Name of user who last updated")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SecretValueUpdate(BaseModel):
    """Schema for updating a secret value."""
    
    value: str = Field(..., min_length=1, description="The secret value to store")


class SecretValueResponse(BaseModel):
    """Response when a secret value is requested."""
    
    key_name: str
    value: Optional[str] = Field(None, description="The secret value (may be masked)")
    is_masked: bool = Field(default=True, description="Whether the value is masked")
    is_set: bool = Field(..., description="Whether the secret exists in Key Vault")


class SecretCategoryResponse(BaseModel):
    """Response schema for secret categories."""
    
    category: str
    display_name: str
    secrets: list[SecretMetadataResponse]


class SecretsStatusResponse(BaseModel):
    """Response schema for overall secrets status."""
    
    total_secrets: int
    set_secrets: int
    unset_secrets: int
    required_unset: int
    keyvault_configured: bool


# Category display names mapping
CATEGORY_DISPLAY_NAMES = {
    "email": "Email (Azure Communication)",
    "azure_openai": "Azure OpenAI",
    "storage": "Azure Storage",
    "firebase": "Firebase Authentication",
}


def get_category_display_name(category: str) -> str:
    """Get human-readable category name."""
    return CATEGORY_DISPLAY_NAMES.get(category, category.replace("_", " ").title())

