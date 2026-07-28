# Docker & Containerization

**Module 13 — Docker & Containerization | Topic 1**

---

## 1. Why Docker?

### The Problem Docker Solves

Imagine Rahul builds a FastAPI app on his laptop in Bhopal. Everything works perfectly. He sends the code to Priya in Pune, and she gets errors — different Python version, missing libraries, wrong OS settings.

**Docker solves this: "It works on my machine" becomes "It works on EVERY machine."**

### Containers vs Virtual Machines

| Feature | Virtual Machine (VM) | Docker Container |
|---|---|---|
| **What it runs** | Full operating system + app | Only the app + its dependencies |
| **Size** | 2-10 GB | 50-500 MB |
| **Startup time** | 1-5 minutes | 1-5 seconds |
| **Resource usage** | Heavy (needs full OS) | Light (shares host OS kernel) |
| **Isolation** | Complete | Process-level |
| **Analogy** | Renting a full house | Renting a room in a shared house |

**Simple analogy:** A VM is like carrying your entire kitchen to cook one dish. A Docker container is like carrying just the recipe and ingredients — you use whatever kitchen is available.

---

## 2. Core Docker Concepts

### Images

An **image** is a blueprint — a read-only template with everything your app needs to run (code, libraries, OS tools). Think of it like a recipe card.

```
Image = Your code + Python + Libraries + OS tools (all frozen together)
```

### Containers

A **container** is a running instance of an image. You can run many containers from one image, just like cooking the same recipe multiple times.

```
Image  -->  Container 1 (running)
       -->  Container 2 (running)
       -->  Container 3 (stopped)
```

### Layers

Docker images are built in **layers**. Each instruction in a Dockerfile creates a new layer. Layers are cached, so rebuilding is fast.

```
Layer 4: COPY . /app          (your code — changes often)
Layer 3: RUN pip install ...   (dependencies — changes sometimes)
Layer 2: WORKDIR /app          (working directory)
Layer 1: FROM python:3.12      (base image — rarely changes)
```

**Why layers matter:** If you only change your code (Layer 4), Docker reuses cached Layers 1-3, making builds much faster.

### Docker Hub

**Docker Hub** (hub.docker.com) is like the "app store" for Docker images. You can:
- **Pull** pre-built images (Python, PostgreSQL, Redis, Nginx)
- **Push** your own images for others to use
- Find **official images** maintained by the software creators

```bash
# Pull an image from Docker Hub
docker pull python:3.12-slim

# Pull PostgreSQL
docker pull postgres:16
```

---

## 3. Writing a Dockerfile

A **Dockerfile** is a text file with instructions to build an image. No file extension needed — the file is simply named `Dockerfile`.

### Dockerfile for a FastAPI App

```dockerfile
# Step 1: Start from a Python base image
FROM python:3.12-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy requirements first (for better caching)
COPY requirements.txt .

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy all application code
COPY . .

# Step 6: Tell Docker which port the app uses
EXPOSE 8000

# Step 7: Command to run when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile for a Django App

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for PostgreSQL client
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "techpath_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Key Dockerfile Instructions

| Instruction | Purpose | Example |
|---|---|---|
| `FROM` | Base image to start from | `FROM python:3.12-slim` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from host to image | `COPY . .` |
| `RUN` | Execute a command during build | `RUN pip install -r requirements.txt` |
| `EXPOSE` | Document which port the app uses | `EXPOSE 8000` |
| `CMD` | Default command when container starts | `CMD ["uvicorn", "app.main:app"]` |
| `ENV` | Set environment variables | `ENV APP_ENV=production` |
| `ARG` | Build-time variables | `ARG PYTHON_VERSION=3.12` |

---

## 4. Essential Docker Commands

### Building Images

```bash
# Build an image from a Dockerfile in the current directory
docker build -t techpath-api .

# Build with a specific tag/version
docker build -t techpath-api:v1.0 .

# Build with a different Dockerfile name
docker build -f Dockerfile.prod -t techpath-api:prod .
```

### Running Containers

```bash
# Run a container (basic)
docker run techpath-api

# Run in detached mode (background) with a name
docker run -d --name my-api techpath-api

# Run with port mapping (host:container)
docker run -d -p 8000:8000 --name my-api techpath-api

# Run with environment variables
docker run -d -p 8000:8000 \
  -e DATABASE_URL="sqlite:///./data/techpath.db" \
  -e SECRET_KEY="my-secret-key" \
  --name my-api techpath-api

# Run and remove container when it stops
docker run --rm -p 8000:8000 techpath-api
```

### Managing Containers

```bash
# List running containers
docker ps

# List ALL containers (including stopped)
docker ps -a

# Stop a container
docker stop my-api

# Start a stopped container
docker start my-api

# Restart a container
docker restart my-api

# Remove a container (must be stopped first)
docker rm my-api

# Force remove a running container
docker rm -f my-api
```

### Inspecting and Debugging

```bash
# View container logs
docker logs my-api

# Follow logs in real-time (like tail -f)
docker logs -f my-api

# Execute a command inside a running container
docker exec -it my-api bash

# Run a Python shell inside the container
docker exec -it my-api python

# Inspect container details
docker inspect my-api
```

### Managing Images

```bash
# List all images
docker images

# Remove an image
docker rmi techpath-api

# Remove all unused images
docker image prune

# Remove ALL unused Docker objects (careful!)
docker system prune
```

---

## 5. Volumes — Persistent Data

By default, data inside a container is **lost** when the container is removed. **Volumes** solve this by storing data outside the container.

```bash
# Create a named volume
docker volume create techpath-data

# Run with a volume mounted
docker run -d -p 5432:5432 \
  -v techpath-data:/var/lib/postgresql/data \
  --name my-db postgres:16

# Mount a local folder (bind mount)
docker run -d -p 8000:8000 \
  -v $(pwd)/app:/app/app \
  --name my-api techpath-api
```

| Volume Type | Use Case | Example |
|---|---|---|
| **Named volume** | Database storage, persistent data | `-v db-data:/var/lib/postgresql/data` |
| **Bind mount** | Development (live code reload) | `-v ./app:/app/app` |
| **tmpfs mount** | Temporary data (in memory only) | `--tmpfs /tmp` |

---

## 6. Networks — Container Communication

Containers need a shared **network** to talk to each other.

```bash
# Create a custom network
docker network create techpath-net

# Run containers on the same network
docker run -d --name my-db --network techpath-net postgres:16
docker run -d --name my-api --network techpath-net -p 8000:8000 techpath-api

# Inside my-api, connect to database using container name as hostname:
# DATABASE_URL = "postgresql://user:pass@my-db:5432/techpath"
```

**Key point:** On the same Docker network, containers can reach each other by container name (e.g., `my-db` becomes the hostname).

---

## 7. Docker Compose — Multi-Service Apps

Docker Compose lets you define and run **multiple containers** with a single YAML file. Instead of running 3-4 separate `docker run` commands, you write one `docker-compose.yml`.

### Basic docker-compose.yml

```yaml
version: "3.8"

services:
  # FastAPI web application
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://techpath:secret@db:5432/techpath_db
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      - db
      - cache

  # PostgreSQL database
  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=techpath
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=techpath_db
    volumes:
      - db-data:/var/lib/postgresql/data

  # Redis cache
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # Celery worker for background tasks
  worker:
    build: .
    command: celery -A app.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://techpath:secret@db:5432/techpath_db
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      - db
      - cache

volumes:
  db-data:
```

### Docker Compose Commands

```bash
# Start all services (detached)
docker compose up -d

# Start and rebuild images
docker compose up -d --build

# Stop all services
docker compose down

# Stop and remove volumes (deletes data!)
docker compose down -v

# View logs of all services
docker compose logs

# View logs of one service
docker compose logs web

# List running services
docker compose ps

# Run a command in a service
docker compose exec web python -c "print('Hello from TechPath!')"

# Scale a service (run multiple instances)
docker compose up -d --scale worker=3
```

---

## 8. Environment Variables and Secrets

### Using .env Files

Create a `.env` file (never commit this to Git!):

```env
# .env file for TechPath Docker setup
POSTGRES_USER=techpath_admin
POSTGRES_PASSWORD=Bhopal@Secure2026
POSTGRES_DB=techpath_production
SECRET_KEY=my-super-secret-jwt-key
APP_ENV=production
REDIS_PASSWORD=Redis@TechPath
```

Reference in docker-compose.yml:

```yaml
services:
  db:
    image: postgres:16
    env_file:
      - .env
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
```

### Secrets Management Best Practices

| Practice | Why |
|---|---|
| **Never hardcode secrets** in Dockerfile or code | Anyone with the image can see them |
| **Use `.env` files** for local development | Easy to manage, easy to exclude from Git |
| **Add `.env` to `.gitignore`** | Prevents accidental commit of secrets |
| **Use Docker secrets** in production (Swarm mode) | Encrypted, only available to assigned services |
| **Use environment variables** via CI/CD | Inject secrets at deployment time |
| **Rotate secrets regularly** | Limits damage if a secret is leaked |

### .dockerignore File

Create a `.dockerignore` to exclude files from the build context (like `.gitignore` for Docker):

```
# .dockerignore
.git
.gitignore
.env
.env.*
__pycache__
*.pyc
.pytest_cache
.vscode
.idea
node_modules
README.md
docker-compose*.yml
```

---

## 9. Optimizing Docker Images

### Multi-Stage Builds

Use multiple `FROM` statements to create smaller final images:

```dockerfile
# ---- Stage 1: Builder ----
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: Runtime ----
FROM python:3.12-slim

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /install /usr/local

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Result:** The final image has no build tools, no pip cache — just your app and its dependencies.

### Optimization Tips

| Tip | Before | After |
|---|---|---|
| Use `slim` or `alpine` base | `python:3.12` (1 GB) | `python:3.12-slim` (150 MB) |
| Use `.dockerignore` | Copies `.git`, `node_modules` | Copies only needed files |
| Combine `RUN` commands | 5 layers for apt-get | 1 layer, smaller image |
| Use `--no-cache-dir` with pip | Keeps pip cache (50+ MB) | No wasted space |
| Multi-stage build | Build tools in final image | Only runtime in final image |
| Order layers by change frequency | Code before deps | Deps before code (better caching) |

### Good Layer Ordering

```dockerfile
# GOOD: Dependencies first (change rarely), code last (changes often)
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .          # <-- rarely changes
RUN pip install -r requirements.txt
COPY . .                         # <-- changes often (only this layer rebuilds)
```

```dockerfile
# BAD: Code first means pip install runs every time you change code
FROM python:3.12-slim
WORKDIR /app
COPY . .                         # <-- changes often, invalidates ALL layers below
RUN pip install -r requirements.txt  # <-- re-runs even if requirements didn't change
```

---

## 10. Pushing Images to a Registry

### Push to Docker Hub

```bash
# Step 1: Log in to Docker Hub
docker login

# Step 2: Tag your image (username/image-name:tag)
docker tag techpath-api rahul2026/techpath-api:v1.0
docker tag techpath-api rahul2026/techpath-api:latest

# Step 3: Push to Docker Hub
docker push rahul2026/techpath-api:v1.0
docker push rahul2026/techpath-api:latest

# Step 4: Anyone can now pull your image
docker pull rahul2026/techpath-api:v1.0
```

### Push to GitHub Container Registry (GHCR)

```bash
# Step 1: Create a Personal Access Token on GitHub
#         (Settings > Developer settings > Personal access tokens)
#         Scopes needed: write:packages, read:packages, delete:packages

# Step 2: Log in to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Step 3: Tag for GHCR
docker tag techpath-api ghcr.io/rahul2026/techpath-api:v1.0

# Step 4: Push
docker push ghcr.io/rahul2026/techpath-api:v1.0
```

### Docker Hub vs GHCR

| Feature | Docker Hub | GHCR |
|---|---|---|
| **Free private repos** | 1 | Unlimited |
| **Public repos** | Unlimited | Unlimited |
| **CI/CD integration** | Works with all | Best with GitHub Actions |
| **Best for** | Public images | GitHub-based projects |

---

## 11. Quick Reference — Command Cheat Sheet

| Task | Command |
|---|---|
| Build image | `docker build -t name .` |
| Run container | `docker run -d -p 8000:8000 --name c1 name` |
| List containers | `docker ps` (running) / `docker ps -a` (all) |
| Stop container | `docker stop c1` |
| Remove container | `docker rm c1` |
| View logs | `docker logs c1` / `docker logs -f c1` |
| Shell into container | `docker exec -it c1 bash` |
| List images | `docker images` |
| Remove image | `docker rmi name` |
| Compose up | `docker compose up -d` |
| Compose down | `docker compose down` |
| Compose logs | `docker compose logs -f` |
| Compose rebuild | `docker compose up -d --build` |
| Create volume | `docker volume create vol1` |
| Create network | `docker network create net1` |
| Push to Hub | `docker push user/image:tag` |
| Clean everything | `docker system prune -a` |

---

## 12. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---|---|---|
| Using `CMD` with wrong format | Container exits immediately | Use exec form: `CMD ["uvicorn", ...]` not `CMD uvicorn ...` |
| Forgetting `--host 0.0.0.0` | Can't access app from outside container | Add `--host 0.0.0.0` to uvicorn/gunicorn |
| Not using `.dockerignore` | Image is huge, builds are slow | Create `.dockerignore` with `.git`, `__pycache__`, etc. |
| Hardcoding secrets in Dockerfile | Security risk | Use `ENV` or `.env` files instead |
| Not mapping ports | App runs but no access from browser | Use `-p 8000:8000` |
| Data lost when container removed | No persistence | Use volumes for database data |
| `COPY . .` before `pip install` | Dependencies reinstall on every code change | Copy `requirements.txt` first, install, then copy code |

---

*TechPath Institute — Module 13: Docker & Containerization*
*"Containers make deployment predictable — build once, run anywhere."*
