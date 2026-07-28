# Optimizing Docker Images

**Module 13 — Docker & Containerization | Topic 6**

---

## Why Image Size Matters

Amit built a FastAPI app. His Docker image was 1.2 GB. Every time he pushed it to a registry, it took 10 minutes. Every deployment downloaded 1.2 GB. His CI/CD pipeline was slow, and his server disk filled up fast.

After optimization, the image dropped to 180 MB — 85% smaller.

**Smaller images mean:**
- Faster builds (less to process)
- Faster deployments (less to download)
- Lower storage costs (registries charge by size)
- Smaller attack surface (fewer packages = fewer vulnerabilities)
- Faster container startup

---

## Strategy 1: Choose the Right Base Image

The base image is the biggest factor in image size.

| Base Image | Size | Notes |
|-----------|------|-------|
| `python:3.12` | ~900 MB | Full Debian, includes gcc and dev tools |
| `python:3.12-slim` | ~150 MB | Minimal Debian, no dev tools |
| `python:3.12-alpine` | ~50 MB | Alpine Linux, very small but compatibility issues |
| `ubuntu:22.04` | ~77 MB | Bare Ubuntu, you install Python yourself |

### Recommendation

**Use `python:3.12-slim` for most projects.** It is the best balance of size and compatibility.

```dockerfile
# Instead of this (900 MB base)
FROM python:3.12

# Use this (150 MB base)
FROM python:3.12-slim
```

### When to Use Alpine

Alpine is tiny but uses `musl` instead of `glibc`. Some Python packages (numpy, pandas, cryptography) need extra work:

```dockerfile
# Alpine needs extra build deps for some packages
FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev libffi-dev
RUN pip install cryptography  # Now this works
```

**Rule of thumb:** If your app uses only pure-Python packages (FastAPI, SQLAlchemy, Pydantic), Alpine works great. If you use numpy, pandas, or other C-extension packages, stick with slim.

---

## Strategy 2: Multi-Stage Builds

Multi-stage builds are the most powerful optimization technique. You use one stage to build/compile, and a separate clean stage for the final image.

> **Analogy:** Think of cooking biryani. You need a big messy kitchen (build stage) with all the spices, pots, and ingredients. But the final serving plate (production stage) only has the finished biryani — no mess.

### Before Multi-Stage (Single Stage)

```dockerfile
# Single stage — 500+ MB image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc libpq-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Problem: gcc and libpq-dev are still in the final image
# They were only needed to compile packages!
```

### After Multi-Stage

```dockerfile
# ========== Stage 1: Builder ==========
FROM python:3.12-slim AS builder

# Install build dependencies (only in this stage)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies into a virtual env
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ========== Stage 2: Production ==========
FROM python:3.12-slim

# Copy only the virtual env from builder (no gcc, no dev tools!)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install only runtime dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Non-root user for security
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**What happens:**
1. Stage 1 (`builder`) installs gcc and compiles everything
2. Stage 2 starts fresh from `python:3.12-slim`
3. Only the compiled Python packages (in `/opt/venv`) are copied over
4. gcc, build headers, and other junk are left behind in Stage 1
5. Final image is much smaller

**Size comparison:**

| Approach | Image Size |
|----------|-----------|
| Single stage with `python:3.12` | ~1.2 GB |
| Single stage with `python:3.12-slim` | ~350 MB |
| Multi-stage with `python:3.12-slim` | ~180 MB |

---

## Strategy 3: Optimize Layer Caching

Docker caches each layer. If a layer hasn't changed, it reuses the cached version. Order your Dockerfile instructions from least-changing to most-changing.

### Bad Order (Cache Broken Every Time)

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# BAD: Code changes on every build, invalidating pip install cache
COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### Good Order (Cache Preserved)

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# GOOD: Requirements rarely change — this layer stays cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code changes frequently — only this layer rebuilds
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

**The principle:** Things that change rarely go first (base image, system packages, pip install). Things that change often go last (your code).

---

## Strategy 4: The .dockerignore File

The `.dockerignore` file prevents unnecessary files from being sent to the Docker daemon during builds.

```
# .dockerignore

# Version control
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
.pytest_cache
.mypy_cache
.ruff_cache
*.egg-info

# Virtual environments
.venv
venv
env

# Environment files with secrets
.env
.env.local
.env.production

# IDE
.vscode
.idea

# Documentation
*.md
LICENSE
docs/

# Tests (not needed in production image)
tests/
test_*.py

# Docker files (don't need to copy Docker config into the image)
Dockerfile
docker-compose*.yml
.dockerignore

# OS files
.DS_Store
Thumbs.db

# Node.js (if frontend is separate)
node_modules
```

**Impact:** Without `.dockerignore`, Docker sends your entire project directory (including `.git`, `node_modules`, etc.) to the build context. A `.git` folder alone can be hundreds of MB.

---

## Strategy 5: Reduce Layer Count

Each `RUN` command creates a new layer. Combine related commands:

```dockerfile
# BAD — 4 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN rm -rf /var/lib/apt/lists/*

# GOOD — 1 layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
    && rm -rf /var/lib/apt/lists/*
```

### Use --no-install-recommends

```dockerfile
# Without: installs recommended packages too (larger)
RUN apt-get install -y curl

# With: installs only what's explicitly needed (smaller)
RUN apt-get install -y --no-install-recommends curl
```

### Clean Up in the Same Layer

```dockerfile
# BAD — cleanup is in a separate layer, original data still in previous layer
RUN apt-get update && apt-get install -y gcc
RUN rm -rf /var/lib/apt/lists/*

# GOOD — cleanup in the same layer
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*
```

---

## Strategy 6: Use pip Wisely

```dockerfile
# Don't cache pip downloads (saves space)
RUN pip install --no-cache-dir -r requirements.txt

# Pin exact versions for reproducible builds
# requirements.txt:
# fastapi==0.115.0
# uvicorn==0.30.0

# Generate pinned requirements
# pip freeze > requirements.txt
```

---

## Strategy 7: Run as Non-Root User

Not a size optimization, but a critical security practice:

```dockerfile
# Create a non-root user
RUN adduser --disabled-password --no-create-home appuser

# Switch to that user
USER appuser

# Now the app runs without root privileges
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

**Why?** If an attacker breaks into your container, they have limited permissions as `appuser` instead of full root access.

---

## Complete Optimized Dockerfile

Putting it all together — Priya's production-ready FastAPI Dockerfile:

```dockerfile
# ========== Stage 1: Build ==========
FROM python:3.12-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ========== Stage 2: Production ==========
FROM python:3.12-slim

# Runtime-only dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Non-root user
RUN adduser --disabled-password --no-create-home appuser

WORKDIR /app
COPY . .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Measuring Image Size

```bash
# Check image size
docker images my-app

# Detailed layer breakdown
docker history my-app

# Use dive tool for visual analysis
# Install: https://github.com/wagoodman/dive
dive my-app
```

---

## Optimization Checklist

| Check | Done? |
|-------|-------|
| Using `slim` or `alpine` base image | |
| Multi-stage build implemented | |
| `.dockerignore` file created | |
| `requirements.txt` copied before code | |
| Using `--no-cache-dir` with pip | |
| Using `--no-install-recommends` with apt | |
| Cleaning apt lists in the same layer | |
| Running as non-root user | |
| No secrets in the image | |
| Pinned package versions | |

---

## Practice Exercise

1. Build your FastAPI app without optimization — note the image size
2. Add a `.dockerignore` file — rebuild and compare size
3. Switch from `python:3.12` to `python:3.12-slim` — compare
4. Implement a multi-stage build — compare
5. Run `docker history my-app` to see layer sizes

---

*Next Topic: Container Registries — Docker Hub, GHCR, and pushing your images.*
