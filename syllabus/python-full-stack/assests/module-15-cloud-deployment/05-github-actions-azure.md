# Deploy Docker to Azure via GitHub Actions

**Module 15 — Cloud Deployment | Topic 5**

---

## The Full Pipeline

In previous modules, you learned to:
1. Write a Dockerfile (Module 13)
2. Build and push Docker images in CI (Module 14)
3. Create Azure resources (this module)

Now we connect everything — pushing code automatically deploys to Azure.

```
Push to main → CI tests → Build Docker → Push to GHCR → Deploy to Azure Container Apps
```

---

## Prerequisites

Before setting up the pipeline, you need:

1. A GitHub repository with a Dockerfile
2. Azure CLI installed and logged in
3. Azure Container Apps environment created
4. An Azure service principal for authentication

### Creating a Service Principal

A **service principal** is like a robot account that GitHub Actions uses to talk to Azure.

```bash
# Create a service principal with contributor access
az ad sp create-for-rbac \
  --name "github-actions-deploy" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/techpath-rg \
  --json-auth

# Output (save this JSON!):
# {
#   "clientId": "xxxx-xxxx-xxxx",
#   "clientSecret": "xxxx-xxxx-xxxx",
#   "subscriptionId": "xxxx-xxxx-xxxx",
#   "tenantId": "xxxx-xxxx-xxxx",
#   ...
# }
```

### Adding Secrets to GitHub

Add these as GitHub Repository Secrets:

| Secret Name | Value |
|-------------|-------|
| `AZURE_CREDENTIALS` | The entire JSON output from above |
| `AZURE_CONTAINER_APP_NAME` | `techpath-api` |
| `AZURE_RESOURCE_GROUP` | `techpath-rg` |

---

## Complete CI/CD Workflow

```yaml
# .github/workflows/deploy-azure.yml

name: Build & Deploy to Azure

on:
  push:
    branches: [main]

env:
  IMAGE_NAME: ghcr.io/${{ github.repository }}/api

jobs:
  # ============================
  # Job 1: Run Tests
  # ============================
  test:
    name: Lint & Test
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: sqlite+aiosqlite:///./test.db
      SECRET_KEY: ci-test-secret

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint
        run: ruff check app/

      - name: Test
        run: pytest --cov=app --cov-fail-under=70

  # ============================
  # Job 2: Build & Push Docker
  # ============================
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write

    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ============================
  # Job 3: Deploy to Azure
  # ============================
  deploy:
    name: Deploy to Azure Container Apps
    runs-on: ubuntu-latest
    needs: build
    environment: production

    steps:
      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy to Container Apps
        uses: azure/container-apps-deploy-action@v2
        with:
          containerAppName: ${{ secrets.AZURE_CONTAINER_APP_NAME }}
          resourceGroup: ${{ secrets.AZURE_RESOURCE_GROUP }}
          imageToDeploy: ${{ env.IMAGE_NAME }}:${{ github.sha }}

      - name: Health check
        run: |
          APP_URL=$(az containerapp show \
            --name ${{ secrets.AZURE_CONTAINER_APP_NAME }} \
            --resource-group ${{ secrets.AZURE_RESOURCE_GROUP }} \
            --query properties.configuration.ingress.fqdn -o tsv)
          echo "App URL: https://$APP_URL"
          sleep 30
          curl -f "https://$APP_URL/health" || echo "Health check warning"
```

---

## Alternative: Deploy to Azure App Service

If you are using App Service instead of Container Apps:

```yaml
  deploy:
    name: Deploy to App Service
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy to Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: techpath-api
          images: ${{ env.IMAGE_NAME }}:${{ github.sha }}
```

---

## Multi-Environment Deployment

Deploy to staging first, then production after approval.

```yaml
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    environment: staging
    steps:
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - uses: azure/container-apps-deploy-action@v2
        with:
          containerAppName: techpath-api-staging
          resourceGroup: techpath-rg
          imageToDeploy: ${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment: production           # Requires manual approval
    steps:
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - uses: azure/container-apps-deploy-action@v2
        with:
          containerAppName: techpath-api
          resourceGroup: techpath-rg
          imageToDeploy: ${{ env.IMAGE_NAME }}:${{ github.sha }}
```

**Flow:**

```
Tests pass → Build Docker → Deploy to Staging → [Manual approval] → Deploy to Production
```

---

## Alternative: Deploy via SSH to VPS

If you are deploying to your own VPS (not Azure), the deploy job looks like this:

```yaml
  deploy:
    name: Deploy to VPS
    runs-on: ubuntu-latest
    needs: build
    environment: production

    steps:
      - name: Deploy via SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519

          ssh -o StrictHostKeyChecking=no ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} << 'DEPLOY'
            # Login to GHCR on the server
            echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

            # Pull the new image
            cd /opt/techpath-api
            docker compose pull

            # Restart with new image
            docker compose up -d --remove-orphans

            # Clean up old images
            docker image prune -f

            echo "Deployment complete!"
          DEPLOY

      - name: Health check
        run: |
          sleep 15
          curl -f https://api.techpath.biz/health || exit 1
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Azure login fails | Regenerate service principal credentials |
| Image pull fails | Check GHCR permissions and image tag |
| Container won't start | Check logs: `az containerapp logs show --name app --resource-group rg` |
| Health check fails | Verify the /health endpoint exists and the port is correct |
| Deployment succeeds but app crashes | Check env vars are set correctly on Azure |

---

## Practice Exercise

1. Create an Azure service principal and add credentials to GitHub Secrets
2. Create the CI/CD workflow with test, build, and deploy jobs
3. Push to main and watch the pipeline run
4. Add a staging environment with a separate Container App
5. Set up manual approval for production deployments

---

*Next Topic: Azure Key Vault — managing production secrets securely.*
