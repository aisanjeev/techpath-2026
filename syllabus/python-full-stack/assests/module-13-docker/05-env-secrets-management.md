# Environment Variables & Secrets Management

**Module 13 — Docker & Containerization | Topic 5**

---

## Why Environment Variables Matter

When Sneha builds a FastAPI app, she needs to store configuration like:
- Database connection strings
- API keys (Razorpay, SendGrid, Azure)
- Secret keys for JWT tokens
- Debug mode on/off

**Rule #1: Never hardcode secrets in your code.**

```python
# BAD — secret in code, will end up on GitHub
DATABASE_URL = "postgresql://admin:SuperSecret@db.example.com/prod"

# GOOD — read from environment
import os
DATABASE_URL = os.getenv("DATABASE_URL")
```

> **Analogy:** Hardcoding secrets is like writing your ATM PIN on the card itself. Environment variables are like memorizing the PIN — the card (code) travels safely without exposing the secret.

---

## Environment Variables in Docker

There are several ways to pass environment variables to Docker containers, from simple to production-grade.

### Method 1: Command-Line Flags (-e)

```bash
# Single variable
docker run -e DATABASE_URL=sqlite:///app.db my-app

# Multiple variables
docker run \
  -e DATABASE_URL=postgresql://user:pass@db:5432/mydb \
  -e SECRET_KEY=my-secret-key \
  -e DEBUG=false \
  my-app
```

**Pros:** Quick for testing
**Cons:** Secrets visible in `docker inspect` and shell history

### Method 2: Environment File (--env-file)

Create a `.env` file:

```bash
# .env
DATABASE_URL=postgresql://techpath:secret123@db:5432/techpath_db
SECRET_KEY=jwt-signing-key-here
REDIS_URL=redis://redis:6379/0
DEBUG=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

Run with:

```bash
docker run --env-file .env my-app
```

**Pros:** Cleaner than multiple `-e` flags, easy to manage
**Cons:** File must not be committed to Git

### Method 3: Docker Compose Environment

```yaml
# docker-compose.yml
services:
  api:
    build: .
    environment:
      - DATABASE_URL=postgresql://techpath:secret@db:5432/app_db
      - SECRET_KEY=my-secret
      - DEBUG=true

    # OR use env_file
    env_file:
      - .env
      - .env.local    # overrides .env
```

### Method 4: Dockerfile ENV (Build-Time Defaults)

```dockerfile
# These become defaults — can be overridden at runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_PORT=8000
```

**Use `ENV` for:** Non-sensitive defaults (Python settings, port numbers)
**Never use `ENV` for:** Passwords, API keys, secrets

---

## Managing Multiple Environments

Real projects have at least three environments:

| Environment | Purpose | Example Values |
|-------------|---------|----------------|
| Development | Rahul's laptop | SQLite, debug=true, fake API keys |
| Staging | Testing server | PostgreSQL, debug=false, test API keys |
| Production | Live server | PostgreSQL, debug=false, real API keys |

### File Structure

```
project/
├── .env                    # Shared defaults (committed to Git)
├── .env.local              # Local overrides (NOT committed)
├── .env.staging            # Staging config
├── .env.production         # Production config (on server only)
├── docker-compose.yml      # Base compose file
├── docker-compose.dev.yml  # Dev overrides
└── docker-compose.prod.yml # Prod overrides
```

### .env (Shared Defaults — Safe to Commit)

```bash
# .env — shared defaults, no real secrets
APP_NAME=TechPath API
APP_PORT=8000
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000,http://localhost:4321
```

### .env.local (Local Overrides — Never Commit)

```bash
# .env.local — Rahul's local secrets
DATABASE_URL=sqlite+aiosqlite:///./data/dev.db
SECRET_KEY=dev-only-secret-key
FIREBASE_PROJECT_ID=techpath-dev
DEBUG=true
```

### .gitignore

```
# ALWAYS ignore these
.env.local
.env.staging
.env.production
*.pem
*.key
```

---

## Docker Secrets (Swarm Mode)

For production deployments with Docker Swarm, Docker has a built-in secrets manager.

```bash
# Create a secret
echo "SuperSecretPassword" | docker secret create db_password -

# Use in docker-compose (Swarm mode)
```

```yaml
# docker-compose.yml (Swarm)
services:
  api:
    image: my-app
    secrets:
      - db_password
      - jwt_secret

secrets:
  db_password:
    external: true
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

Inside the container, secrets are available as files at `/run/secrets/`:

```python
# Reading a Docker secret in Python
def read_secret(name: str) -> str:
    """Read a Docker secret from the filesystem."""
    secret_path = f"/run/secrets/{name}"
    try:
        with open(secret_path) as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fall back to environment variable
        return os.getenv(name.upper(), "")

DB_PASSWORD = read_secret("db_password")
```

**Advantages of Docker Secrets:**
- Encrypted at rest and in transit
- Only available to services that need them
- Never stored in images or environment variables
- Mounted as in-memory files (not written to disk inside container)

---

## Build-Time vs Runtime Variables

| Type | Set When | Use For | Instruction |
|------|----------|---------|-------------|
| Build-time (ARG) | During `docker build` | Version numbers, build config | `ARG` |
| Runtime (ENV) | During `docker run` | App config, secrets | `ENV` / `-e` |

```dockerfile
# Build-time argument
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# Runtime environment variable
ENV APP_PORT=8000
```

```bash
# Override build-time argument
docker build --build-arg PYTHON_VERSION=3.11 -t my-app .
```

**Important:** `ARG` values are NOT available at runtime. They only exist during the build process.

---

## Best Practices for Secrets

### The Do's

| Practice | Example |
|----------|---------|
| Use `.env` files for local development | `docker run --env-file .env app` |
| Add `.env.local` to `.gitignore` | Prevents accidental commits |
| Use a secrets manager in production | Azure Key Vault, AWS Secrets Manager |
| Rotate secrets regularly | Change passwords every 90 days |
| Use different secrets per environment | Dev, staging, prod each have unique keys |

### The Don'ts

| Anti-Pattern | Why It's Dangerous |
|-------------|-------------------|
| Hardcoding secrets in code | Exposed on GitHub forever |
| Committing `.env` with real secrets | Anyone with repo access sees them |
| Using `ENV` for secrets in Dockerfile | Baked into the image layer |
| Logging secrets | Visible in container logs |
| Passing secrets as build args | Visible in `docker history` |

### Checking for Accidentally Committed Secrets

```bash
# Search your Git history for potential secrets
git log -p | grep -i "password\|secret\|api_key\|token" | head -20

# Use a tool like trufflehog
pip install trufflehog
trufflehog git file://./
```

---

## Python Pattern: Config with Pydantic Settings

The cleanest way to handle configuration in a Python app:

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """App configuration — reads from environment variables."""

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/app.db"

    # Auth
    secret_key: str = "change-me-in-production"
    jwt_expire_minutes: int = 60

    # App
    app_name: str = "TechPath API"
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
```

```python
# Usage anywhere in the app
from app.core.config import settings

print(settings.database_url)
print(settings.debug)
```

Pydantic Settings automatically reads from:
1. Environment variables (highest priority)
2. `.env` file
3. Default values (lowest priority)

---

## Practical Example: Configuring a Full Stack App

```yaml
# docker-compose.yml

services:
  api:
    build: .
    ports:
      - "${APP_PORT:-8000}:8000"
    env_file:
      - .env
      - .env.local
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: ${DB_USER:-techpath}
      POSTGRES_PASSWORD: ${DB_PASSWORD}     # MUST be set in .env.local
      POSTGRES_DB: ${DB_NAME:-techpath_db}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD:-redis123}

volumes:
  postgres_data:
```

The `${VAR:-default}` syntax provides a default value if the variable is not set.

---

## Practice Exercise

1. Create a `.env` file with database and secret key variables
2. Create a `.env.local` with override values
3. Add `.env.local` to `.gitignore`
4. Modify your `docker-compose.yml` to use `env_file`
5. Run `docker compose exec api env` to verify variables are set correctly
6. Try the Pydantic Settings pattern in your FastAPI app

---

*Next Topic: Optimizing Docker Images — multi-stage builds, .dockerignore, and slim images.*
