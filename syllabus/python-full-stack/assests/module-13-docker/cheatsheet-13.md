# Docker Cheatsheet

**Module 13 — Quick Reference Card**

---

## Image Commands

| Command | What It Does |
|---------|-------------|
| `docker build -t name .` | Build image from Dockerfile |
| `docker build -t name:tag .` | Build with specific tag |
| `docker images` | List all local images |
| `docker rmi image` | Remove an image |
| `docker pull image:tag` | Download image from registry |
| `docker push user/image:tag` | Upload image to registry |
| `docker image prune -a` | Remove all unused images |
| `docker history image` | Show image layer history |

---

## Container Commands

| Command | What It Does |
|---------|-------------|
| `docker run -d -p 8000:8000 --name api image` | Run container in background |
| `docker run -it image bash` | Run interactive shell |
| `docker run --rm image` | Run and auto-remove when done |
| `docker run -e KEY=VAL image` | Run with env variable |
| `docker run --env-file .env image` | Run with env file |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker stop name` | Stop container gracefully |
| `docker start name` | Start stopped container |
| `docker restart name` | Restart container |
| `docker rm name` | Remove stopped container |
| `docker rm -f name` | Force remove running container |

---

## Logs & Debugging

| Command | What It Does |
|---------|-------------|
| `docker logs name` | View container logs |
| `docker logs -f name` | Follow logs in real-time |
| `docker logs --tail 50 name` | Last 50 log lines |
| `docker exec -it name bash` | Shell into running container |
| `docker exec name command` | Run command in container |
| `docker inspect name` | Full container details (JSON) |
| `docker stats` | Live CPU/memory usage |
| `docker port name` | Show port mappings |

---

## Volumes & Networks

| Command | What It Does |
|---------|-------------|
| `docker volume create data` | Create named volume |
| `docker volume ls` | List volumes |
| `docker volume rm data` | Remove volume |
| `-v data:/app/data` | Mount named volume |
| `-v $(pwd)/src:/app/src` | Bind mount (host dir) |
| `-v /path:/path:ro` | Read-only mount |
| `docker network create net` | Create network |
| `docker network ls` | List networks |

---

## Docker Compose

| Command | What It Does |
|---------|-------------|
| `docker compose up -d` | Start all services (background) |
| `docker compose up -d --build` | Rebuild and start |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Stop + remove volumes (data loss!) |
| `docker compose ps` | List running services |
| `docker compose logs -f api` | Follow logs for a service |
| `docker compose exec api bash` | Shell into a service |
| `docker compose stop api` | Stop one service |
| `docker compose build --no-cache` | Fresh rebuild |

---

## Dockerfile Instructions

```dockerfile
FROM python:3.12-slim          # Base image
WORKDIR /app                   # Set working directory
COPY requirements.txt .        # Copy file into container
RUN pip install -r req.txt     # Run command during build
ENV PYTHONUNBUFFERED=1         # Set environment variable
EXPOSE 8000                    # Document port (does NOT publish)
CMD ["uvicorn", "app:app"]     # Default run command
ARG VERSION=1.0                # Build-time variable
LABEL maintainer="name"        # Metadata
```

---

## Multi-Stage Build Pattern

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY . .
RUN adduser --disabled-password --no-create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

---

## docker-compose.yml Template

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: techpath
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U techpath"]
      interval: 5s
      retries: 5

volumes:
  pgdata:
```

---

## .dockerignore Template

```
__pycache__
*.pyc
.git
.env
.env.local
.venv
venv
tests/
*.md
.pytest_cache
node_modules
Dockerfile
docker-compose*.yml
```

---

## Registry Commands

| Command | What It Does |
|---------|-------------|
| `docker login` | Login to Docker Hub |
| `docker login ghcr.io` | Login to GitHub Registry |
| `docker tag app user/app:v1` | Tag image for push |
| `docker push user/app:v1` | Push to Docker Hub |
| `docker push ghcr.io/user/app:v1` | Push to GHCR |

---

## Cleanup

| Command | What It Does |
|---------|-------------|
| `docker container prune` | Remove stopped containers |
| `docker image prune -a` | Remove unused images |
| `docker volume prune` | Remove unused volumes |
| `docker system prune -a` | Remove EVERYTHING unused |
| `docker system df` | Check disk usage |

---

## Key Flags

| Flag | Meaning |
|------|---------|
| `-d` | Detached (background) |
| `-p host:container` | Port mapping |
| `-e KEY=VAL` | Environment variable |
| `-v host:container` | Volume mount |
| `-it` | Interactive terminal |
| `--rm` | Auto-remove on exit |
| `--name` | Container name |
| `--network` | Attach to network |
| `--env-file` | Load env from file |
| `--no-cache` | Skip build cache |

---

## Base Image Sizes

| Image | Size | Use |
|-------|------|-----|
| `python:3.12` | ~900 MB | Development |
| `python:3.12-slim` | ~150 MB | Production (recommended) |
| `python:3.12-alpine` | ~50 MB | Size-critical apps |
