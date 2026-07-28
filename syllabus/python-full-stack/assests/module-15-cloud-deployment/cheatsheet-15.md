# Cloud Deployment — Cheatsheet

**Module 15 — Quick Reference Card**

---

## Free-Tier Platforms

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| **Render** | 750 hrs/month, sleeps at 15 min | Python APIs |
| **Railway** | $5 credit/month | Fast prototyping |
| **Fly.io** | 3 shared VMs | Docker-native apps |
| **Vercel** | Unlimited (serverless) | Frontends, Next.js |
| **Netlify** | 100 GB bandwidth | Static sites |

---

## Cloud Database Services

| Service | Type | Free Tier |
|---------|------|-----------|
| **Supabase** | PostgreSQL | 500 MB, 2 projects |
| **Neon** | Serverless PostgreSQL | 512 MB, auto-suspend |
| **Railway** | PostgreSQL | Within $5 credit |
| **PlanetScale** | MySQL | 5 GB |

### Connection Strings

```bash
# Supabase (use pooler port 6543)
DATABASE_URL=postgresql+asyncpg://postgres.[ref]:[pass]@pooler.supabase.com:6543/postgres

# Neon (requires SSL)
DATABASE_URL=postgresql+asyncpg://user:[pass]@host.neon.tech/db?sslmode=require
```

---

## Render Deployment

```bash
# Start command for FastAPI
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

```yaml
# render.yaml
services:
  - type: web
    name: my-api
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Fly.io Commands

```bash
fly auth login            # Login
fly launch                # Initialize app
fly deploy                # Deploy
fly logs                  # View logs
fly status                # Check status
fly scale count 2         # Scale to 2 instances
```

---

## Vercel Deployment

1. Import GitHub repo at vercel.com
2. Set framework, build command, output dir
3. Add environment variables
4. Deploy (auto-deploys on push)

---

## Azure CLI Quick Reference

```bash
az login                              # Login
az group create --name rg --location centralindia  # Resource group
az group delete --name rg --yes       # Delete everything

# App Service
az webapp create --name app --resource-group rg --plan plan --runtime "PYTHON|3.12"
az webapp config appsettings set --name app --resource-group rg --settings KEY=VAL

# Container Apps
az containerapp create --name app --resource-group rg --environment env \
  --image ghcr.io/user/app:latest --target-port 8000 --ingress external

# PostgreSQL
az postgres flexible-server create --name db --resource-group rg \
  --admin-user admin --admin-password 'Pass123!' --sku-name Standard_B1ms

# Key Vault
az keyvault create --name kv --resource-group rg --location centralindia
az keyvault secret set --vault-name kv --name "secret-name" --value "secret-value"
az keyvault secret show --vault-name kv --name "secret-name" --query value -o tsv
```

---

## Azure Container Apps Deployment (GitHub Actions)

```yaml
- uses: azure/login@v2
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}

- uses: azure/container-apps-deploy-action@v2
  with:
    containerAppName: my-app
    resourceGroup: my-rg
    imageToDeploy: ghcr.io/user/app:${{ github.sha }}
```

---

## Key Vault from Python

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

client = SecretClient(
    vault_url="https://my-kv.vault.azure.net/",
    credential=DefaultAzureCredential()
)
secret = client.get_secret("database-url").value
```

---

## Health Check Endpoint

```python
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"app": "healthy", "database": "healthy"}
    except Exception:
        return JSONResponse(status_code=503, content={"database": "unhealthy"})
```

---

## Environment Strategy

| Environment | Branch | Database | Deploys |
|-------------|--------|----------|---------|
| Local | feature/* | SQLite | Manual |
| Staging | develop | PostgreSQL | Auto on push |
| Production | main | PostgreSQL | Manual approval |

---

## Environment Variables Per Stage

```bash
# Local (.env.local)
DEBUG=true
DATABASE_URL=sqlite+aiosqlite:///./data/dev.db

# Staging
DEBUG=false
DATABASE_URL=postgresql+asyncpg://...staging...

# Production
DEBUG=false
DATABASE_URL=<from Key Vault>
```

---

## Zero-Downtime Deployment

```yaml
# docker-compose.prod.yml
services:
  api:
    image: ghcr.io/user/app:latest
    deploy:
      update_config:
        order: start-first     # Start new before stopping old
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      start_period: 30s
```

---

## Monitoring Checklist

| Item | Tool |
|------|------|
| Uptime monitoring | UptimeRobot (free) |
| Error tracking | Sentry |
| Logs | Azure Monitor / structured logging |
| Metrics | Azure Monitor |
| Alerts | Azure Alerts / UptimeRobot |
| Health check | Custom /health endpoint |

---

## Log Levels

| Level | Use For |
|-------|---------|
| DEBUG | Detailed debugging info |
| INFO | Normal operations |
| WARNING | Unexpected but handled |
| ERROR | Something failed |
| CRITICAL | App about to crash |

---

## SSL/HTTPS

| Provider | Method |
|----------|--------|
| Vercel | Automatic |
| Netlify | Automatic (Let's Encrypt) |
| Render | Automatic |
| VPS | Certbot + Let's Encrypt |
| Azure | Managed certificates |

---

## Uptime SLA Reference

| Uptime | Downtime/Month | Downtime/Year |
|--------|----------------|---------------|
| 99% | 7.3 hours | 3.65 days |
| 99.9% | 43 minutes | 8.77 hours |
| 99.99% | 4.3 minutes | 52.6 minutes |

---

## Rollback Options

```bash
# Option 1: Git revert (triggers CI/CD)
git revert HEAD && git push

# Option 2: Deploy previous Docker image
docker pull ghcr.io/user/app:<previous-sha>
docker compose up -d

# Option 3: Manual rollback workflow
gh workflow run rollback.yml -f commit-sha=abc1234
```
