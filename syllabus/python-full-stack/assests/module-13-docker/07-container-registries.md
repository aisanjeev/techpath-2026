# Container Registries — Docker Hub, GHCR & Pushing Images

**Module 13 — Docker & Containerization | Topic 7**

---

## What Is a Container Registry?

A container registry is a storage service for Docker images. It is like GitHub, but for Docker images instead of code.

> **Analogy:** If Docker images are movies, a container registry is Netflix — a place to store, organize, and distribute them.

When you run `docker pull python:3.12-slim`, Docker downloads the image from **Docker Hub**, the default public registry. You can also push your own images to a registry so your team, CI/CD pipeline, or servers can pull them.

---

## Popular Container Registries

| Registry | URL | Free Tier | Best For |
|----------|-----|-----------|----------|
| **Docker Hub** | hub.docker.com | 1 private repo, unlimited public | Personal projects, open source |
| **GitHub Container Registry (GHCR)** | ghcr.io | Unlimited (with GitHub plan) | Projects already on GitHub |
| **Azure Container Registry (ACR)** | azure.microsoft.com | Basic tier ₹400/month | Azure deployments |
| **AWS ECR** | aws.amazon.com | 500 MB free | AWS deployments |
| **Google Artifact Registry** | cloud.google.com | 500 MB free | GCP deployments |

**For this course, we focus on Docker Hub and GHCR** — both are free and widely used.

---

## Docker Hub

### Creating an Account

1. Go to hub.docker.com
2. Sign up with email (use your GitHub account for easy login)
3. Choose a username (e.g., `rahul2024`, `priyatech`)

### Logging In from Terminal

```bash
# Login to Docker Hub
docker login

# It will ask for:
# Username: rahul2024
# Password: (your Docker Hub password or access token)
```

**Tip:** Use an **Access Token** instead of your password:
1. Go to Docker Hub → Account Settings → Security → Access Tokens
2. Generate a new token
3. Use it as your password when running `docker login`

### Image Naming for Docker Hub

To push an image to Docker Hub, it must be named in this format:

```
username/image-name:tag

Examples:
  rahul2024/fastapi-app:v1.0
  rahul2024/fastapi-app:latest
  priyatech/django-shop:prod
```

### Pushing an Image

```bash
# Step 1: Build with the correct name
docker build -t rahul2024/fastapi-app:v1.0 .

# Step 2: Login (if not already)
docker login

# Step 3: Push
docker push rahul2024/fastapi-app:v1.0

# Push with multiple tags
docker tag rahul2024/fastapi-app:v1.0 rahul2024/fastapi-app:latest
docker push rahul2024/fastapi-app:latest
```

### Pulling an Image

```bash
# Pull from Docker Hub
docker pull rahul2024/fastapi-app:v1.0

# Run it
docker run -d -p 8000:8000 rahul2024/fastapi-app:v1.0
```

---

## GitHub Container Registry (GHCR)

GHCR is Docker Hub's competitor, tightly integrated with GitHub. If your code is on GitHub, GHCR is the natural choice.

### Why GHCR?

- **Free** for public and private repos (within GitHub plan limits)
- **Integrated** with GitHub Actions (easy CI/CD)
- **Permissions** tied to your GitHub repo (no separate access management)
- **Visibility** linked to repo visibility (public repo = public images)

### Image Naming for GHCR

```
ghcr.io/github-username/image-name:tag

Examples:
  ghcr.io/rahul2024/fastapi-app:v1.0
  ghcr.io/priyatech/django-shop:main
  ghcr.io/techpath-institute/api:sha-abc1234
```

### Logging In to GHCR

You need a **GitHub Personal Access Token (PAT)** with `write:packages` permission.

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with these permissions:
   - `write:packages`
   - `read:packages`
   - `delete:packages` (optional)
3. Copy the token

```bash
# Login to GHCR
echo "YOUR_GITHUB_TOKEN" | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
```

### Pushing to GHCR

```bash
# Step 1: Build with GHCR naming
docker build -t ghcr.io/rahul2024/fastapi-app:v1.0 .

# Step 2: Login
echo "$GITHUB_TOKEN" | docker login ghcr.io -u rahul2024 --password-stdin

# Step 3: Push
docker push ghcr.io/rahul2024/fastapi-app:v1.0
```

### Pulling from GHCR

```bash
# Public images — no login needed
docker pull ghcr.io/rahul2024/fastapi-app:v1.0

# Private images — login first
echo "$GITHUB_TOKEN" | docker login ghcr.io -u rahul2024 --password-stdin
docker pull ghcr.io/rahul2024/fastapi-app:v1.0
```

---

## Tagging Strategies

Tags identify different versions of your image. A good tagging strategy is crucial.

### Common Tagging Patterns

| Tag | Meaning | Example |
|-----|---------|---------|
| `latest` | Most recent build | `my-app:latest` |
| `v1.0.0` | Semantic version | `my-app:v1.0.0` |
| `main` | Built from main branch | `my-app:main` |
| `develop` | Built from develop branch | `my-app:develop` |
| `sha-abc1234` | Git commit SHA | `my-app:sha-abc1234` |
| `20240715` | Date-based | `my-app:20240715` |

### Best Practices

```bash
# Tag with version AND latest
docker build -t my-app:v1.2.0 -t my-app:latest .

# In CI/CD, tag with git SHA for traceability
GIT_SHA=$(git rev-parse --short HEAD)
docker build -t ghcr.io/user/app:${GIT_SHA} -t ghcr.io/user/app:latest .
```

**Avoid relying only on `latest`:**
- `latest` is just a convention — it does not automatically point to the newest image
- You must explicitly tag and push as `latest`
- In production, always use specific version tags for reproducibility

---

## Automating with GitHub Actions

The real power comes from automating image builds and pushes in CI/CD.

```yaml
# .github/workflows/docker-publish.yml

name: Build & Push Docker Image

on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
```

This workflow:
1. Triggers on pushes to `main` or new releases
2. Logs into GHCR using the built-in `GITHUB_TOKEN`
3. Builds the Docker image
4. Pushes it with two tags: `latest` and the git commit SHA

---

## Managing Images in a Registry

### Docker Hub Web Interface

- View your images at hub.docker.com
- See tags, pull counts, and vulnerability scans
- Set image visibility (public/private)
- Configure automated builds (linked to GitHub)

### GHCR Web Interface

- View packages at github.com/USERNAME?tab=packages
- Or in your repository → Packages (right sidebar)
- Manage visibility and permissions per package

### CLI Management

```bash
# List local images
docker images

# Remove local image
docker rmi ghcr.io/rahul2024/fastapi-app:v1.0

# Search Docker Hub
docker search fastapi

# Inspect remote image (without pulling)
docker manifest inspect ghcr.io/rahul2024/fastapi-app:v1.0
```

---

## Private vs Public Images

| Feature | Public Image | Private Image |
|---------|-------------|---------------|
| Who can pull? | Anyone | Only authorized users |
| Authentication needed? | No | Yes |
| Use case | Open source, shared tools | Company apps, proprietary code |
| Docker Hub limit | Unlimited | 1 free private repo |
| GHCR limit | Unlimited | Unlimited (within plan) |

### Making a GHCR Image Public

By default, GHCR images inherit the repository's visibility. To make an image public:

1. Go to your GitHub profile → Packages
2. Click on the package
3. Package Settings → Change Visibility → Public

---

## Security Considerations

### Scanning for Vulnerabilities

```bash
# Docker Scout (built into Docker Desktop)
docker scout quickview my-app:latest

# Trivy (popular open-source scanner)
trivy image my-app:latest
```

### Do Not Push Images with Secrets

```bash
# Check what's in your image before pushing
docker run --rm my-app:latest ls -la /app
docker run --rm my-app:latest cat /app/.env  # Should fail!
docker history my-app:latest  # Check no secrets in layers
```

### Use Signed Images

```bash
# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1
docker push rahul2024/fastapi-app:v1.0  # This push is now signed
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Login to Docker Hub | `docker login` |
| Login to GHCR | `echo $TOKEN \| docker login ghcr.io -u USER --password-stdin` |
| Tag an image | `docker tag app:v1 user/app:v1` |
| Push to Docker Hub | `docker push user/app:v1` |
| Push to GHCR | `docker push ghcr.io/user/app:v1` |
| Pull an image | `docker pull ghcr.io/user/app:v1` |
| List local images | `docker images` |
| Search Docker Hub | `docker search python` |
| Scan for vulnerabilities | `docker scout quickview app:v1` |

---

## Practice Exercise

1. Create a Docker Hub account (if you don't have one)
2. Build your FastAPI app image with proper naming: `username/my-api:v1.0`
3. Push it to Docker Hub
4. Create a GitHub PAT and login to GHCR
5. Tag and push the same image to GHCR
6. Pull the image on a different machine (or after removing locally)
7. Set up automated builds with GitHub Actions

---

*Next Topic: Interactive Dockerfile Builder — visually build Dockerfiles with layer size estimates.*
