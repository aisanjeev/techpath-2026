"""
Secrets Loader Service - Loads secrets from Azure Key Vault at application startup.

This service fetches configured secrets from Key Vault and makes them available
to the application through a runtime config store.
"""
import logging
from typing import Optional

from app.services.keyvault_service import keyvault_service

logger = logging.getLogger(__name__)


class RuntimeSecrets:
    """
    Runtime secrets loaded from Azure Key Vault.
    
    These values override the environment variables at runtime.
    """
    
    def __init__(self) -> None:
        self._secrets: dict[str, str] = {}
        self._loaded = False
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret value by key."""
        return self._secrets.get(key, default)
    
    def set(self, key: str, value: str) -> None:
        """Set a secret value."""
        self._secrets[key] = value
    
    def is_loaded(self) -> bool:
        """Check if secrets have been loaded."""
        return self._loaded
    
    def mark_loaded(self) -> None:
        """Mark secrets as loaded."""
        self._loaded = True
    
    def get_all(self) -> dict[str, str]:
        """Get all loaded secrets (for debugging)."""
        return dict(self._secrets)


# Global runtime secrets store
runtime_secrets = RuntimeSecrets()


# Keys to load from Key Vault
SECRETS_TO_LOAD = [
    "AZURE_STORAGE_CONNECTION_STRING",
    "AZURE_BLOB_CONTAINER",
    "STORAGE_TYPE",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_KEY",
    "AZURE_OPENAI_DEPLOYMENT",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_COMMUNICATION_EMAIL_CONNECTION_STRING",
    "SENDER_ADDRESS",
]


async def load_secrets_from_keyvault(update_db: bool = False) -> dict[str, bool]:
    """
    Load secrets from Azure Key Vault into runtime config.
    
    Args:
        update_db: If True, also update the is_set status in the database
    
    Returns a dict with key names and whether they were successfully loaded.
    """
    results: dict[str, bool] = {}
    
    if not keyvault_service.is_configured():
        logger.warning("Azure Key Vault is not configured. Skipping secrets loading.")
        return {key: False for key in SECRETS_TO_LOAD}
    
    logger.info("Loading secrets from Azure Key Vault...")
    
    for key in SECRETS_TO_LOAD:
        try:
            value = await keyvault_service.get_secret(key)
            if value:
                runtime_secrets.set(key, value)
                results[key] = True
                logger.info(f"✓ Loaded secret: {key}")
            else:
                results[key] = False
                logger.debug(f"✗ Secret not found: {key}")
        except Exception as e:
            results[key] = False
            logger.error(f"✗ Error loading secret {key}: {e}")
    
    runtime_secrets.mark_loaded()
    
    loaded_count = sum(1 for v in results.values() if v)
    logger.info(f"Loaded {loaded_count}/{len(SECRETS_TO_LOAD)} secrets from Key Vault")
    
    # Update database is_set status if requested
    if update_db:
        await _update_db_status(results)
    
    return results


async def _update_db_status(results: dict[str, bool]) -> None:
    """Update the is_set status in the database based on Key Vault results."""
    try:
        from app.db.session import AsyncSessionLocal
        from app.crud.secret import secret_metadata_crud
        
        async with AsyncSessionLocal() as db:
            for key, is_set in results.items():
                await secret_metadata_crud.update_is_set(db, key, is_set)
        
        logger.info("Updated secrets status in database")
    except Exception as e:
        logger.error(f"Failed to update secrets status in database: {e}")


def get_secret(key: str, env_fallback: Optional[str] = None) -> Optional[str]:
    """
    Get a secret value, checking Key Vault first, then falling back to env var.
    
    Args:
        key: The secret key name
        env_fallback: The fallback value from environment variable
        
    Returns:
        The secret value from Key Vault if available, otherwise the env fallback
    """
    # Try runtime secrets (loaded from Key Vault) first
    kv_value = runtime_secrets.get(key)
    if kv_value:
        return kv_value
    
    # Fall back to environment variable
    return env_fallback

