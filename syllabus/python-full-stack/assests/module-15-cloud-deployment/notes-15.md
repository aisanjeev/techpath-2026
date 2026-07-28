# Cloud Deployment — Azure & Free-Tier Platforms

**Module 15 — Cloud Deployment | Topic 1**

> Think of deployment like opening your shop to the world. You have been coding on your laptop (your workshop), but now it is time to put your app on the internet so anyone can use it — just like Rahul's chai stall going from a home kitchen to a busy street corner in Bhopal.

---

## 1. Understanding Deployment

### What is Deployment?

Deployment means taking your application from your local computer and putting it on a server so that users can access it over the internet.

| Term | Meaning | Analogy |
|------|---------|---------|
| **Local** | Your laptop / PC | Cooking at home |
| **Server** | A computer that runs 24/7 on the internet | A restaurant kitchen |
| **Deployment** | Moving your code to the server | Opening your restaurant to customers |
| **Domain** | The URL users type (e.g., `techpath.biz`) | Your restaurant's address |
| **SSL** | The padlock icon (HTTPS) | A security guard at the door |

### Why Not Just Run on Your Laptop?

- Your laptop turns off at night — servers run 24/7
- Your home internet is slow for serving many users
- No fixed address (IP changes) — servers have permanent domains
- No SSL certificate — browsers show "Not Secure" warning

---

## 2. Free-Tier Platforms — Deploy in 10 Minutes

These platforms let you deploy for free (with limits). Perfect for learning, portfolios, and small projects.

### 2.1 Render — Best Free Option for Backend

Render is like a free parking spot for your app. You connect your GitHub repo, and Render builds and runs it automatically.

**What You Get Free:**
- 750 hours/month of web service runtime
- Free PostgreSQL database (90 days)
- Auto-deploy on every `git push`
- Free SSL certificate
- Custom domain support

**Deploying a FastAPI App to Render:**

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Fill in the settings:

```
Name:           techpath-api
Runtime:        Python 3
Build Command:  pip install -r requirements.txt
Start Command:  uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

6. Click "Create Web Service" — done!

**Your app is now live at:** `https://techpath-api.onrender.com`

**Project Structure Render Expects:**

```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   └── main.py
├── requirements.txt       # All dependencies
├── render.yaml            # Optional: deployment config
└── Dockerfile             # Optional: custom build
```

**Sample `requirements.txt`:**
```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
alembic==1.13.0
```

> **Tip from Priya:** "My first deploy failed because I forgot to add `uvicorn` to requirements.txt. Always check your dependencies!"

### 2.2 Railway — Simple and Fast

Railway is another free platform with a generous free tier.

**What You Get Free:**
- $5 of free credits/month (enough for a small app)
- Built-in PostgreSQL, MySQL, Redis
- One-click deploy from GitHub
- Environment variable management

**Deploy Steps:**
1. Sign up at [railway.app](https://railway.app) with GitHub
2. Click "New Project" → "Deploy from GitHub Repo"
3. Select your repo
4. Railway auto-detects Python and sets build commands
5. Add environment variables in the dashboard
6. Your app is live!

**Adding a Database on Railway:**
1. In your project, click "New" → "Database" → "PostgreSQL"
2. Railway gives you a `DATABASE_URL` automatically
3. Add it to your app's environment variables
4. Your app connects to the cloud database!

### 2.3 Fly.io — Docker-Based Deployment

Fly.io runs your app in containers (Docker) close to your users worldwide.

**What You Get Free:**
- 3 shared VMs
- 3 GB persistent storage
- 160 GB bandwidth/month

**Deploy Steps:**
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch your app (from your project directory)
fly launch

# Deploy
fly deploy
```

Fly.io will ask you questions about your app and generate a `fly.toml` config file.

### Comparing Free Platforms

| Feature | Render | Railway | Fly.io |
|---------|--------|---------|--------|
| **Ease of Use** | Very Easy | Very Easy | Moderate |
| **Free Tier** | 750 hrs/month | $5 credit/month | 3 VMs |
| **Database** | PostgreSQL (90 days free) | PostgreSQL, MySQL, Redis | PostgreSQL (paid) |
| **Auto-Deploy** | Yes (GitHub) | Yes (GitHub) | Yes (CLI) |
| **Custom Domain** | Yes (free) | Yes (free) | Yes (free) |
| **Docker Support** | Yes | Yes | Yes (required) |
| **Best For** | Beginners | Quick prototypes | Global apps |
| **Cold Start** | Yes (free tier sleeps) | No | No |

> **What is "Cold Start"?** On Render's free tier, if no one visits your app for 15 minutes, it goes to sleep. The next visitor waits 30-50 seconds for it to wake up. This is fine for portfolios and learning — not for production apps.

---

## 3. Cloud Databases — Free PostgreSQL

Your app needs a database. These services give you a free cloud PostgreSQL database.

### 3.1 Supabase — Free PostgreSQL + More

Supabase gives you a full PostgreSQL database with a nice dashboard.

**What You Get Free:**
- 500 MB database storage
- 2 GB bandwidth
- 50,000 monthly active users
- REST API auto-generated from your tables

**Setup Steps:**
1. Sign up at [supabase.com](https://supabase.com)
2. Click "New Project"
3. Set a database password (save it!)
4. Go to Settings → Database → Connection String
5. Copy the `DATABASE_URL` — it looks like:

```
postgresql://postgres:[PASSWORD]@db.xxxx.supabase.co:5432/postgres
```

6. Add this URL to your app's environment variables

**Using with SQLAlchemy:**
```python
# In your config
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# For async: replace postgresql:// with postgresql+asyncpg://
ASYNC_DATABASE_URL = DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)
```

### 3.2 Neon — Serverless PostgreSQL

Neon is a "serverless" PostgreSQL — it scales to zero when not in use (saves money).

**What You Get Free:**
- 0.5 GB storage
- 190 compute hours/month
- Auto-suspend after 5 minutes of inactivity
- Branching (like Git branches for your database!)

**Setup Steps:**
1. Sign up at [neon.tech](https://neon.tech)
2. Create a project
3. Copy the connection string
4. Use it in your app

**Connection String Format:**
```
postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

### Choosing a Cloud Database

| Feature | Supabase | Neon |
|---------|----------|------|
| **Free Storage** | 500 MB | 0.5 GB |
| **Dashboard** | Excellent (table editor) | Good |
| **Auto-Sleep** | No (always running) | Yes (saves resources) |
| **REST API** | Built-in | No |
| **Branching** | No | Yes |
| **Best For** | Full-stack apps | Serverless apps |

---

## 4. Static Frontend Deployment — Vercel & Netlify

For your frontend (HTML/CSS/JS, React, Astro), these platforms are the best free option.

### 4.1 Vercel — Built for Frontend

Vercel is the company behind Next.js. It deploys frontend apps instantly.

**What You Get Free:**
- Unlimited static sites
- 100 GB bandwidth/month
- Serverless functions
- Auto-deploy from GitHub
- Free SSL + custom domains
- Preview deployments for every pull request

**Deploy Steps:**
1. Push your frontend code to GitHub
2. Go to [vercel.com](https://vercel.com) and sign up with GitHub
3. Click "Add New" → "Project"
4. Import your GitHub repo
5. Vercel auto-detects the framework (React, Astro, Next.js)
6. Click "Deploy" — done in 30 seconds!

**Custom Domain Setup:**
1. In Vercel dashboard → Project → Settings → Domains
2. Add your domain (e.g., `techpath.biz`)
3. Update your DNS records at your domain registrar:

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com

Type: A
Name: @
Value: 76.76.21.21
```

4. SSL certificate is auto-generated — your site is HTTPS immediately

### 4.2 Netlify — Alternative to Vercel

Netlify offers similar features to Vercel with some extras.

**What You Get Free:**
- 100 GB bandwidth/month
- 300 build minutes/month
- Forms handling (collect form submissions without a backend)
- Serverless functions
- Free SSL + custom domains

**Deploy Steps:**
1. Push code to GitHub
2. Sign up at [netlify.com](https://netlify.com) with GitHub
3. Click "Add new site" → "Import from Git"
4. Select your repo and branch
5. Set build command and publish directory:

```
Build Command:    npm run build
Publish Directory: dist      # or "build" for React
```

6. Click "Deploy site"

### Vercel vs Netlify

| Feature | Vercel | Netlify |
|---------|--------|---------|
| **Speed** | Excellent | Very Good |
| **Framework Support** | All (best for Next.js) | All (framework-agnostic) |
| **Forms** | No (need backend) | Yes (built-in) |
| **Serverless Functions** | Yes | Yes |
| **Preview Deploys** | Yes | Yes |
| **Build Minutes** | 6000/month | 300/month |
| **Best For** | Next.js / React apps | Static sites with forms |

---

## 5. Azure — Core Cloud Concepts

Microsoft Azure is one of the "Big 3" cloud providers (along with AWS and Google Cloud). Many Indian companies use Azure because of Microsoft's strong presence in India.

> **Analogy:** If free-tier platforms are like renting a room in a hostel (cheap, shared, limited), Azure is like renting an entire office building — more expensive, but you control everything.

### 5.1 Azure App Service — Managed Web Hosting

Azure App Service runs your web app without you managing servers.

**Key Features:**
- Supports Python, Node.js, Java, .NET, PHP
- Built-in auto-scaling (handles traffic spikes)
- Deployment slots (staging + production)
- Custom domains + SSL
- Integrated monitoring

**Pricing (India — Central India region):**

| Plan | Monthly Cost | Features |
|------|-------------|----------|
| **Free (F1)** | ₹0 | 1 GB RAM, 1 GB storage, shared CPU |
| **Basic (B1)** | ~₹1,100/month | 1.75 GB RAM, 10 GB storage, custom domain |
| **Standard (S1)** | ~₹5,500/month | Auto-scale, deployment slots, backups |

**Deploy a FastAPI App to Azure App Service:**

```bash
# Install Azure CLI
# Windows: Download from https://aka.ms/installazurecliwindows
# Or use: winget install Microsoft.AzureCLI

# Login to Azure
az login

# Create a resource group (think of it as a folder for your resources)
az group create --name techpath-rg --location centralindia

# Create an App Service plan
az appservice plan create \
  --name techpath-plan \
  --resource-group techpath-rg \
  --sku B1 \
  --is-linux

# Create the web app
az webapp create \
  --name techpath-api \
  --resource-group techpath-rg \
  --plan techpath-plan \
  --runtime "PYTHON:3.12"

# Deploy from GitHub
az webapp deployment source config \
  --name techpath-api \
  --resource-group techpath-rg \
  --repo-url https://github.com/yourname/techpath-api \
  --branch main
```

### 5.2 Azure Container Apps — Run Docker Containers

Container Apps is Azure's serverless container platform. You give it a Docker image, and it runs it.

**Why Use Containers?**
- Your app runs the same way everywhere (laptop, staging, production)
- No "works on my machine" problems
- Easy scaling — run 1 or 100 copies of your app

**Key Concepts:**

```
┌─────────────────────────────────────────────┐
│              Container App Environment       │
│                                              │
│  ┌──────────────┐   ┌──────────────────┐    │
│  │ Container     │   │ Container        │    │
│  │ App: API      │   │ App: Frontend    │    │
│  │ (FastAPI)     │   │ (Astro/React)    │    │
│  └──────────────┘   └──────────────────┘    │
│                                              │
│  Shared: networking, logging, scaling        │
└─────────────────────────────────────────────┘
```

**Dockerfile for a FastAPI App:**
```dockerfile
# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (Docker caches this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deploy to Azure Container Apps:**
```bash
# Create a Container Apps environment
az containerapp env create \
  --name techpath-env \
  --resource-group techpath-rg \
  --location centralindia

# Create a container registry (to store your Docker images)
az acr create \
  --name techpathregistry \
  --resource-group techpath-rg \
  --sku Basic

# Build and push your Docker image
az acr build \
  --registry techpathregistry \
  --image techpath-api:v1 .

# Deploy the container app
az containerapp create \
  --name techpath-api \
  --resource-group techpath-rg \
  --environment techpath-env \
  --image techpathregistry.azurecr.io/techpath-api:v1 \
  --target-port 8000 \
  --ingress external
```

### 5.3 Azure Database for PostgreSQL

A fully managed PostgreSQL database on Azure.

**Pricing (Central India):**

| Tier | Monthly Cost | Features |
|------|-------------|----------|
| **Burstable (B1ms)** | ~₹1,200/month | 1 vCore, 2 GB RAM |
| **General Purpose** | ~₹8,000/month | 2 vCores, 8 GB RAM |

**Create a Database:**
```bash
# Create a flexible PostgreSQL server
az postgres flexible-server create \
  --name techpath-db \
  --resource-group techpath-rg \
  --location centralindia \
  --admin-user techpath_admin \
  --admin-password "YourSecurePassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32

# Create the database
az postgres flexible-server db create \
  --resource-group techpath-rg \
  --server-name techpath-db \
  --database-name techpath_prod
```

**Connection String:**
```
postgresql://techpath_admin:YourSecurePassword123!@techpath-db.postgres.database.azure.com:5432/techpath_prod?sslmode=require
```

---

## 6. CI/CD with GitHub Actions

### What is CI/CD?

| Term | Full Form | Meaning |
|------|-----------|---------|
| **CI** | Continuous Integration | Automatically test code when you push |
| **CD** | Continuous Deployment | Automatically deploy code after tests pass |

> **Analogy:** Imagine Vikram writes code and pushes to GitHub. CI is like an automatic quality check — it runs tests to make sure nothing is broken. CD is like an automatic delivery service — if tests pass, the code goes live on the server automatically.

### How GitHub Actions Works

```
Developer pushes code to GitHub
         │
         ▼
GitHub Actions workflow triggers
         │
         ▼
   ┌─────────────────┐
   │  Step 1: Build   │  ← Install dependencies
   │  Step 2: Test    │  ← Run pytest / npm test
   │  Step 3: Deploy  │  ← Push to Render / Azure
   └─────────────────┘
         │
         ▼
  App is live with new changes!
```

### Workflow File Location

GitHub Actions looks for workflow files in `.github/workflows/`:
```
your-project/
├── .github/
│   └── workflows/
│       ├── test.yml        # Run tests on every push
│       └── deploy.yml      # Deploy to production
├── app/
├── requirements.txt
└── Dockerfile
```

### Simple Test Workflow

```yaml
# .github/workflows/test.yml
name: Run Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # Step 1: Get the code
      - uses: actions/checkout@v4

      # Step 2: Set up Python
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Step 3: Install dependencies
      - run: pip install -r requirements.txt

      # Step 4: Run tests
      - run: pytest tests/ -v
```

### Deploy to Azure Container Apps (GitHub Actions)

This is the full CI/CD pipeline: push code → build Docker image → deploy to Azure.

See the file `code-azure-container-deploy.yml` in this module for the complete workflow.

**GitHub Secrets You Need to Set:**

Go to your repo → Settings → Secrets and variables → Actions → New repository secret:

| Secret Name | Where to Get It |
|------------|----------------|
| `AZURE_CREDENTIALS` | `az ad sp create-for-rbac --name "github-deploy" --role contributor` |
| `REGISTRY_LOGIN_SERVER` | `techpathregistry.azurecr.io` |
| `REGISTRY_USERNAME` | From Azure Container Registry → Access keys |
| `REGISTRY_PASSWORD` | From Azure Container Registry → Access keys |
| `DATABASE_URL` | Your PostgreSQL connection string |
| `SECRET_KEY` | A random string for JWT signing |

---

## 7. Azure Key Vault — Secrets Management

### Why Key Vault?

Never put passwords, API keys, or database URLs directly in your code or environment variables on the server. Use Azure Key Vault — a secure safe for your secrets.

> **Analogy:** Imagine Neha keeps her house keys under the doormat. Anyone can find them! Key Vault is like a bank locker — only authorized people with proper ID can access the secrets.

### Common Secrets to Store

| Secret | Example | Why It Is Sensitive |
|--------|---------|-------------------|
| `DATABASE_URL` | `postgresql://user:pass@host/db` | Contains database password |
| `SECRET_KEY` | `a8f2e9b1c4d7...` | Used to sign JWT tokens |
| `FIREBASE_KEY` | `{"type": "service_account"...}` | Full access to Firebase |
| `SMTP_PASSWORD` | `xyzabc123` | Can send emails as you |
| `AZURE_STORAGE_KEY` | `Eby8v...` | Access to file storage |

### Setting Up Key Vault

```bash
# Create a Key Vault
az keyvault create \
  --name techpath-vault \
  --resource-group techpath-rg \
  --location centralindia

# Add a secret
az keyvault secret set \
  --vault-name techpath-vault \
  --name "DATABASE-URL" \
  --value "postgresql://user:pass@host/db"

# Read a secret
az keyvault secret show \
  --vault-name techpath-vault \
  --name "DATABASE-URL" \
  --query "value" -o tsv
```

### Using Key Vault in Python

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Connect to Key Vault
credential = DefaultAzureCredential()
vault_url = "https://techpath-vault.vault.azure.net"
client = SecretClient(vault_url=vault_url, credential=credential)

# Get a secret
db_url = client.get_secret("DATABASE-URL").value
secret_key = client.get_secret("SECRET-KEY").value

print(f"Connected to database: {db_url[:20]}...")
```

**Install the required packages:**
```bash
pip install azure-identity azure-keyvault-secrets
```

---

## 8. Monitoring & Observability

### Why Monitor?

Deploying is only half the job. You need to know:
- Is your app running? (uptime)
- Is it fast enough? (performance)
- Are there errors? (reliability)
- How many users are visiting? (traffic)

> **Analogy:** Ananya opens a restaurant. She does not just cook and leave — she checks if customers are happy, if the kitchen is clean, and if supplies are running low. Monitoring is the same for your app.

### 8.1 Azure Monitor

Azure Monitor collects logs, metrics, and alerts from your Azure resources.

**Key Features:**
- **Metrics**: CPU usage, memory, request count, response time
- **Logs**: Application logs, error logs, access logs
- **Alerts**: Get notified (email/SMS) when something goes wrong
- **Dashboards**: Visual overview of your app's health

**Setting Up Alerts:**
```bash
# Create an alert when CPU goes above 80%
az monitor metrics alert create \
  --name "high-cpu-alert" \
  --resource-group techpath-rg \
  --scopes "/subscriptions/.../techpath-api" \
  --condition "avg Percentage CPU > 80" \
  --description "CPU usage is too high!" \
  --action-group "/subscriptions/.../alertTeam"
```

### 8.2 Application Logging

Always add proper logging to your FastAPI app:

```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("techpath")

@app.get("/api/v1/courses")
async def get_courses():
    logger.info("Fetching all courses")
    try:
        courses = await crud.get_courses()
        logger.info(f"Found {len(courses)} courses")
        return {"success": True, "data": courses}
    except Exception as e:
        logger.error(f"Failed to fetch courses: {e}")
        raise
```

### 8.3 Health Check Endpoint

Every production app should have a health check — a simple endpoint that says "I am alive."

```python
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns 200 if the app is running.
    Monitoring tools hit this every 30 seconds.
    """
    return {
        "status": "healthy",
        "app": "TechPath API",
        "version": "1.0.0"
    }
```

### 8.4 Uptime Monitoring (Free Tools)

| Tool | Free Tier | Features |
|------|-----------|----------|
| [UptimeRobot](https://uptimerobot.com) | 50 monitors | HTTP checks every 5 min, email alerts |
| [Better Stack](https://betterstack.com) | 10 monitors | Status pages, incident management |
| [Freshping](https://freshping.io) | 50 monitors | Multi-location checks |

**How It Works:**
1. Sign up at UptimeRobot
2. Add your app URL: `https://techpath-api.onrender.com/health`
3. Set check interval: every 5 minutes
4. Add your email for alerts
5. If your app goes down, you get an email within 5 minutes

---

## 9. Environment Strategy

### The Three Environments

Every professional team uses at least three environments:

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   LOCAL      │ ──→ │   STAGING    │ ──→ │  PRODUCTION  │
│ (Your laptop)│     │ (Test server) │     │ (Live server) │
│              │     │              │     │              │
│ localhost    │     │ staging.     │     │ techpath.biz │
│ :8000       │     │ techpath.biz │     │              │
│              │     │              │     │              │
│ SQLite DB   │     │ PostgreSQL   │     │ PostgreSQL   │
│ Fake data   │     │ Test data    │     │ Real data    │
└─────────────┘     └──────────────┘     └──────────────┘
```

| Environment | Purpose | Who Uses It | Database |
|-------------|---------|------------|----------|
| **Local** | Development | Developers | SQLite (fast, no setup) |
| **Staging** | Testing before release | Team + QA | PostgreSQL (same as prod) |
| **Production** | Live app for real users | Everyone | PostgreSQL (backed up) |

### Environment Variables Per Environment

```bash
# .env.local (development)
DATABASE_URL=sqlite+aiosqlite:///./data/techpath.db
DEBUG=true
SECRET_KEY=local-dev-key-not-secure

# .env.staging
DATABASE_URL=postgresql+asyncpg://user:pass@staging-db:5432/techpath_staging
DEBUG=false
SECRET_KEY=staging-secret-key-abc123

# .env.production
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/techpath_prod
DEBUG=false
SECRET_KEY=production-super-secure-key-xyz789
```

> **Rule:** Never use production database credentials on your local machine. Never use `DEBUG=true` in production.

### Zero-Downtime Deployment

When you deploy a new version, you do not want users to see an error page. Zero-downtime deployment means the old version keeps running until the new version is ready.

**How It Works (Blue-Green Deployment):**

```
Step 1: Old version (Blue) is running and serving users
        ┌──────────┐
Users → │ Blue v1  │  ← Currently live
        └──────────┘

Step 2: New version (Green) is deployed alongside
        ┌──────────┐
Users → │ Blue v1  │  ← Still serving users
        └──────────┘
        ┌──────────┐
        │ Green v2 │  ← Starting up, running health checks
        └──────────┘

Step 3: Traffic switches to Green once it is healthy
        ┌──────────┐
        │ Blue v1  │  ← Stopped
        └──────────┘
        ┌──────────┐
Users → │ Green v2 │  ← Now serving users
        └──────────┘
```

Azure Container Apps and Render both support this automatically. When you deploy a new version, the old version keeps running until the new one passes its health check.

---

## 10. Putting It All Together — Deployment Checklist

Before deploying any app to production, go through this checklist:

### Pre-Deployment Checklist

| Step | Action | Why |
|------|--------|-----|
| 1 | Run all tests (`pytest`) | Catch bugs before users do |
| 2 | Check environment variables | Missing vars = app crash |
| 3 | Set `DEBUG=false` | Debug mode leaks sensitive info |
| 4 | Use HTTPS (SSL) | Protect user data |
| 5 | Set up health check endpoint | Monitoring needs it |
| 6 | Configure logging | Debug issues in production |
| 7 | Set up database backups | Protect against data loss |
| 8 | Set up monitoring/alerts | Know when things break |
| 9 | Test on staging first | Catch env-specific issues |
| 10 | Document your deployment | Help future-you (and your team) |

### Quick Deployment Decision Guide

```
Is it a portfolio / learning project?
├── YES → Use Render (free, easy)
│
├── Is it a frontend-only app?
│   ├── YES → Use Vercel or Netlify
│   └── NO ↓
│
├── Is it a startup / side project?
│   ├── YES → Use Railway or Render (paid tier)
│   └── NO ↓
│
├── Is it for a company / enterprise?
│   ├── YES → Use Azure / AWS
│   └── NO → Start with Render, upgrade later
```

---

## Key Takeaways

1. **Start free, upgrade later** — Use Render/Railway for learning, move to Azure for production
2. **Automate everything** — GitHub Actions deploys your code automatically
3. **Secure your secrets** — Never hardcode passwords; use Key Vault or environment variables
4. **Monitor your app** — Set up health checks, logging, and alerts from day one
5. **Use environments** — Local → Staging → Production keeps bugs away from users
6. **Docker is your friend** — Containers make deployment consistent across all platforms

> "Deploying your first app to the internet is like publishing your first book. It feels amazing when the world can finally see what you built." — TechPath Institute
