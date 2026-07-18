"""Unified storage service for local filesystem and Azure Blob Storage."""
import logging
import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import BinaryIO, Optional

import aiofiles
import aiofiles.os

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.utils.helpers import sanitize_filename

logger = logging.getLogger(__name__)


class BaseStorageService(ABC):
    """Abstract base class for storage services."""

    @abstractmethod
    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        folder: str = "",
        content_type: Optional[str] = None,
    ) -> str:
        """Upload a file and return its URL."""
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file by its path/URL."""
        pass

    @abstractmethod
    async def get_file_url(self, file_path: str) -> str:
        """Get the public URL for a file."""
        pass

    @abstractmethod
    async def file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        pass

    @abstractmethod
    async def delete_recording(self, stream_path: str) -> bool:
        """Delete all recording files associated with a stream path."""
        pass


class LocalStorageService(BaseStorageService):
    """Local filesystem storage service for development."""

    def __init__(self, upload_path: str) -> None:
        self.upload_path = Path(upload_path)
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensure the upload directory exists."""
        self.upload_path.mkdir(parents=True, exist_ok=True)

    def _generate_unique_filename(self, filename: str) -> str:
        """Generate a unique filename to prevent collisions."""
        safe_name = sanitize_filename(filename)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]

        # Split name and extension
        parts = safe_name.rsplit(".", 1)
        name = parts[0]
        ext = f".{parts[1]}" if len(parts) > 1 else ""

        return f"{name}_{timestamp}_{unique_id}{ext}"

    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        folder: str = "",
        content_type: Optional[str] = None,
    ) -> str:
        """Upload a file to local storage."""
        try:
            # Create folder if specified
            target_dir = self.upload_path / folder if folder else self.upload_path
            target_dir.mkdir(parents=True, exist_ok=True)

            # Generate unique filename
            unique_filename = self._generate_unique_filename(filename)
            file_path = target_dir / unique_filename

            # Write file
            content = file.read()
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(content)

            # Return relative path from upload directory
            relative_path = f"{folder}/{unique_filename}" if folder else unique_filename
            logger.info(f"File uploaded to local storage: {relative_path}")
            return relative_path

        except Exception as e:
            logger.error(f"Error uploading file to local storage: {e}")
            raise ExternalServiceError("Local Storage", str(e))

    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from local storage."""
        try:
            full_path = self.upload_path / file_path
            if await aiofiles.os.path.exists(full_path):
                await aiofiles.os.remove(full_path)
                logger.info(f"File deleted from local storage: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file from local storage: {e}")
            return False

    async def delete_recording(self, stream_path: str) -> bool:
        """Delete all recording files associated with a stream path."""
        import os
        try:
            target_dir = self.upload_path / stream_path
            if target_dir.exists() and target_dir.is_dir():
                deleted = False
                for f in os.listdir(target_dir):
                    if f.endswith(".mp4"):
                        file_path = target_dir / f
                        os.remove(file_path)
                        logger.info(f"Deleted recording from local storage: {file_path}")
                        deleted = True
                # Clean up empty dir
                if not os.listdir(target_dir):
                    os.rmdir(target_dir)
                return deleted
            return False
        except Exception as e:
            logger.error(f"Error deleting recording from local storage: {e}")
            return False

    async def get_file_url(self, file_path: str) -> str:
        """Get the URL for a local file (relative path for API serving)."""
        return f"/uploads/{file_path}"

    async def file_exists(self, file_path: str) -> bool:
        """Check if a file exists in local storage."""
        full_path = self.upload_path / file_path
        return await aiofiles.os.path.exists(full_path)

    async def resolve_url(self, path_or_url: str) -> str:
        """Return a valid URL from a local path or existing local URL."""
        if not path_or_url:
            return path_or_url
        if path_or_url.startswith("/uploads/"):
            return path_or_url
        return await self.get_file_url(path_or_url)


class AzureBlobStorageService(BaseStorageService):
    """Azure Blob Storage service for production."""

    def __init__(
        self,
        connection_string: str,
        container_name: str,
    ) -> None:
        self.connection_string = connection_string
        self.container_name = container_name
        self._client = None

    def _get_client(self):
        """Get or create the blob service client."""
        if self._client is None:
            try:
                from azure.storage.blob import BlobServiceClient

                self._client = BlobServiceClient.from_connection_string(
                    self.connection_string
                )
            except ImportError:
                raise ExternalServiceError(
                    "Azure Blob Storage",
                    "azure-storage-blob package not installed",
                )
            except Exception as e:
                raise ExternalServiceError("Azure Blob Storage", str(e))
        return self._client

    def _get_container_client(self):
        """Get the container client."""
        return self._get_client().get_container_client(self.container_name)

    def _generate_blob_name(self, filename: str, folder: str = "") -> str:
        """Generate a unique blob name."""
        safe_name = sanitize_filename(filename)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]

        parts = safe_name.rsplit(".", 1)
        name = parts[0]
        ext = f".{parts[1]}" if len(parts) > 1 else ""

        blob_name = f"{name}_{timestamp}_{unique_id}{ext}"

        if folder:
            blob_name = f"{folder}/{blob_name}"

        return blob_name

    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        folder: str = "",
        content_type: Optional[str] = None,
    ) -> str:
        """Upload a file to Azure Blob Storage."""
        try:
            from azure.storage.blob import ContentSettings

            blob_name = self._generate_blob_name(filename, folder)
            blob_client = self._get_container_client().get_blob_client(blob_name)

            content = file.read()
            content_settings = None
            if content_type:
                content_settings = ContentSettings(content_type=content_type)

            blob_client.upload_blob(
                content,
                overwrite=True,
                content_settings=content_settings,
            )

            logger.info(f"File uploaded to Azure Blob Storage: {blob_name}")
            return blob_name

        except Exception as e:
            logger.error(f"Error uploading file to Azure Blob Storage: {e}")
            raise ExternalServiceError("Azure Blob Storage", str(e))

    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from Azure Blob Storage."""
        try:
            blob_client = self._get_container_client().get_blob_client(file_path)
            blob_client.delete_blob()
            logger.info(f"File deleted from Azure Blob Storage: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file from Azure Blob Storage: {e}")
            return False

    async def delete_recording(self, stream_path: str) -> bool:
        """Delete all recording files associated with a stream path."""
        try:
            container = self._get_container_client()
            blobs = container.list_blobs(name_starts_with=stream_path)
            deleted = False
            for blob in blobs:
                if blob.name.endswith(".mp4"):
                    container.delete_blob(blob.name)
                    logger.info(f"Deleted recording from Azure Blob Storage: {blob.name}")
                    deleted = True
            return deleted
        except Exception as e:
            logger.error(f"Error deleting recording from Azure Blob Storage: {e}")
            return False

    async def get_file_url(self, file_path: str) -> str:
        """Get the public URL for a blob."""
        try:
            from azure.storage.blob import generate_blob_sas, BlobSasPermissions

            blob_client = self._get_container_client().get_blob_client(file_path)

            # Generate SAS token for read access (valid for 7 days)
            sas_token = generate_blob_sas(
                account_name=self._get_client().account_name,
                container_name=self.container_name,
                blob_name=file_path,
                account_key=self._get_client().credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(days=7),
            )

            return f"{blob_client.url}?{sas_token}"
        except Exception as e:
            logger.error(f"Error generating blob URL: {e}")
            # Return direct URL without SAS (requires public access)
            return f"https://{self._get_client().account_name}.blob.core.windows.net/{self.container_name}/{file_path}"

    async def file_exists(self, file_path: str) -> bool:
        """Check if a blob exists."""
        try:
            blob_client = self._get_container_client().get_blob_client(file_path)
            return blob_client.exists()
        except Exception:
            return False

    async def resolve_url(self, path_or_url: str) -> str:
        """Get a fresh SAS URL from a blob path or an existing (possibly expired) SAS URL."""
        if not path_or_url:
            return path_or_url
        if path_or_url.startswith("https://"):
            try:
                blob_path = path_or_url.split(f"/{self.container_name}/", 1)[1].split("?")[0]
            except IndexError:
                return path_or_url
        else:
            blob_path = path_or_url
        return await self.get_file_url(blob_path)


def get_storage_service() -> BaseStorageService:
    """
    Factory function to get the appropriate storage service.
    
    Checks Key Vault runtime secrets first, then falls back to environment variables.
    """
    from app.services.secrets_loader import runtime_secrets
    
    # Get storage type (Key Vault takes precedence)
    storage_type = runtime_secrets.get("STORAGE_TYPE") or settings.STORAGE_TYPE
    
    if storage_type.lower() == "local":
        return LocalStorageService(settings.LOCAL_UPLOAD_PATH)
    elif storage_type.lower() == "azure":
        # Get Azure credentials (Key Vault takes precedence)
        connection_string = (
            runtime_secrets.get("AZURE_STORAGE_CONNECTION_STRING") 
            or settings.AZURE_STORAGE_CONNECTION_STRING
        )
        container_name = (
            runtime_secrets.get("AZURE_BLOB_CONTAINER") 
            or settings.AZURE_BLOB_CONTAINER
        )
        
        if not connection_string:
            raise ExternalServiceError(
                "Azure Blob Storage",
                "AZURE_STORAGE_CONNECTION_STRING not configured (check Key Vault or env vars)",
            )
        return AzureBlobStorageService(connection_string, container_name)
    else:
        # Default to local storage
        return LocalStorageService(settings.LOCAL_UPLOAD_PATH)


class StorageServiceProxy:
    """
    Lazy proxy for storage service that initializes on first use.
    
    This allows the storage service to use secrets loaded from Key Vault
    at application startup, rather than at module import time.
    """
    
    _instance: Optional[BaseStorageService] = None
    
    def _get_service(self) -> BaseStorageService:
        if self._instance is None:
            self._instance = get_storage_service()
        return self._instance
    
    def reset(self) -> None:
        """Reset the cached instance (useful after loading new secrets)."""
        self._instance = None
    
    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        folder: str = "",
        content_type: Optional[str] = None,
    ) -> str:
        return await self._get_service().upload_file(file, filename, folder, content_type)
    
    async def delete_file(self, file_path: str) -> bool:
        return await self._get_service().delete_file(file_path)
    
    async def delete_recording(self, stream_path: str) -> bool:
        return await self._get_service().delete_recording(stream_path)
    
    async def get_file_url(self, file_path: str) -> str:
        return await self._get_service().get_file_url(file_path)
    
    async def file_exists(self, file_path: str) -> bool:
        return await self._get_service().file_exists(file_path)

    async def resolve_url(self, path_or_url: str) -> str:
        return await self._get_service().resolve_url(path_or_url)


# Global storage service instance (lazy loaded)
storage_service = StorageServiceProxy()

