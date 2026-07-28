# Azure Core Concepts

**Module 15 — Cloud Deployment | Topic 4**

---

## Why Azure?

Microsoft Azure is one of the "Big Three" cloud providers (alongside AWS and Google Cloud). For Indian developers, Azure is particularly relevant because:

- **Microsoft partnership with Indian companies** — Reliance Jio, Infosys, Wipro, TCS all use Azure heavily
- **India data centers** — Azure has regions in Mumbai (Central India), Pune (West India), and Chennai (South India)
- **Free tier** — 12 months of free services + $200 credit for new accounts
- **Integration** — Works seamlessly with GitHub (Microsoft owns GitHub)
- **Job market** — Azure skills are in high demand in India's IT sector

> **Analogy:** If free-tier platforms (Render, Railway) are like food stalls, Azure is like a fully equipped commercial kitchen. More setup, more features, more control — but also more to learn.

---

## Azure Services for Full-Stack Apps

| Service | What It Does | Monthly Cost (Free Tier) |
|---------|-------------|-------------------------|
| **App Service** | Host web apps (Python, Node) | 1 free instance (F1) |
| **Container Apps** | Run Docker containers | 180,000 vCPU sec/month free |
| **Azure Database for PostgreSQL** | Managed PostgreSQL | Free for 12 months (Flexible) |
| **Azure Blob Storage** | File storage (images, uploads) | 5 GB free |
| **Azure Key Vault** | Secrets management | 10,000 operations free |
| **Azure Monitor** | Logs, metrics, alerts | 5 GB log data free |
| **Azure Container Registry** | Docker image storage | Basic tier ~₹400/month |

---

## Azure App Service

App Service is the easiest way to deploy a web app on Azure. It supports Python directly — no Docker required.

### How It Works

1. Upload your code (via Git push, GitHub Actions, or zip deploy)
2. Azure installs dependencies and runs your app
3. You get a URL: `https://your-app.azurewebsites.net`

### Creating an App Service

Using Azure CLI:

```bash
# Install Azure CLI
# Windows: winget install Microsoft.AzureCLI
# Mac: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Create a resource group (like a folder for Azure resources)
az group create --name techpath-rg --location centralindia

# Create an App Service plan (F1 = free)
az appservice plan create \
  --name techpath-plan \
  --resource-group techpath-rg \
  --sku F1 \
  --is-linux

# Create the web app
az webapp create \
  --name techpath-api \
  --resource-group techpath-rg \
  --plan techpath-plan \
  --runtime "PYTHON|3.12"
```

### App Service Configuration

```bash
# Set environment variables
az webapp config appsettings set \
  --name techpath-api \
  --resource-group techpath-rg \
  --settings \
    DATABASE_URL="postgresql+asyncpg://..." \
    SECRET_KEY="production-secret" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# Set the startup command
az webapp config set \
  --name techpath-api \
  --resource-group techpath-rg \
  --startup-file "uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

### App Service Tiers

| Tier | CPU | RAM | Cost | Best For |
|------|-----|-----|------|----------|
| **F1 (Free)** | Shared | 1 GB | Free | Learning, testing |
| **B1 (Basic)** | 1 core | 1.75 GB | ~₹1000/month | Small apps |
| **S1 (Standard)** | 1 core | 1.75 GB | ~₹5000/month | Production |
| **P1v3 (Premium)** | 2 cores | 8 GB | ~₹8000/month | High traffic |

---

## Azure Container Apps

Container Apps is Azure's serverless container platform. You give it a Docker image, and it runs it without managing servers.

### Why Container Apps over App Service?

| Feature | App Service | Container Apps |
|---------|------------|----------------|
| Docker support | Yes (single container) | Yes (multiple containers) |
| Scaling | Manual or basic auto-scale | Advanced auto-scale (KEDA) |
| Pricing | Always running | Scale to zero (pay per use) |
| Microservices | Not designed for | Built for microservices |
| Dapr integration | No | Yes |

### Creating a Container App

```bash
# Install the Container Apps extension
az extension add --name containerapp

# Create an environment
az containerapp env create \
  --name techpath-env \
  --resource-group techpath-rg \
  --location centralindia

# Create the container app
az containerapp create \
  --name techpath-api \
  --resource-group techpath-rg \
  --environment techpath-env \
  --image ghcr.io/your-user/techpath-api:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 3 \
  --env-vars \
    DATABASE_URL="postgresql+asyncpg://..." \
    SECRET_KEY="production-secret"
```

### Scaling Rules

```bash
# Scale based on HTTP traffic
az containerapp update \
  --name techpath-api \
  --resource-group techpath-rg \
  --min-replicas 1 \
  --max-replicas 5 \
  --scale-rule-name http-rule \
  --scale-rule-type http \
  --scale-rule-http-concurrency 50
```

This means:
- Always keep at least 1 instance running
- Scale up to 5 when each instance handles 50+ concurrent requests
- Scale back down when traffic drops

---

## Azure Database for PostgreSQL

Managed PostgreSQL on Azure — Microsoft handles backups, updates, and high availability.

### Creating a Database

```bash
# Create a flexible server (free tier for 12 months)
az postgres flexible-server create \
  --name techpath-db \
  --resource-group techpath-rg \
  --location centralindia \
  --admin-user techpath_admin \
  --admin-password 'StrongPassword123!' \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 16

# Create a database
az postgres flexible-server db create \
  --server-name techpath-db \
  --resource-group techpath-rg \
  --database-name techpath_prod

# Allow Azure services to connect
az postgres flexible-server firewall-rule create \
  --name allow-azure \
  --server-name techpath-db \
  --resource-group techpath-rg \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### Connection String

```
postgresql+asyncpg://techpath_admin:StrongPassword123!@techpath-db.postgres.database.azure.com:5432/techpath_prod?sslmode=require
```

---

## Resource Groups — Organizing Resources

Everything in Azure belongs to a **Resource Group**. Think of it like a folder.

```
techpath-rg (Resource Group)
├── techpath-api (Container App)
├── techpath-db (PostgreSQL)
├── techpath-storage (Blob Storage)
├── techpath-kv (Key Vault)
└── techpath-env (Container App Environment)
```

### Why Resource Groups?

- **Organization**: Group related resources together
- **Access control**: Set permissions at the group level
- **Cost tracking**: See costs per resource group
- **Cleanup**: Delete the entire group to remove all resources at once

```bash
# Delete everything when you're done learning
az group delete --name techpath-rg --yes
```

---

## Azure CLI Cheat Sheet

| Command | What It Does |
|---------|-------------|
| `az login` | Login to Azure |
| `az account list` | List subscriptions |
| `az group create` | Create resource group |
| `az group list` | List resource groups |
| `az group delete` | Delete resource group (and all resources) |
| `az webapp create` | Create web app |
| `az containerapp create` | Create container app |
| `az postgres flexible-server create` | Create PostgreSQL |

---

## Practice Exercise

1. Create an Azure free account (azure.microsoft.com/free)
2. Install the Azure CLI
3. Create a resource group in Central India region
4. Create a free-tier App Service and deploy your FastAPI app
5. Create a PostgreSQL Flexible Server and connect your app
6. Clean up: `az group delete --name techpath-rg`

---

*Next Topic: Deploying Docker to Azure Container Apps via GitHub Actions.*
