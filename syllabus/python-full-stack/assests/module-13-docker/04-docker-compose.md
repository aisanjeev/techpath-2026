# Docker Compose — Multi-Service Applications

**Module 13 — Docker & Containerization | Topic 4**

---

## Why Docker Compose?

A real-world application is rarely just one container. A typical Python full-stack app might need:

- **Web server** — FastAPI or Django
- **Database** — PostgreSQL or MySQL
- **Cache** — Redis
- **Background worker** — Celery

Running each with separate `docker run` commands gets messy fast:

```bash
# Without Compose — painful
docker network create app-net
docker run -d --name db --network app-net -e POSTGRES_PASSWORD=secret postgres:16
docker run -d --name redis --network app-net redis:7
docker run -d --name api --network app-net -p 8000:8000 -e DATABASE_URL=... my-api
docker run -d --name worker --network app-net -e DATABASE_URL=... my-worker
```

**Docker Compose** lets you define all these services in a single YAML file and start everything with one command.

> **Analogy:** Imagine organizing a college fest. Instead of calling each volunteer individually, you create a WhatsApp group, post one message, and everyone knows their role. Docker Compose is that WhatsApp group for your containers.

---

## The docker-compose.yml File

Create a file named `docker-compose.yml` (or `compose.yml` in newer versions) in your project root.

### Basic Structure

```yaml
# docker-compose.yml

services:
  service-name:
    image: or build:
    ports:
    environment:
    volumes:
    depends_on:
    networks:

volumes:
  named-volumes:

networks:
  custom-networks:
```

---

## Example 1: FastAPI + PostgreSQL

The simplest real-world setup — an API server with a database.

```yaml
# docker-compose.yml

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://techpath:secret123@db:5432/techpath_db
      - SECRET_KEY=my-super-secret-key
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=techpath
      - POSTGRES_PASSWORD=secret123
      - POSTGRES_DB=techpath_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

**What each section does:**

| Section | Purpose |
|---------|---------|
| `build: .` | Build image from Dockerfile in current directory |
| `image: postgres:16` | Use an existing image from Docker Hub |
| `ports: - "8000:8000"` | Map host port to container port |
| `environment:` | Set environment variables |
| `depends_on:` | Start `db` before `api` |
| `volumes:` | Persist database data |
| `restart: unless-stopped` | Auto-restart if container crashes |

### How Services Find Each Other

Notice the `DATABASE_URL` uses `db` as the hostname:

```
postgresql+asyncpg://techpath:secret123@db:5432/techpath_db
                                        ^^
                                   Service name = hostname
```

Docker Compose automatically creates a network. Services can reach each other using their service name as hostname.

---

## Example 2: Full Stack — Web + DB + Redis + Worker

A production-like setup for an e-commerce API built by Amit.

```yaml
# docker-compose.yml

services:
  # FastAPI application
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://techpath:secret123@db:5432/shop_db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=amit-secret-key-2024
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - uploads:/app/uploads
    restart: unless-stopped

  # Celery background worker
  worker:
    build: .
    command: celery -A app.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql+asyncpg://techpath:secret123@db:5432/shop_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # PostgreSQL database
  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=techpath
      - POSTGRES_PASSWORD=secret123
      - POSTGRES_DB=shop_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U techpath -d shop_db"]
      interval: 5s
      timeout: 5s
      retries: 5
    ports:
      - "5432:5432"

  # Redis cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
  uploads:
```

### Health Checks

Notice the `healthcheck` on the database:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U techpath -d shop_db"]
  interval: 5s      # Check every 5 seconds
  timeout: 5s       # Wait max 5 seconds for response
  retries: 5        # Try 5 times before marking unhealthy
```

With `condition: service_healthy`, the API waits until PostgreSQL is actually ready to accept connections — not just until the container starts.

---

## Docker Compose Commands

### Starting Services

```bash
# Start all services (foreground — see all logs)
docker compose up

# Start in background
docker compose up -d

# Start and rebuild images
docker compose up -d --build

# Start only specific services
docker compose up -d api db
```

### Stopping Services

```bash
# Stop all services (keep containers)
docker compose stop

# Stop and remove containers, networks
docker compose down

# Stop and remove everything including volumes (WARNING: deletes data!)
docker compose down -v

# Stop a specific service
docker compose stop api
```

### Viewing Status and Logs

```bash
# List running services
docker compose ps

# View logs for all services
docker compose logs

# Follow logs for a specific service
docker compose logs -f api

# View last 50 lines of logs
docker compose logs --tail 50 api
```

### Running Commands in Services

```bash
# Run a command in the API service
docker compose exec api python -c "print('hello')"

# Open a shell in the API container
docker compose exec api bash

# Run database migrations
docker compose exec api alembic upgrade head

# Run one-off commands (creates a new container)
docker compose run --rm api python manage.py createsuperuser
```

### Rebuilding

```bash
# Rebuild images
docker compose build

# Rebuild a specific service
docker compose build api

# Rebuild without cache
docker compose build --no-cache
```

---

## Docker Compose for Development

For local development, you often want to:
- Mount your code as a volume (live reload)
- Expose database ports for debugging
- Use development settings

### Development Compose File

```yaml
# docker-compose.dev.yml

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://techpath:secret123@db:5432/dev_db
      - DEBUG=true
    volumes:
      - ./app:/app/app          # Live code reload!
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=techpath
      - POSTGRES_PASSWORD=secret123
      - POSTGRES_DB=dev_db
    ports:
      - "5432:5432"            # Expose for local DB tools
    volumes:
      - dev_postgres_data:/var/lib/postgresql/data

volumes:
  dev_postgres_data:
```

**Run with:**

```bash
docker compose -f docker-compose.dev.yml up
```

The key difference is the **bind mount** (`./app:/app/app`). When you edit code on your laptop, the changes appear instantly inside the container. Combined with `--reload`, uvicorn restarts automatically.

---

## Environment Variables with .env Files

Instead of hardcoding values in `docker-compose.yml`, use a `.env` file:

```bash
# .env
POSTGRES_USER=techpath
POSTGRES_PASSWORD=secret123
POSTGRES_DB=techpath_db
SECRET_KEY=my-production-secret
```

```yaml
# docker-compose.yml
services:
  api:
    build: .
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - SECRET_KEY=${SECRET_KEY}

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
```

Docker Compose automatically reads the `.env` file in the same directory.

---

## Common Patterns

### Wait for Database to Be Ready

```yaml
depends_on:
  db:
    condition: service_healthy
```

### Shared Environment Variables

Use YAML anchors to avoid repeating yourself:

```yaml
x-common-env: &common-env
  DATABASE_URL: postgresql+asyncpg://techpath:secret@db:5432/app_db
  REDIS_URL: redis://redis:6379/0

services:
  api:
    environment:
      <<: *common-env
      PORT: "8000"
  worker:
    environment:
      <<: *common-env
      WORKER_CONCURRENCY: "4"
```

### Multiple Compose Files

```bash
# Use base + override
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start all services | `docker compose up -d` |
| Stop all services | `docker compose down` |
| Rebuild and start | `docker compose up -d --build` |
| View logs | `docker compose logs -f` |
| Run a command | `docker compose exec api bash` |
| List services | `docker compose ps` |
| Stop one service | `docker compose stop api` |
| Remove everything | `docker compose down -v` |

---

## Practice Exercise

1. Create a `docker-compose.yml` with FastAPI + PostgreSQL
2. Run `docker compose up -d` and check `docker compose ps`
3. View logs: `docker compose logs -f api`
4. Open a shell in the API container: `docker compose exec api bash`
5. Stop everything: `docker compose down`
6. Add Redis as a third service and restart

---

*Next Topic: Environment Variables and Secrets Management in Docker.*
