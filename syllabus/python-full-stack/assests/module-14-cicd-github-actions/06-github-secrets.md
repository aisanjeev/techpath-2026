# GitHub Secrets — Storing Credentials Securely

**Module 14 — CI/CD with GitHub Actions | Topic 6**

---

## Why Secrets Matter

Your CI/CD pipeline often needs sensitive information:
- Database passwords for running tests
- API keys for deployment (Azure, AWS, Render)
- Docker Hub credentials for pushing images
- SSH keys for server access
- Notification tokens (Slack, Discord)

**You must NEVER put these directly in your workflow file.** Workflow files are committed to Git — anyone with repo access can see them.

```yaml
# NEVER DO THIS!
- name: Deploy
  run: ssh user@server deploy
  env:
    SSH_KEY: "-----BEGIN RSA PRIVATE KEY-----MIIEowIBAAK..."  # EXPOSED!
```

**GitHub Secrets** encrypt your sensitive values. They are stored securely and injected into workflows at runtime — they never appear in logs.

---

## Types of Secrets

| Type | Scope | Where to Set |
|------|-------|-------------|
| **Repository secrets** | One repository only | Repo → Settings → Secrets |
| **Environment secrets** | Specific environment (staging, prod) | Repo → Settings → Environments |
| **Organization secrets** | All repos in your org | Org → Settings → Secrets |

For most student projects, **repository secrets** are what you need.

---

## Creating a Secret

### Step-by-Step

1. Go to your GitHub repository
2. Click **Settings** (tab at the top)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Enter the name and value:

| Field | Example |
|-------|---------|
| Name | `DEPLOY_SSH_KEY` |
| Value | (paste the actual key) |

6. Click **Add secret**

### Naming Conventions

Use `SCREAMING_SNAKE_CASE`:

| Secret | Purpose |
|--------|---------|
| `DOCKERHUB_USERNAME` | Docker Hub login |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `DEPLOY_SSH_KEY` | SSH private key for server |
| `DEPLOY_HOST` | Server IP or hostname |
| `DEPLOY_USER` | SSH username |
| `AZURE_CREDENTIALS` | Azure service principal JSON |
| `SLACK_WEBHOOK_URL` | Slack notification URL |
| `DATABASE_URL_PROD` | Production database URL |

---

## Using Secrets in Workflows

Access secrets using `${{ secrets.SECRET_NAME }}`:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Deploy via SSH
        run: |
          echo "${{ secrets.DEPLOY_SSH_KEY }}" > deploy_key
          chmod 600 deploy_key
          ssh -i deploy_key -o StrictHostKeyChecking=no \
            ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} \
            "cd /app && docker compose pull && docker compose up -d"
          rm deploy_key
```

### Important Security Rules

1. **Secrets are masked in logs.** If a secret value appears in the output, GitHub replaces it with `***`.

2. **Secrets are NOT available in forks.** If someone forks your repo and opens a PR, the workflow runs but without your secrets. This prevents strangers from stealing your credentials.

3. **Secrets are NOT available in pull_request from forks.** Only pushes from your own repo have access.

4. **Secrets cannot be read after creation.** You can update or delete them, but cannot view the stored value.

---

## The Built-in GITHUB_TOKEN

Every workflow automatically gets a `GITHUB_TOKEN` — no setup needed. It can:

| Permission | What It Can Do |
|------------|---------------|
| `contents: read` | Clone your repo |
| `packages: write` | Push to GHCR |
| `issues: write` | Comment on issues |
| `pull-requests: write` | Comment on PRs |
| `statuses: write` | Set commit status checks |

```yaml
# No secret setup needed — this just works!
- name: Login to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}    # Automatic!
```

---

## Environment Secrets

For more control, use **environments**. Each environment can have:
- Its own secrets
- Required approvals before deployment
- Deployment branch restrictions

### Setting Up Environments

1. Repo → Settings → Environments
2. Click **New environment**
3. Name it (e.g., `production`, `staging`)
4. Add protection rules:
   - **Required reviewers**: Team lead must approve
   - **Wait timer**: Wait 5 minutes before deploying
   - **Deployment branches**: Only `main` can deploy to production

### Using Environments in Workflows

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging          # Uses staging secrets
    steps:
      - run: echo "Deploying to ${{ vars.SERVER_URL }}"
        env:
          API_KEY: ${{ secrets.API_KEY }}    # Staging API key

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment: production       # Uses production secrets + requires approval
    steps:
      - run: echo "Deploying to production"
        env:
          API_KEY: ${{ secrets.API_KEY }}    # Production API key (different!)
```

When the production job runs, GitHub pauses and shows a "Review deployments" button. A designated reviewer must approve before the job continues.

---

## Environment Variables vs Secrets

| Feature | Variables (vars) | Secrets |
|---------|-----------------|---------|
| Encrypted? | No | Yes |
| Visible in settings? | Yes (can read) | No (write-only) |
| Masked in logs? | No | Yes |
| Use for | Non-sensitive config | Passwords, keys, tokens |
| Access in workflow | `${{ vars.NAME }}` | `${{ secrets.NAME }}` |

```yaml
# Variables for non-sensitive config
env:
  APP_NAME: ${{ vars.APP_NAME }}         # "TechPath API"
  SERVER_URL: ${{ vars.SERVER_URL }}     # "api.techpath.biz"

# Secrets for sensitive data
  API_KEY: ${{ secrets.API_KEY }}         # Masked in logs
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }} # Masked in logs
```

---

## Common Secrets for Python Projects

### Docker Hub

```
DOCKERHUB_USERNAME = rahul2024
DOCKERHUB_TOKEN    = dckr_pat_xxxxxxxxxxxx
```

### SSH Deployment

```
DEPLOY_HOST    = 192.168.1.100
DEPLOY_USER    = deploy
DEPLOY_SSH_KEY = -----BEGIN OPENSSH PRIVATE KEY-----
                 b3BlbnNzaC1r...
                 -----END OPENSSH PRIVATE KEY-----
```

### Azure

```
AZURE_CREDENTIALS = {"clientId": "...", "clientSecret": "...", ...}
```

### Notification

```
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/T00/B00/xxxxx
```

---

## SSH Key Setup for Deployment

A common pattern is deploying via SSH. Here is how to set it up securely.

### Step 1: Generate a Deploy Key

```bash
# On your local machine
ssh-keygen -t ed25519 -C "github-actions-deploy" -f deploy_key
# Creates: deploy_key (private) and deploy_key.pub (public)
```

### Step 2: Add Public Key to Server

```bash
# Copy the public key to your server
ssh-copy-id -i deploy_key.pub user@your-server-ip
```

### Step 3: Add Private Key as GitHub Secret

1. Copy the entire content of `deploy_key` (the private key)
2. Add it as a secret named `DEPLOY_SSH_KEY` in GitHub

### Step 4: Use in Workflow

```yaml
- name: Deploy to server
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/deploy_key
    chmod 600 ~/.ssh/deploy_key
    ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no \
      ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} \
      "cd /opt/app && docker compose pull && docker compose up -d"
```

---

## Security Best Practices

| Practice | Why |
|----------|-----|
| Use repository secrets, not hardcoded values | Secrets are encrypted and access-controlled |
| Rotate secrets regularly | Limits damage if a secret is leaked |
| Use environment protection rules for production | Requires human approval before deploying |
| Limit GITHUB_TOKEN permissions | Only grant what the workflow needs |
| Use fine-grained PATs instead of classic tokens | Scoped to specific repos and permissions |
| Never echo or print secret values | Even with masking, avoid unnecessary exposure |
| Audit secret access in the Settings page | See when secrets were last updated |

---

## Practice Exercise

1. Create a GitHub repository secret named `TEST_SECRET` with value `hello123`
2. Create a workflow that uses the secret: `echo "Secret length: ${#SECRET}"` (prints length, not value)
3. Set up an environment called `staging` with a secret
4. Create a `production` environment with a required reviewer
5. Generate an SSH deploy key and add it as a secret

---

*Next Topic: Deployment Triggers — deploying on successful builds and rollback strategies.*
