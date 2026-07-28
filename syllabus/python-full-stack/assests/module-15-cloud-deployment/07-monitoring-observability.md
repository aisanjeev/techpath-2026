# Monitoring & Observability

**Module 15 — Cloud Deployment | Topic 7**

---

## Why Monitoring Matters

Amit deploys his FastAPI app on a Friday evening. Everything looks fine. On Monday, he discovers the app has been crashing every 2 hours since Saturday — but nobody noticed because there were no alerts.

**Monitoring prevents this** by watching your app 24/7 and alerting you when something goes wrong.

> **Analogy:** Running an app without monitoring is like driving a car without a dashboard — you have no idea about speed, fuel level, or engine temperature until something breaks down.

---

## The Three Pillars of Observability

| Pillar | What It Is | Example |
|--------|-----------|---------|
| **Logs** | Text records of events | "2024-07-15 10:30:45 ERROR: Database connection failed" |
| **Metrics** | Numerical measurements over time | CPU: 45%, Response time: 120ms, Errors: 3/min |
| **Traces** | Request journey through services | User request → API → DB → Cache → Response (250ms total) |

### Logs — What Happened

Logs tell you what happened and when. They are the first place you look when debugging.

```python
# Python logging in FastAPI
import logging

logger = logging.getLogger(__name__)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    logger.info(f"Fetching user {user_id}")
    try:
        user = await crud.get_user(user_id)
        logger.info(f"User {user_id} found: {user.email}")
        return user
    except Exception as e:
        logger.error(f"Failed to fetch user {user_id}: {e}")
        raise
```

### Metrics — How Is It Performing

Metrics are numbers that tell you about your app's health:

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Response time (p95) | < 200ms | 200-500ms | > 500ms |
| Error rate | < 1% | 1-5% | > 5% |
| CPU usage | < 50% | 50-80% | > 80% |
| Memory usage | < 60% | 60-85% | > 85% |
| Uptime | 99.9% | 99-99.9% | < 99% |

### Traces — Where Did Time Go

For complex requests that touch multiple services, traces show the breakdown:

```
GET /api/v1/courses/42 — 350ms total
├── Authentication (Firebase verify) — 50ms
├── Database query (get course) — 80ms
├── Database query (get modules) — 120ms
├── Serialize response — 10ms
└── Network overhead — 90ms
```

---

## Azure Monitor

Azure Monitor is the built-in monitoring service for all Azure resources.

### What It Monitors

| Resource | Metrics Available |
|----------|------------------|
| Container Apps | CPU, memory, requests, errors, response time |
| App Service | CPU, memory, HTTP status codes, response time |
| PostgreSQL | Connections, storage, query performance |
| Key Vault | API calls, latency, failures |

### Viewing Metrics

```bash
# View Container App logs
az containerapp logs show \
  --name techpath-api \
  --resource-group techpath-rg \
  --follow

# View recent logs
az containerapp logs show \
  --name techpath-api \
  --resource-group techpath-rg \
  --tail 100
```

Or in the Azure Portal:
1. Go to your Container App
2. Click **Monitoring** → **Metrics**
3. Select metric: Requests, Response Time, CPU Usage, etc.
4. Choose time range and granularity

---

## Setting Up Alerts

Alerts notify you when something goes wrong — before your users notice.

### Common Alert Rules

| Alert | Condition | Action |
|-------|-----------|--------|
| High error rate | > 5% of requests return 5xx | Send email |
| Slow response | p95 response time > 2 seconds | Send email |
| High CPU | CPU > 80% for 5 minutes | Scale up + email |
| App down | No successful health checks for 3 minutes | Urgent notification |
| Database full | Storage > 80% | Email + Slack |

### Creating an Alert Rule

```bash
# Create an alert for high error rate
az monitor metrics alert create \
  --name "high-error-rate" \
  --resource-group techpath-rg \
  --scopes "/subscriptions/.../techpath-api" \
  --condition "avg Requests > 100 and avg FailedRequests > 5" \
  --description "Error rate exceeds 5%" \
  --severity 2 \
  --action-group "/subscriptions/.../my-action-group"
```

### Action Groups

Action groups define who gets notified and how:

```bash
# Create an action group
az monitor action-group create \
  --name techpath-alerts \
  --resource-group techpath-rg \
  --short-name tp-alert \
  --action email admin-email techpath.biz@gmail.com
```

---

## Application-Level Logging

### Structured Logging in FastAPI

Use structured logging (JSON) instead of plain text — it is easier to search and filter.

```python
# app/core/logging_config.py
import logging
import json
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Configure logging
def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
```

**Output:**
```json
{"timestamp": "2024-07-15T10:30:45Z", "level": "ERROR", "message": "Database connection failed", "module": "database", "function": "connect", "line": 42}
```

### Request Logging Middleware

```python
# app/middleware/logging.py
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration_ms = (time.time() - start_time) * 1000

        logger.info(
            f"{request.method} {request.url.path} "
            f"status={response.status_code} "
            f"duration={duration_ms:.1f}ms "
            f"client={request.client.host}"
        )

        return response
```

---

## Health Check Endpoint

Every production app should have a health check endpoint that monitoring tools can ping.

```python
# app/api/v1/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check — returns 200 if app and DB are healthy."""
    checks = {
        "app": "healthy",
        "database": "healthy",
    }

    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        return JSONResponse(status_code=503, content=checks)

    return checks
```

### Uptime Monitoring Services

External services that ping your health endpoint from around the world:

| Service | Free Tier |
|---------|-----------|
| UptimeRobot | 50 monitors, 5-min intervals |
| Better Stack | 10 monitors, 3-min intervals |
| Freshping | 50 monitors, 1-min intervals |
| Pingdom | 1 monitor |

### Setting Up UptimeRobot

1. Go to uptimerobot.com
2. Create a free account
3. Add a monitor:
   - Type: HTTP(s)
   - URL: `https://api.techpath.biz/health`
   - Interval: 5 minutes
4. Add alert contacts (email, Slack, etc.)

---

## Uptime and SLA

**SLA (Service Level Agreement)** defines how much downtime is acceptable.

| Uptime % | Downtime per Month | Downtime per Year |
|----------|-------------------|-------------------|
| 99% | 7.3 hours | 3.65 days |
| 99.9% | 43 minutes | 8.77 hours |
| 99.95% | 22 minutes | 4.38 hours |
| 99.99% | 4.3 minutes | 52.6 minutes |

For student and small projects, 99.9% uptime is a reasonable target.

---

## Log Levels

Use the right log level for each situation:

| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Detailed debugging info | "Query parameters: {'limit': 10}" |
| **INFO** | Normal operations | "User rahul@gmail.com logged in" |
| **WARNING** | Something unexpected but handled | "Rate limit approaching: 90/100" |
| **ERROR** | Something failed | "Database connection refused" |
| **CRITICAL** | App is about to crash | "Out of memory, shutting down" |

```python
logger.debug("Processing request with params: %s", params)
logger.info("Order %s created successfully", order_id)
logger.warning("Cache miss for key: %s", cache_key)
logger.error("Payment failed for order %s: %s", order_id, error)
logger.critical("Database unreachable, entering degraded mode")
```

---

## Practice Exercise

1. Add a `/health` endpoint to your FastAPI app
2. Set up structured JSON logging
3. Add request logging middleware
4. Sign up for UptimeRobot and monitor your deployed app
5. Create an Azure Monitor alert for error rate > 5%
6. Intentionally break something and verify you get alerted

---

*Next Topic: Environment Strategy — local, staging, production, and zero-downtime deployments.*
