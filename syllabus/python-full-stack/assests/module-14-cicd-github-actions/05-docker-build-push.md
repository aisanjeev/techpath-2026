# Docker Build & Push in CI/CD

**Module 14 — CI/CD with GitHub Actions | Topic 5**

---

## Why Build Docker in CI?

When Rahul builds a Docker image on his laptop and pushes it to production, there are problems:

- His laptop might have different files than what is on GitHub
- He might forget to run tests first
- The build might include local debug settings
- There is no audit trail of what was built and when

**Building Docker images in CI/CD solves all of this.** The pipeline:
1. Runs all tests first
2. Builds from the exact code on GitHub
3. Tags with the git commit SHA (traceability)
4. Pushes to a registry automatically

---

## GitHub Container Registry (GHCR) Setup

GHCR is the easiest registry to use with GitHub Actions because:
- No separate account needed
- Uses the built-in `GITHUB_TOKEN` (no secrets to configure)
- Images are linked to your repository
- Free for public repos

### Workflow Permissions

For GHCR, your workflow needs `packages: write` permission:

```yaml
permissions:
  contents: read
  packages: write
```

---

## Basic Docker Build & Push Workflow

```yaml
# .github/workflows/docker.yml

name: Build & Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    name: Build & Push to GHCR
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

      - name: Build Docker image
        run: |
          docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
          docker tag ghcr.io/${{ github.repository }}:${{ github.sha }} \
                     ghcr.io/${{ github.repository }}:latest

      - name: Push Docker image
        run: |
          docker push ghcr.io/${{ github.repository }}:${{ github.sha }}
          docker push ghcr.io/${{ github.repository }}:latest
```

### What This Does

1. Checks out your code
2. Logs into GHCR using the built-in `GITHUB_TOKEN`
3. Builds the Docker image with a tag based on the git commit SHA
4. Also tags it as `latest`
5. Pushes both tags to GHCR

After running, your image is available at:
```
ghcr.io/your-username/your-repo:latest
ghcr.io/your-username/your-repo:abc1234567
```

---

## Using docker/build-push-action (Recommended)

The `docker/build-push-action` is a more powerful way to build Docker images in CI. It supports caching, multi-platform builds, and more.

```yaml
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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Understanding the Metadata Action

The `docker/metadata-action` automatically generates smart tags:

| Event | Generated Tag |
|-------|--------------|
| Push to `main` | `ghcr.io/user/app:main` |
| Push to `develop` | `ghcr.io/user/app:develop` |
| Commit SHA abc1234 | `ghcr.io/user/app:abc1234` |
| Release v1.2.3 | `ghcr.io/user/app:1.2.3` |

### Understanding Build Cache

```yaml
cache-from: type=gha        # Load cache from GitHub Actions cache
cache-to: type=gha,mode=max  # Save all layers to cache
```

Without cache: Every build downloads the base image and installs all packages (~3-5 minutes).
With cache: Unchanged layers are reused (~30 seconds for code-only changes).

---

## Complete Pipeline: Test → Build → Push

The real-world pattern is to test first, then build and push only if tests pass.

```yaml
# .github/workflows/ci-cd.yml

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Job 1: Run tests
  test:
    name: Lint & Test
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: sqlite+aiosqlite:///./test.db
      SECRET_KEY: ci-secret

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - run: pip install -r requirements.txt

      - name: Lint
        run: ruff check app/

      - name: Test
        run: pytest --cov=app --cov-fail-under=70

  # Job 2: Build and push Docker image (only after tests pass)
  build:
    name: Build & Push Docker
    runs-on: ubuntu-latest
    needs: test                              # Wait for tests
    if: github.ref == 'refs/heads/main'      # Only on main branch
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

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
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Flow

```
Push to main → Test (lint + pytest) → Build Docker → Push to GHCR
Push to develop → Test only (no build)
Pull Request → Test only (no build)
```

---

## Building for a Specific Subdirectory

If your Dockerfile is not in the root (e.g., in a monorepo):

```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: ./backend                     # Build from this directory
    file: ./backend/Dockerfile             # Use this Dockerfile
    push: true
    tags: ghcr.io/${{ github.repository }}/api:latest
```

---

## Pushing to Docker Hub Instead

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ${{ secrets.DOCKERHUB_USERNAME }}/my-app:latest
```

You need to add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` as GitHub Secrets (covered in the next topic).

---

## Verifying the Pushed Image

After the workflow runs:

1. Go to your GitHub repo → Packages (right sidebar)
2. Click on the package to see all tags
3. Pull and test locally:

```bash
docker pull ghcr.io/your-username/your-repo:latest
docker run -p 8000:8000 ghcr.io/your-username/your-repo:latest
```

---

## Practice Exercise

1. Create a workflow that builds and pushes to GHCR on push to main
2. Add a `test` job that must pass before building
3. Use `docker/build-push-action` with GitHub cache
4. Push to main and check the Packages section of your repo
5. Pull the image locally and run it

---

*Next Topic: GitHub Secrets — storing API keys and credentials securely.*
