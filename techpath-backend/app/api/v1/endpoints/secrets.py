"""API endpoints for secret management via Azure Key Vault."""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin_user
from app.core.exceptions import NotFoundError, ValidationError
from app.db.session import get_db
from app.models.user import User
from app.crud.secret import secret_metadata_crud
from app.services.keyvault_service import keyvault_service
from app.schemas.secret import (
    SecretMetadataResponse,
    SecretValueUpdate,
    SecretValueResponse,
    SecretCategoryResponse,
    SecretsStatusResponse,
    get_category_display_name,
)

router = APIRouter()


def _to_response(secret, include_user_name: bool = True) -> SecretMetadataResponse:
    """Convert SecretMetadata model to response schema."""
    return SecretMetadataResponse(
        id=secret.id,
        key_name=secret.key_name,
        display_name=secret.display_name,
        description=secret.description,
        category=secret.category,
        is_required=secret.is_required,
        is_set=secret.is_set,
        display_order=secret.display_order,
        updated_by_id=secret.updated_by_id,
        updated_by_name=secret.updated_by.name if include_user_name and secret.updated_by else None,
        created_at=secret.created_at,
        updated_at=secret.updated_at,
    )


@router.get("/", response_model=list[SecretMetadataResponse])
async def list_secrets(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> list[SecretMetadataResponse]:
    """
    List all secret metadata (admin only).
    
    Returns metadata only - actual values are stored in Azure Key Vault.
    """
    secrets = await secret_metadata_crud.get_all(db, category=category)
    return [_to_response(s) for s in secrets]


@router.get("/status", response_model=SecretsStatusResponse)
async def get_secrets_status(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SecretsStatusResponse:
    """
    Get overall status of secrets configuration (admin only).
    """
    all_secrets = await secret_metadata_crud.get_all(db)
    required_unset = await secret_metadata_crud.get_required_unset(db)
    
    set_count = sum(1 for s in all_secrets if s.is_set)
    
    return SecretsStatusResponse(
        total_secrets=len(all_secrets),
        set_secrets=set_count,
        unset_secrets=len(all_secrets) - set_count,
        required_unset=len(required_unset),
        keyvault_configured=keyvault_service.is_configured(),
    )


@router.get("/categories", response_model=list[SecretCategoryResponse])
async def list_secrets_by_category(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> list[SecretCategoryResponse]:
    """
    List all secrets grouped by category (admin only).
    """
    categories = await secret_metadata_crud.get_categories(db)
    result = []
    
    for category in categories:
        secrets = await secret_metadata_crud.get_by_category(db, category)
        result.append(
            SecretCategoryResponse(
                category=category,
                display_name=get_category_display_name(category),
                secrets=[_to_response(s) for s in secrets],
            )
        )
    
    return result


@router.get("/{key_name}", response_model=SecretValueResponse)
async def get_secret_value(
    key_name: str,
    reveal: bool = Query(False, description="Whether to reveal the actual value"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SecretValueResponse:
    """
    Get a secret value from Key Vault (admin only).
    
    By default, the value is masked. Set reveal=true to see the actual value.
    """
    # Check metadata exists
    secret_meta = await secret_metadata_crud.get_by_key(db, key_name)
    if not secret_meta:
        raise NotFoundError(f"Secret '{key_name}' not found")
    
    # Check Key Vault configuration
    if not keyvault_service.is_configured():
        return SecretValueResponse(
            key_name=key_name,
            value=None,
            is_masked=True,
            is_set=False,
        )
    
    # Get value from Key Vault
    value = await keyvault_service.get_secret(key_name)
    
    if value is None:
        return SecretValueResponse(
            key_name=key_name,
            value=None,
            is_masked=True,
            is_set=False,
        )
    
    # Return masked or actual value
    if reveal:
        return SecretValueResponse(
            key_name=key_name,
            value=value,
            is_masked=False,
            is_set=True,
        )
    else:
        return SecretValueResponse(
            key_name=key_name,
            value=keyvault_service.get_masked_value(value),
            is_masked=True,
            is_set=True,
        )


@router.put("/{key_name}", response_model=SecretMetadataResponse)
async def update_secret_value(
    key_name: str,
    data: SecretValueUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SecretMetadataResponse:
    """
    Update a secret value in Key Vault (admin only).
    
    Creates or updates the secret in Azure Key Vault.
    """
    # Check metadata exists
    secret_meta = await secret_metadata_crud.get_by_key(db, key_name)
    if not secret_meta:
        raise NotFoundError(f"Secret '{key_name}' not found in configuration")
    
    # Check Key Vault configuration
    if not keyvault_service.is_configured():
        raise ValidationError(
            "Azure Key Vault is not configured. "
            "Please set AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_KEYVAULT_URL."
        )
    
    # Store in Key Vault
    try:
        await keyvault_service.set_secret(key_name, data.value)
    except ValueError as e:
        raise ValidationError(str(e))
    
    # Update metadata
    updated = await secret_metadata_crud.update_is_set(
        db, key_name, is_set=True, updated_by_id=current_admin.id
    )
    
    if not updated:
        raise NotFoundError(f"Secret '{key_name}' not found")
    
    return _to_response(updated)


@router.delete("/{key_name}", response_model=SecretMetadataResponse)
async def delete_secret_value(
    key_name: str,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SecretMetadataResponse:
    """
    Delete a secret value from Key Vault (admin only).
    
    Removes the secret from Azure Key Vault but keeps the metadata.
    """
    # Check metadata exists
    secret_meta = await secret_metadata_crud.get_by_key(db, key_name)
    if not secret_meta:
        raise NotFoundError(f"Secret '{key_name}' not found")
    
    # Check Key Vault configuration
    if not keyvault_service.is_configured():
        raise ValidationError("Azure Key Vault is not configured")
    
    # Delete from Key Vault
    try:
        await keyvault_service.delete_secret(key_name)
    except ValueError as e:
        raise ValidationError(str(e))
    
    # Update metadata
    updated = await secret_metadata_crud.update_is_set(
        db, key_name, is_set=False, updated_by_id=current_admin.id
    )
    
    if not updated:
        raise NotFoundError(f"Secret '{key_name}' not found")
    
    return _to_response(updated)


@router.post("/sync", response_model=list[SecretMetadataResponse])
async def sync_secrets_status(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> list[SecretMetadataResponse]:
    """
    Sync is_set status from Key Vault for all secrets (admin only).
    
    Checks each secret in Key Vault and updates the is_set flag in the database.
    """
    if not keyvault_service.is_configured():
        raise ValidationError("Azure Key Vault is not configured")
    
    all_secrets = await secret_metadata_crud.get_all(db)
    updated_secrets = []
    
    for secret in all_secrets:
        exists = await keyvault_service.secret_exists(secret.key_name)
        if exists != secret.is_set:
            await secret_metadata_crud.update_is_set(
                db, secret.key_name, is_set=exists, updated_by_id=current_admin.id
            )
        
        # Refresh the secret to get updated data
        refreshed = await secret_metadata_crud.get_by_key(db, secret.key_name)
        if refreshed:
            updated_secrets.append(_to_response(refreshed))
    
    return updated_secrets

