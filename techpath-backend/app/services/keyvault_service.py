"""Azure Key Vault service for managing secrets."""
from typing import Optional

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

from app.core.config import settings


class KeyVaultService:
    """Service for interacting with Azure Key Vault."""

    def __init__(self) -> None:
        """Initialize the Key Vault client if configured."""
        self._client: Optional[SecretClient] = None
        self._initialized = False

    def _get_client(self) -> SecretClient:
        """Get or create the Key Vault client."""
        if not self._initialized:
            if not settings.has_keyvault_config:
                raise ValueError(
                    "Azure Key Vault is not configured. "
                    "Set AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_KEYVAULT_URL."
                )

            credential = ClientSecretCredential(
                tenant_id=settings.AZURE_TENANT_ID,
                client_id=settings.AZURE_CLIENT_ID,
                client_secret=settings.AZURE_CLIENT_SECRET,
            )
            self._client = SecretClient(
                vault_url=settings.AZURE_KEYVAULT_URL,
                credential=credential,
            )
            self._initialized = True

        if self._client is None:
            raise ValueError("Key Vault client not initialized")

        return self._client

    def is_configured(self) -> bool:
        """Check if Key Vault is configured."""
        return settings.has_keyvault_config

    async def get_secret(self, name: str) -> Optional[str]:
        """
        Retrieve a secret value from Key Vault.

        Args:
            name: The name of the secret (will be converted to Key Vault format)

        Returns:
            The secret value or None if not found
        """
        if not self.is_configured():
            return None

        try:
            client = self._get_client()
            # Convert underscore to hyphen for Key Vault naming convention
            kv_name = name.replace("_", "-").lower()
            secret = client.get_secret(kv_name)
            return secret.value
        except ResourceNotFoundError:
            return None
        except HttpResponseError as e:
            raise ValueError(f"Error retrieving secret '{name}': {e.message}")

    async def set_secret(self, name: str, value: str) -> bool:
        """
        Store or update a secret in Key Vault.

        Args:
            name: The name of the secret
            value: The secret value to store

        Returns:
            True if successful
        """
        if not self.is_configured():
            raise ValueError("Key Vault is not configured")

        try:
            client = self._get_client()
            # Convert underscore to hyphen for Key Vault naming convention
            kv_name = name.replace("_", "-").lower()
            client.set_secret(kv_name, value)
            return True
        except HttpResponseError as e:
            raise ValueError(f"Error setting secret '{name}': {e.message}")

    async def delete_secret(self, name: str) -> bool:
        """
        Delete a secret from Key Vault.

        Args:
            name: The name of the secret

        Returns:
            True if successful
        """
        if not self.is_configured():
            raise ValueError("Key Vault is not configured")

        try:
            client = self._get_client()
            # Convert underscore to hyphen for Key Vault naming convention
            kv_name = name.replace("_", "-").lower()
            # Start deletion
            poller = client.begin_delete_secret(kv_name)
            # Wait for deletion to complete
            poller.wait()
            return True
        except ResourceNotFoundError:
            return False
        except HttpResponseError as e:
            raise ValueError(f"Error deleting secret '{name}': {e.message}")

    async def secret_exists(self, name: str) -> bool:
        """
        Check if a secret exists in Key Vault.

        Args:
            name: The name of the secret

        Returns:
            True if the secret exists
        """
        if not self.is_configured():
            return False

        try:
            client = self._get_client()
            kv_name = name.replace("_", "-").lower()
            client.get_secret(kv_name)
            return True
        except ResourceNotFoundError:
            return False
        except HttpResponseError:
            return False

    async def list_secrets(self) -> list[str]:
        """
        List all secret names in Key Vault.

        Returns:
            List of secret names (converted back to underscore format)
        """
        if not self.is_configured():
            return []

        try:
            client = self._get_client()
            secrets = []
            for secret_properties in client.list_properties_of_secrets():
                # Convert hyphen back to underscore
                name = secret_properties.name.replace("-", "_").upper()
                secrets.append(name)
            return secrets
        except HttpResponseError as e:
            raise ValueError(f"Error listing secrets: {e.message}")

    def get_masked_value(self, value: str, visible_chars: int = 4) -> str:
        """
        Return a masked version of a secret value.

        Args:
            value: The secret value
            visible_chars: Number of characters to show at the end

        Returns:
            Masked string like "••••••••abcd"
        """
        if len(value) <= visible_chars:
            return "•" * len(value)
        return "•" * (len(value) - visible_chars) + value[-visible_chars:]


# Global instance
keyvault_service = KeyVaultService()

