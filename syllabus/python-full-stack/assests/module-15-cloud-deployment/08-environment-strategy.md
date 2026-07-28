# Environment Strategy — Local to Production

**Module 15 — Cloud Deployment | Topic 8**

---

## Why Multiple Environments?

Sneha wants to test a new payment feature. If she tests directly on the production server and something goes wrong, real customers lose their money. That is unacceptable.

**Multiple environments** solve this by providing separate stages for development, testing, and production. Each environment is a complete copy of the app with different data and settings.

> **Analogy:** Think of a Bollywood movie production. The director doesn't film the final take on day one. There are rehearsals (local), screen tests (staging), and only then the final shoot (production). Each stage catches different problems.

---

## The Three-Environment Strategy

| Environment | Purpose | Who Uses It | Data |
|-------------|---------|-------------|------|
| **Local** | Development on your laptop | Individual developer | Fake/test data |
| **Staging** | Testing before production | Team, QA | Copy of real data structure |
| **Production** | Live app for real users | Everyone | Real user data |

```
Local (your laptop)
    ↓ git push to develop
Staging (staging.api.techpath.biz)
    ↓ git push to main (after approval)
Production (api.techpath.biz)
```

---

## Local Environment

### What It Looks Like

```
Your Laptop:
├── FastAPI running on localhost:8000
├── SQLite database (local file)
├── Redis via Docker (localhost:6379)
├── .env.local with test credentials
└── Hot reload enabled (--reload flag)
```

### Configuration

```bash
# .env.local (local development)
DATABASE_URL=sqlite+aiosqlite:///./data/dev.db
SECRET_KEY=dev-only-not-a-real-secret
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:4321
STORAGE_TYPE=local
LOG_LEVEL=debug
```

### Running Locally

```bash
# Option 1: Direct
uvicorn app.main:app --reload --port 8000

# Option 2: Docker Compose (recommended)
docker compose -f docker-compose.dev.yml up
```

---

## Staging Environment

Staging is a mirror of production. It runs the exact same code and configuration, but with test data.

### What It Looks Like

```
Staging Server (staging.api.techpath.biz):
├── Docker container with latest develop branch
├── PostgreSQL database (test data)
├── Same infrastructure as production
├── Protected (not public)
└── Auto-deploys from develop branch
```

### Configuration

```bash
# Staging environment variables
DATABASE_URL=postgresql+asyncpg://staging_user:pass@staging-db:5432/staging_db
SECRET_KEY=staging-secret-key
DEBUG=false
CORS_ORIGINS=https://staging.techpath.biz
STORAGE_TYPE=azure
LOG_LEVEL=info
ENVIRONMENT=staging
```

### Key Rules for Staging

| Rule | Why |
|------|-----|
| Same Docker image as production | Catches environment-specific bugs |
| Same database type (PostgreSQL) | SQLite behaves differently than PostgreSQL |
| Different credentials | Staging secrets should never access production data |
| Automated deployment | Push to `develop` → auto-deploy to staging |
| Test data only | Never use real customer data on staging |

---

## Production Environment

Production is the live app that real users interact with.

### What It Looks Like

```
Production Server (api.techpath.biz):
├── Docker container with main branch
├── PostgreSQL database (real data)
├── Azure Key Vault for secrets
├── SSL/HTTPS enforced
├── Monitoring & alerts active
├── Daily backups
└── Requires approval to deploy
```

### Configuration

```bash
# Production environment variables
DATABASE_URL=<from Azure Key Vault>
SECRET_KEY=<from Azure Key Vault>
DEBUG=false
CORS_ORIGINS=https://techpath.biz,https://www.techpath.biz
STORAGE_TYPE=azure
LOG_LEVEL=warning
ENVIRONMENT=production
```

### Production Checklist

| Check | Status |
|-------|--------|
| Debug mode OFF | Required |
| HTTPS enforced | Required |
| Secrets in Key Vault (not env vars) | Recommended |
| Database backups configured | Required |
| Monitoring and alerts active | Required |
| Error tracking (Sentry) configured | Recommended |
| Rate limiting enabled | Recommended |
| CORS properly configured | Required |
| Health check endpoint working | Required |

---

## Branch Strategy

Map Git branches to environments:

```
feature/* branches → Local development
        ↓ (PR to develop)
develop branch → Staging environment
        ↓ (PR to main, with approval)
main branch → Production environment
```

### GitHub Actions Configuration

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: echo "Deploying to staging..."
      # Deploy to staging server

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production      # Requires manual approval
    steps:
      - run: echo "Deploying to production..."
      # Deploy to production server
```

---

## Zero-Downtime Deployment

When you deploy a new version, users should never see an error or downtime. There are several strategies.

### Strategy 1: Rolling Update

Replace containers one at a time. At any moment, some containers run the old version and some run the new version.

```
Before:  [v1] [v1] [v1]
Step 1:  [v2] [v1] [v1]    ← Replace first container
Step 2:  [v2] [v2] [v1]    ← Replace second
Step 3:  [v2] [v2] [v2]    ← All updated
```

**Docker Compose rolling update:**

```yaml
# docker-compose.prod.yml
services:
  api:
    image: ghcr.io/user/app:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1         # Update one at a time
        delay: 10s             # Wait 10s between updates
        order: start-first     # Start new before stopping old
```

### Strategy 2: Blue-Green Deployment

Run two identical environments. Switch traffic from the old (blue) to the new (green).

```
Before:
  Blue  (v1) ← Traffic goes here
  Green (v2) ← Deployed, tested, ready

Switch:
  Blue  (v1) ← Standby (rollback target)
  Green (v2) ← Traffic goes here now

If problems:
  Blue  (v1) ← Switch back instantly
  Green (v2) ← Investigate the issue
```

**Implementation with Nginx:**

```nginx
# nginx.conf
upstream api {
    # Switch between blue and green by commenting/uncommenting
    server blue-api:8000;    # Blue (current)
    # server green-api:8000; # Green (next version)
}
```

### Strategy 3: Docker Compose with Health Checks

The simplest zero-downtime approach for single-server deployments:

```yaml
# docker-compose.prod.yml
services:
  api:
    image: ghcr.io/user/app:latest
    deploy:
      update_config:
        order: start-first     # Start new container first
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s        # Wait 30s before first check

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      api:
        condition: service_healthy
```

**How it works:**
1. Docker starts the new container alongside the old one
2. Waits for the health check to pass
3. Routes traffic to the new container
4. Stops the old container
5. Zero downtime for users

---

## Environment Parity

The closer your environments are to each other, the fewer surprises in production.

| Factor | Local | Staging | Production |
|--------|-------|---------|------------|
| OS | Docker (Linux) | Docker (Linux) | Docker (Linux) |
| Python version | 3.12 | 3.12 | 3.12 |
| Database | SQLite (ok) or PostgreSQL | PostgreSQL | PostgreSQL |
| Cache | Redis (Docker) | Redis | Redis |
| Docker image | Same Dockerfile | Same image | Same image |
| Secrets | .env.local | Environment vars | Key Vault |

### Common Parity Breaks

| Issue | What Happens |
|-------|-------------|
| SQLite locally, PostgreSQL in production | Features work locally but break in production |
| Different Python versions | Syntax errors or behavior differences |
| Missing env vars in production | App crashes on startup |
| Different Docker base images | Library incompatibilities |

---

## Database Migrations Across Environments

```bash
# Local: Migrate your dev database
alembic upgrade head

# Staging: Run migrations after deploying
ssh staging-server "cd /opt/app && docker compose exec api alembic upgrade head"

# Production: Run migrations with caution
# 1. Backup the database first
# 2. Run migration
# 3. Verify data integrity
ssh prod-server "cd /opt/app && docker compose exec api alembic upgrade heads"
```

### Migration Best Practices

| Practice | Why |
|----------|-----|
| Always test migrations on staging first | Catches issues before they hit production |
| Make migrations reversible (downgrade) | Can undo if something breaks |
| Never drop columns in the same deploy | Old code might still reference them |
| Add columns as nullable first | Existing rows won't break |
| Run data backfill as a separate step | Don't mix schema and data changes |

---

## Summary: The Complete Deployment Flow

```
1. Developer creates feature branch
2. Writes code + tests locally
3. Opens PR → CI runs (lint, test, coverage)
4. Code review + approval
5. Merge to develop → Auto-deploy to staging
6. QA tests on staging
7. Merge to main → Build Docker → Push to GHCR
8. Manual approval gate
9. Deploy to production (zero-downtime)
10. Health check + monitoring verification
11. If problems → Rollback to previous version
```

---

## Practice Exercise

1. Set up separate `.env` files for local, staging, and production
2. Create a Docker Compose file for local development
3. Configure GitHub Actions to deploy develop → staging and main → production
4. Implement a health check endpoint
5. Test zero-downtime deployment using `order: start-first`
6. Practice a rollback by reverting a commit

---

*Congratulations! You now understand the complete deployment lifecycle — from writing code on your laptop to running it in production with monitoring and zero-downtime updates.*
