# Deployment Checklist and Post-Launch Monitoring

**Module 16 -- Spec-Kit Development Methodology | Topic 8**

---

## Why Deployment Needs a Checklist

Deploying software to production is like launching a rocket. There are hundreds of things that need to go right, and forgetting even one can cause failure. Astronauts do not rely on memory -- they use checklists. Software teams should do the same.

Sneha, a developer in Bangalore, once deployed a FastAPI app to production without checking environment variables. The app started fine but crashed the moment a user tried to log in because `FIREBASE_PROJECT_ID` was not set. The error logs showed "Firebase initialization failed," but by then, 200 users had seen a 500 error page. A simple checklist would have caught this in 30 seconds.

---

## Pre-Deployment Checklist

Before deploying, go through this checklist item by item.

### 1. Code Quality

| Check | Status | Notes |
|-------|--------|-------|
| All tests pass locally | [ ] | Run `pytest` / `npm test` |
| Linting passes | [ ] | Run `ruff check` / `npm run lint` |
| Type checking passes | [ ] | Run `mypy` / TypeScript compiler |
| No TODO or FIXME in new code | [ ] | Search for leftover markers |
| Code reviewed and approved | [ ] | PR has at least one approval |
| No merge conflicts | [ ] | Branch is up to date with main |

### 2. Environment Variables

| Check | Status | Notes |
|-------|--------|-------|
| All required env vars are set on server | [ ] | Compare with `.env.example` |
| No secrets in code or Git history | [ ] | Check for hardcoded keys |
| Environment-specific values are correct | [ ] | Production URLs, not staging |
| API keys have proper permissions | [ ] | Not overly permissive |

**How to verify on the server:**

```bash
# List all environment variables (check for missing ones)
printenv | grep -E "DATABASE_URL|SECRET_KEY|FIREBASE"

# Or check the .env file
cat /app/.env | grep -v "^#" | sort
```

### 3. Database Migrations

| Check | Status | Notes |
|-------|--------|-------|
| Migration files committed to Git | [ ] | `alembic/versions/` has new files |
| Migrations tested on staging DB | [ ] | Run `alembic upgrade head` on staging first |
| Rollback tested | [ ] | Run `alembic downgrade -1` to verify |
| Seed data updated if needed | [ ] | New lookup tables, default records |
| Backup taken before migration | [ ] | `mysqldump` or `pg_dump` |

**Migration commands:**

```bash
# Take a backup first
mysqldump -u root -p techpath_db > backup_2026-07-25.sql

# Apply migrations
poetry run alembic upgrade heads

# If something goes wrong, roll back
poetry run alembic downgrade -1

# Restore from backup if needed
mysql -u root -p techpath_db < backup_2026-07-25.sql
```

### 4. Build and Dependencies

| Check | Status | Notes |
|-------|--------|-------|
| Build succeeds without warnings | [ ] | Run `npm run build` or equivalent |
| Dependencies are locked | [ ] | `poetry.lock` / `package-lock.json` committed |
| No vulnerable dependencies | [ ] | Run `npm audit` / `pip-audit` |
| Static assets are built | [ ] | Frontend CSS/JS bundles generated |

---

## Health Checks

A health check endpoint lets monitoring tools verify your application is running and can connect to its dependencies.

### Implementing a Health Check (FastAPI)

```python
from fastapi import APIRouter
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check -- is the server running?"""
    return {"status": "healthy", "version": "1.0.0"}

@router.get("/health/ready")
async def readiness_check(db=Depends(get_db)):
    """Readiness check -- can we reach the database?"""
    checks = {}

    # Check database connectivity
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "connected"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"

    all_healthy = all(v != "error" for v in checks.values())

    return {
        "status": "ready" if all_healthy else "degraded",
        "checks": checks,
    }
```

### Health Check Types

| Type | What It Checks | Used By |
|------|---------------|---------|
| Liveness (`/health`) | Is the process running? | Load balancer, container orchestrator |
| Readiness (`/health/ready`) | Can it serve requests? (DB, cache connected) | Load balancer (to route traffic) |
| Startup (`/health/startup`) | Has the app finished initializing? | Container orchestrator (to know when to start sending traffic) |

---

## Monitoring Tools

Once your app is deployed, you need to monitor it continuously. Here are essential tools:

### Uptime Monitoring

| Tool | What It Does | Cost |
|------|-------------|------|
| UptimeRobot | Pings your health endpoint every 5 minutes | Free (50 monitors) |
| Better Uptime | Uptime monitoring with incident pages | Free tier available |
| Pingdom | Enterprise-grade uptime monitoring | Paid |

**Setup example (UptimeRobot):**
1. Create a free account at uptimerobot.com
2. Add a new HTTP monitor
3. Set URL to `https://api.yourapp.in/health`
4. Set check interval to 5 minutes
5. Add alert contacts (email, SMS, Slack)

### Error Tracking

| Tool | What It Does | Cost |
|------|-------------|------|
| Sentry | Catches and groups runtime errors | Free (5K events/month) |
| LogRocket | Records user sessions with errors | Free tier |
| Rollbar | Error tracking with deployment tracking | Free tier |

**Setup example (Sentry with FastAPI):**

```python
# Install: pip install sentry-sdk[fastapi]
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    environment=os.environ.get("ENV", "production"),
    traces_sample_rate=0.1,  # 10% of requests for performance monitoring
)
```

Once configured, Sentry automatically captures:
- Unhandled exceptions with full stack traces
- Request details (URL, headers, body)
- User context (if configured)
- Release version and deployment info

---

## Logging

Good logs are your best friend when debugging production issues.

### Logging Levels

| Level | When to Use | Example |
|-------|------------|---------|
| DEBUG | Detailed info for developers | "Querying users table with filter: city=Bhopal" |
| INFO | Normal operations | "User rahul@email.com logged in" |
| WARNING | Something unexpected but not broken | "API rate limit at 80% capacity" |
| ERROR | Something failed but the app continues | "Failed to send SMS to 9876543210" |
| CRITICAL | The app is about to crash | "Database connection pool exhausted" |

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

# GOOD -- structured, useful information
logger.info("Order created", extra={
    "order_id": order.id,
    "user_id": user.id,
    "total": order.total_amount,
    "items_count": len(order.items),
})

# BAD -- vague, no context
logger.info("Order created")

# BAD -- logging sensitive data
logger.info(f"User logged in with password: {password}")  # NEVER do this!
```

### What to Log

| Log This | Do NOT Log This |
|----------|----------------|
| Request method and path | Full request bodies with user data |
| Response status codes | Passwords or tokens |
| Error messages and stack traces | Credit card or Aadhaar numbers |
| Performance metrics (response time) | Personal data (full PAN number) |
| Authentication events (login, logout) | Session tokens or API keys |

---

## Rollback Strategy

Sometimes a deployment introduces a bug. You need a plan to undo the change quickly.

### Rollback Steps

```
1. Detect the problem
   --> Monitoring alert, error spike in Sentry, user reports

2. Assess severity
   --> Is the app down? Is data corrupted? Are users affected?

3. Decide: fix forward or roll back?
   --> Simple fix (typo, config): fix forward
   --> Complex bug or data issue: roll back

4. Roll back
   --> Redeploy the previous version
   --> Roll back database migration if needed
   --> Clear cache if relevant

5. Verify
   --> Check health endpoint
   --> Check error rates in Sentry
   --> Verify key user flows manually

6. Communicate
   --> Notify the team
   --> Update status page if you have one
```

### Rollback Commands

```bash
# Option 1: Redeploy the previous Git commit
git log --oneline -5        # Find the last good commit
git checkout abc1234         # Switch to that commit
# Trigger deployment pipeline

# Option 2: If using Docker
docker pull myapp:previous-tag
docker stop myapp-current
docker run -d --name myapp myapp:previous-tag

# Option 3: Database rollback
poetry run alembic downgrade -1
```

---

## Incident Response

When something goes wrong in production, follow a structured process.

### Severity Levels

| Level | Description | Example | Response Time |
|-------|------------|---------|---------------|
| SEV-1 | Complete outage, all users affected | App returns 500 for everyone | Immediate (within 15 min) |
| SEV-2 | Major feature broken, many users affected | Payment processing failing | Within 1 hour |
| SEV-3 | Minor feature broken, some users affected | Search not returning results for one category | Within 4 hours |
| SEV-4 | Cosmetic issue, no functionality impact | Button color wrong on one page | Next business day |

### Incident Response Steps

```
1. Acknowledge    --> "I see the alert, I am investigating"
2. Assess         --> What is broken? How many users affected?
3. Communicate    --> Update team and stakeholders
4. Mitigate       --> Stop the bleeding (rollback, disable feature)
5. Resolve        --> Fix the root cause
6. Verify         --> Confirm the fix works
7. Post-mortem    --> Document what happened and why
```

---

## Post-Mortem Template

After every significant incident, write a post-mortem. This is not about blame -- it is about learning and preventing the same issue from happening again.

```markdown
# Post-Mortem: [Incident Title]

**Date:** [When it happened]
**Duration:** [How long it lasted]
**Severity:** [SEV-1 / SEV-2 / SEV-3]
**Author:** [Your name]

## Summary
[1-2 sentence description of what happened]

## Impact
- [Number of users affected]
- [Revenue impact, if any]
- [Duration of the outage]

## Timeline (IST)
| Time | Event |
|------|-------|
| 14:00 | Deployment of version 2.3.1 completed |
| 14:05 | Error rate spike detected by Sentry |
| 14:08 | UptimeRobot alert: /health returning 503 |
| 14:12 | Engineer Arjun acknowledges the alert |
| 14:15 | Root cause identified: missing env variable |
| 14:18 | Environment variable set, app restarted |
| 14:20 | Health check passing, error rate normalized |

## Root Cause
[Detailed explanation of what went wrong]

## What Went Well
- [Alert fired within 3 minutes of the issue]
- [Rollback completed in under 10 minutes]

## What Went Wrong
- [Environment variable was not in the deployment checklist]
- [No staging environment to catch this before production]

## Action Items
| Action | Owner | Deadline |
|--------|-------|----------|
| Add env var check to deployment script | Arjun | 2026-07-28 |
| Set up staging environment | Rahul | 2026-08-05 |
| Add env var validation at app startup | Priya | 2026-07-30 |
```

---

## Example: Deploying a FastAPI App

Here is a condensed deployment flow for a FastAPI application on a VPS:

```bash
# 1. SSH into the server
ssh deploy@api.myapp.in

# 2. Pull the latest code
cd /app/backend
git pull origin main

# 3. Install dependencies
poetry install --no-dev

# 4. Run migrations
poetry run alembic upgrade heads

# 5. Restart the application
sudo systemctl restart myapp

# 6. Verify health
curl http://localhost:8000/health
# Expected: {"status": "healthy", "version": "2.3.1"}

# 7. Check logs for errors
sudo journalctl -u myapp --since "5 minutes ago" | grep ERROR
```

---

## Key Takeaways

1. Use a deployment checklist every single time -- never rely on memory.
2. Verify environment variables, database migrations, and build artifacts before deploying.
3. Implement health check endpoints (`/health` and `/health/ready`) for automated monitoring.
4. Use UptimeRobot (free) for uptime and Sentry (free tier) for error tracking.
5. Log structured data at appropriate levels; never log passwords or sensitive data.
6. Have a rollback plan ready: know how to revert to the previous version within minutes.
7. Write post-mortems after incidents to learn and prevent recurrence -- blame the process, not the person.

---

*TechPath Institute -- Spec-Kit Development Methodology*
