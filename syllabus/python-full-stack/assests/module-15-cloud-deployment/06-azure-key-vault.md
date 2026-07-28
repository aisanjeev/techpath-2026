# Azure Key Vault — Production Secrets Management

**Module 15 — Cloud Deployment | Topic 6**

---

## Why Key Vault?

In previous modules, you stored secrets in:
- `.env` files (local development)
- GitHub Secrets (CI/CD pipelines)
- Container environment variables (runtime)

But for production, you need something more secure. **Azure Key Vault** is a centralized, encrypted vault for:
- API keys
- Database passwords
- JWT signing keys
- SSL certificates
- Encryption keys

> **Analogy:** Storing secrets in environment variables is like keeping your house keys under the doormat — convenient but not very secure. Key Vault is like a bank safety deposit box — proper security, access logging, and only authorized people can open it.

---

## Key Vault Advantages

| Feature | Env Variables | Key Vault |
|---------|--------------|-----------|
| Encryption | Not encrypted | Encrypted at rest and in transit |
| Access control | Anyone with server access | Fine-grained IAM policies |
| Audit logging | No | Full access logs |
| Rotation | Manual | Automated rotation possible |
| Versioning | No | Version history for every secret |
| Central management | Scattered across services | One place for all secrets |

---

## Setting Up Key Vault

### Step 1: Create the Vault

```bash
# Create a Key Vault
az keyvault create \
  --name techpath-kv \
  --resource-group techpath-rg \
  --location centralindia \
  --sku standard
```

### Step 2: Add Secrets

```bash
# Add secrets to the vault
az keyvault secret set \
  --vault-name techpath-kv \
  --name "database-url" \
  --value "postgresql+asyncpg://user:pass@host:5432/db"

az keyvault secret set \
  --vault-name techpath-kv \
  --name "jwt-secret-key" \
  --value "super-secure-jwt-signing-key-2024"

az keyvault secret set \
  --vault-name techpath-kv \
  --name "firebase-project-id" \
  --value "techpath-prod"

az keyvault secret set \
  --vault-name techpath-kv \
  --name "razorpay-api-key" \
  --value "rzp_live_xxxxxxxxxxxxx"
```

### Step 3: Retrieve Secrets

```bash
# Get a secret value
az keyvault secret show \
  --vault-name techpath-kv \
  --name "database-url" \
  --query value -o tsv

# List all secrets (names only, not values)
az keyvault secret list \
  --vault-name techpath-kv \
  --query '[].name' -o table
```

---

## Accessing Key Vault from Python

### Using azure-keyvault-secrets

```bash
pip install azure-keyvault-secrets azure-identity
```

```python
# app/services/secrets.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class AzureSecretsService:
    """Fetch secrets from Azure Key Vault."""

    def __init__(self, vault_url: str):
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=credential)

    def get_secret(self, name: str) -> str:
        """Get a secret value by name."""
        secret = self.client.get_secret(name)
        return secret.value

    def list_secrets(self) -> list[str]:
        """List all secret names."""
        return [s.name for s in self.client.list_properties_of_secrets()]

# Usage
vault = AzureSecretsService("https://techpath-kv.vault.azure.net/")
db_url = vault.get_secret("database-url")
jwt_key = vault.get_secret("jwt-secret-key")
```

### Integrating with FastAPI Config

```python
# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These can come from env vars OR Key Vault
    database_url: str = ""
    secret_key: str = ""
    firebase_project_id: str = ""

    # Key Vault settings
    azure_key_vault_url: str = ""

    class Config:
        env_file = ".env"

    def load_from_key_vault(self):
        """Load secrets from Azure Key Vault if configured."""
        if not self.azure_key_vault_url:
            return  # Skip if no vault configured (local dev)

        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        client = SecretClient(
            vault_url=self.azure_key_vault_url,
            credential=DefaultAzureCredential()
        )

        # Map Key Vault secret names to settings attributes
        secret_map = {
            "database-url": "database_url",
            "jwt-secret-key": "secret_key",
            "firebase-project-id": "firebase_project_id",
        }

        for vault_name, attr_name in secret_map.items():
            try:
                secret = client.get_secret(vault_name)
                setattr(self, attr_name, secret.value)
            except Exception:
                pass  # Use default/env value if vault secret not found

settings = Settings()
settings.load_from_key_vault()
```

---

## Granting Access to Your App

Your Container App or App Service needs permission to read from Key Vault.

### Using Managed Identity (Recommended)

**Managed Identity** lets Azure services authenticate to Key Vault without passwords.

```bash
# Enable managed identity on Container App
az containerapp identity assign \
  --name techpath-api \
  --resource-group techpath-rg \
  --system-assigned

# Get the identity's principal ID
PRINCIPAL_ID=$(az containerapp identity show \
  --name techpath-api \
  --resource-group techpath-rg \
  --query principalId -o tsv)

# Grant access to Key Vault
az keyvault set-policy \
  --name techpath-kv \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list
```

Now your app can access Key Vault secrets without any passwords or connection strings.

---

## Secret Rotation

Secrets should be rotated (changed) regularly. Key Vault makes this easy with versioning.

```bash
# Update a secret (creates a new version)
az keyvault secret set \
  --vault-name techpath-kv \
  --name "database-url" \
  --value "postgresql+asyncpg://new-user:new-pass@host:5432/db"

# The old version is still accessible if needed
az keyvault secret list-versions \
  --vault-name techpath-kv \
  --name "database-url"
```

Your app automatically gets the latest version the next time it reads the secret.

---

## Key Vault in CI/CD

Pull secrets from Key Vault during deployment:

```yaml
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Get secrets from Key Vault
        uses: azure/get-keyvault-secrets@v1
        with:
          keyvault: techpath-kv
          secrets: 'database-url, jwt-secret-key'
        id: kv-secrets

      - name: Deploy with secrets
        run: |
          az containerapp update \
            --name techpath-api \
            --resource-group techpath-rg \
            --set-env-vars \
              DATABASE_URL="${{ steps.kv-secrets.outputs.database-url }}" \
              SECRET_KEY="${{ steps.kv-secrets.outputs.jwt-secret-key }}"
```

---

## Best Practices

| Practice | Why |
|----------|-----|
| Use Managed Identity | No passwords to manage or leak |
| Least privilege access | Only grant `get` and `list`, not `set` or `delete` |
| Enable soft delete | Recover accidentally deleted secrets |
| Enable purge protection | Prevent permanent deletion for 90 days |
| Rotate secrets regularly | Limits damage from leaked secrets |
| Use separate vaults per environment | Dev and prod secrets never mix |
| Audit access logs | Know who accessed what and when |

---

## Practice Exercise

1. Create an Azure Key Vault in your resource group
2. Add your database URL and secret key as vault secrets
3. Enable Managed Identity on your Container App
4. Grant the identity read access to Key Vault
5. Modify your FastAPI app to read from Key Vault
6. Verify secrets are loaded correctly

---

*Next Topic: Monitoring & Observability — Azure Monitor, logs, and uptime alerts.*
