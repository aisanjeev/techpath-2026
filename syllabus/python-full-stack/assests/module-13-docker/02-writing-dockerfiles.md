# Writing Dockerfiles

**Module 13 — Docker & Containerization | Topic 2**

---

## What Is a Dockerfile?

A **Dockerfile** is a plain text file containing step-by-step instructions to build a Docker image. Think of it as a recipe — each line is one cooking step, and the final dish is your Docker image.

The file is always named `Dockerfile` (no extension, capital D).

```
Your Project Folder/
├── app/
│   ├── main.py
│   └── models.py
├── requirements.txt
├── Dockerfile          ← This file
└── .dockerignore
```

---

## Dockerfile Instructions — The Building Blocks

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Base image to start from | `FROM python:3.12-slim` |
| `WORKDIR` | Set working directory inside container | `WORKDIR /app` |
| `COPY` | Copy files from your machine into the container | `COPY . /app` |
| `RUN` | Run a command during build (install packages) | `RUN pip install -r requirements.txt` |
| `ENV` | Set environment variables | `ENV PYTHONDONTWRITEBYTECODE=1` |
| `EXPOSE` | Document which port the app uses | `EXPOSE 8000` |
| `CMD` | Default command when container starts | `CMD ["uvicorn", "main:app"]` |
| `ENTRYPOINT` | Fixed command (cannot be overridden easily) | `ENTRYPOINT ["python"]` |
| `ARG` | Build-time variable | `ARG APP_VERSION=1.0` |
| `LABEL` | Add metadata to image | `LABEL maintainer="rahul@techpath.biz"` |

---

## Your First Dockerfile — A Simple Python Script

Let us start simple. Suppose Priya has a Python script `hello.py`:

```python
# hello.py
print("Hello from TechPath Docker container!")
print("This app is running inside a container.")
```

**Dockerfile:**

```dockerfile
# Step 1: Start with a Python base image
FROM python:3.12-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the script into the container
COPY hello.py .

# Step 4: Run the script when the container starts
CMD ["python", "hello.py"]
```

**Build and run:**

```bash
# Build the image (don't forget the dot at the end!)
docker build -t hello-app .

# Run the container
docker run hello-app
# Output: Hello from TechPath Docker container!
```

---

## Dockerfile for FastAPI

This is the most common Dockerfile you will write in this course. Let us build one step by step.

**Project structure:**

```
fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

**requirements.txt:**

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
pydantic==2.9.0
```

**Dockerfile:**

```dockerfile
# ---- Base Image ----
# Use slim variant — smaller than full, bigger than alpine but more compatible
FROM python:3.12-slim

# ---- Environment Variables ----
# Prevent Python from writing .pyc files (cleaner container)
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr (see logs immediately)
ENV PYTHONUNBUFFERED=1

# ---- Working Directory ----
WORKDIR /app

# ---- Install Dependencies First (for layer caching) ----
# Copy only requirements first — this layer is cached if requirements don't change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy Application Code ----
# This layer changes frequently, so it comes AFTER dependency installation
COPY ./app ./app

# ---- Expose Port ----
# Document that the app listens on port 8000
EXPOSE 8000

# ---- Start Command ----
# Run uvicorn when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Why `--host 0.0.0.0`?

By default, uvicorn binds to `127.0.0.1` (localhost only). Inside a container, this means the app is only accessible from within the container itself. Using `0.0.0.0` makes it accessible from outside the container.

---

## Dockerfile for Django

Django apps need a few extra steps — collecting static files and using gunicorn for production.

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (needed for some Python packages)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run with gunicorn (production WSGI server)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

---

## Understanding Each Instruction

### FROM — The Starting Point

Every Dockerfile starts with `FROM`. It defines the base image.

```dockerfile
# Full Python (large, has everything)
FROM python:3.12

# Slim Python (smaller, most things work)
FROM python:3.12-slim

# Alpine Python (tiny, some packages need extra work)
FROM python:3.12-alpine

# Ubuntu base (when you need full control)
FROM ubuntu:22.04
```

**Which to choose?**

| Base Image | Size | Best For |
|-----------|------|----------|
| `python:3.12` | ~900 MB | Development, debugging |
| `python:3.12-slim` | ~150 MB | Production (recommended) |
| `python:3.12-alpine` | ~50 MB | When size matters most |

> **Recommendation for beginners:** Always start with `python:3.12-slim`. It is a good balance of size and compatibility.

### WORKDIR — Set the Working Directory

```dockerfile
WORKDIR /app
```

This creates the `/app` directory inside the container and makes it the current directory. All subsequent `COPY`, `RUN`, and `CMD` instructions run relative to this directory.

### COPY — Bring Files Into the Container

```dockerfile
# Copy a single file
COPY requirements.txt .

# Copy a directory
COPY ./app ./app

# Copy everything
COPY . .
```

> **Important:** The `.` at the end means "current working directory inside the container" (which is `/app` because of `WORKDIR`).

### RUN — Execute Commands During Build

```dockerfile
# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install system packages
RUN apt-get update && apt-get install -y curl

# Create a directory
RUN mkdir -p /app/data
```

**Tip:** Combine related `RUN` commands with `&&` to reduce layers:

```dockerfile
# BAD — creates 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# GOOD — creates 1 layer
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
```

### EXPOSE — Document the Port

```dockerfile
EXPOSE 8000
```

`EXPOSE` does **not** actually publish the port. It is documentation — telling other developers which port the app uses. You still need `-p` when running the container.

### CMD vs ENTRYPOINT

| Feature | CMD | ENTRYPOINT |
|---------|-----|------------|
| Can be overridden? | Yes, easily | No (need `--entrypoint`) |
| Use case | Default command | Fixed command |
| Syntax | `CMD ["python", "app.py"]` | `ENTRYPOINT ["python"]` |

```dockerfile
# CMD — user can override
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
# docker run myapp              → runs uvicorn
# docker run myapp python shell → runs python shell instead

# ENTRYPOINT — always runs python
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run myapp              → runs python app.py
# docker run myapp test.py      → runs python test.py
```

**For most web apps, use CMD.**

---

## The .dockerignore File

Just like `.gitignore`, the `.dockerignore` file tells Docker which files to skip when copying.

```
# .dockerignore
__pycache__
*.pyc
.git
.gitignore
.env
.env.local
.venv
venv
*.md
tests/
.pytest_cache
.mypy_cache
.ruff_cache
node_modules
```

**Why it matters:**
- Smaller build context = faster builds
- Prevents sensitive files (`.env`) from getting into the image
- Avoids copying unnecessary files (tests, docs, git history)

---

## Build and Run Your Image

```bash
# Build the image
docker build -t my-fastapi-app .

# Build with a specific tag
docker build -t my-fastapi-app:v1.0 .

# Run the container
docker run -p 8000:8000 my-fastapi-app

# Run in the background (detached mode)
docker run -d -p 8000:8000 --name api my-fastapi-app

# Run with environment variables
docker run -d -p 8000:8000 -e DATABASE_URL=sqlite:///./data/app.db my-fastapi-app
```

**The `-p` flag maps ports:**
```
-p 8000:8000
    ↑       ↑
    Host    Container
    port    port
```

So `localhost:8000` on your machine connects to port `8000` inside the container.

---

## Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting the `.` at the end of `docker build` | Build fails — no context | `docker build -t app .` |
| `COPY . .` before `pip install` | Cache invalidated on every code change | Copy `requirements.txt` first, install, then copy code |
| Not using `--host 0.0.0.0` | App unreachable from outside container | Add `--host 0.0.0.0` to uvicorn/gunicorn |
| Copying `.env` into the image | Secrets baked into the image | Add `.env` to `.dockerignore` |
| Using `latest` tag | Unpredictable builds | Always specify version: `python:3.12-slim` |

---

## Practice Exercise

1. Create a simple FastAPI app with one endpoint: `GET /` returns `{"message": "Hello from Docker!"}`
2. Write a `Dockerfile` for it
3. Create a `.dockerignore` file
4. Build the image: `docker build -t my-api .`
5. Run it: `docker run -p 8000:8000 my-api`
6. Open `http://localhost:8000` in your browser

---

*Next Topic: Docker Commands — managing containers, images, volumes, and networks.*
