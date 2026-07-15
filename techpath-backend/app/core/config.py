"""Application configuration with environment variable support."""
import json
from typing import List, Optional
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # -----------------
    # Application
    # -----------------
    APP_NAME: str = "TechPath API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")

    # -----------------
    # Server
    # -----------------
    API_BASE_URL: str = Field(default="http://localhost:8000")
    FRONTEND_URL: str = Field(default="http://localhost:4321")
    ALLOWED_HOSTS: List[str] = Field(default=["localhost", "127.0.0.1"])
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:4321", "http://localhost:3000"]
    )

    @field_validator("ALLOWED_HOSTS", "CORS_ORIGINS", mode="before")
    @classmethod
    def parse_list(cls, v: str | List[str]) -> List[str]:
        """Parse JSON string to list if needed."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v

    # -----------------
    # Database
    # -----------------
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./data/techpath.db")
    DATABASE_ECHO: bool = Field(default=False)

    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite database."""
        return "sqlite" in self.DATABASE_URL.lower()

    @property
    def is_mysql(self) -> bool:
        """Check if using MySQL database."""
        return "mysql" in self.DATABASE_URL.lower()

    # -----------------
    # Authentication
    # -----------------
    SECRET_KEY: str
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    # -----------------
    # Storage
    # -----------------
    STORAGE_TYPE: str = Field(default="local")  # "local" or "azure"
    LOCAL_UPLOAD_PATH: str = Field(default="./data/uploads")
    AZURE_STORAGE_CONNECTION_STRING: str = Field(default="")
    AZURE_BLOB_CONTAINER: str = Field(default="techpath-uploads")

    @property
    def is_local_storage(self) -> bool:
        """Check if using local filesystem storage."""
        return self.STORAGE_TYPE.lower() == "local"

    @property
    def is_azure_storage(self) -> bool:
        """Check if using Azure Blob Storage."""
        return self.STORAGE_TYPE.lower() == "azure"

    # -----------------
    # Azure OpenAI
    # -----------------
    AZURE_OPENAI_ENDPOINT: str = Field(default="")
    AZURE_OPENAI_KEY: str = Field(default="")
    AZURE_OPENAI_DEPLOYMENT: str = Field(default="gpt-4")
    AZURE_OPENAI_API_VERSION: str = Field(default="2024-02-15-preview")

    @property
    def has_openai_config(self) -> bool:
        """Check if Azure OpenAI is configured."""
        return bool(self.AZURE_OPENAI_ENDPOINT and self.AZURE_OPENAI_KEY)

    # -----------------
    # Email (SMTP)
    # -----------------
    SMTP_SERVER: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    FROM_EMAIL: str = Field(default="noreply@techpath.biz")
    ADMIN_EMAIL: str = Field(default="sanjeev@techpath.biz")

    # -----------------
    # Firebase
    # -----------------
    FIREBASE_PROJECT_ID: str = Field(default="techpath-main")
    # Optional: path to a Firebase service-account JSON key file.
    # Download from Firebase Console → Project Settings → Service Accounts
    # → Generate New Private Key.  Leave blank to rely on Application Default
    # Credentials (ADC) or the project-ID-only mode (verify_id_token only).
    FIREBASE_SERVICE_ACCOUNT_PATH: str = Field(default="")

    @property
    def has_smtp_config(self) -> bool:
        """Check if SMTP is configured."""
        return bool(self.SMTP_USER and self.SMTP_PASSWORD)

    # -----------------
    # Redis (Optional)
    # -----------------
    REDIS_URL: Optional[str] = Field(default=None)

    # -----------------
    # Azure Key Vault
    # -----------------
    AZURE_TENANT_ID: str = Field(default="")
    AZURE_CLIENT_ID: str = Field(default="")
    AZURE_CLIENT_SECRET: str = Field(default="")
    AZURE_KEYVAULT_URL: str = Field(default="")

    @property
    def has_keyvault_config(self) -> bool:
        """Check if Azure Key Vault is configured."""
        return bool(
            self.AZURE_TENANT_ID
            and self.AZURE_CLIENT_ID
            and self.AZURE_CLIENT_SECRET
            and self.AZURE_KEYVAULT_URL
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()

