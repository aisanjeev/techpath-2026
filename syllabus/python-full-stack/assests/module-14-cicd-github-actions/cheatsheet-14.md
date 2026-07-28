# CI/CD with GitHub Actions — Cheatsheet

**Module 14 — Quick Reference Card**

---

## Workflow File Location

```
.github/workflows/ci.yml
```

---

## Workflow Structure

```yaml
name: CI Pipeline                  # Workflow name

on:                                # Triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:                              # Jobs
  test:
    runs-on: ubuntu-latest         # Runner
    steps:                         # Steps
      - uses: actions/checkout@v4  # Action step
      - run: pytest                # Command step
```

---

## Triggers

| Trigger | Syntax |
|---------|--------|
| Push to branch | `on: push: branches: [main]` |
| Pull request | `on: pull_request: branches: [main]` |
| Schedule (cron) | `on: schedule: - cron: '0 0 * * *'` |
| Manual | `on: workflow_dispatch` |
| Release | `on: release: types: [published]` |
| File path filter | `on: push: paths: ['app/**']` |

---

## Common Actions

| Action | Version | Purpose |
|--------|---------|---------|
| `actions/checkout` | `@v4` | Clone repository |
| `actions/setup-python` | `@v5` | Install Python |
| `actions/setup-node` | `@v4` | Install Node.js |
| `actions/cache` | `@v4` | Cache dependencies |
| `actions/upload-artifact` | `@v4` | Upload files from job |
| `actions/download-artifact` | `@v4` | Download files to job |
| `docker/login-action` | `@v3` | Login to Docker registry |
| `docker/setup-buildx-action` | `@v3` | Set up Docker Buildx |
| `docker/build-push-action` | `@v6` | Build and push Docker image |
| `docker/metadata-action` | `@v5` | Auto-generate image tags |

---

## Python CI Steps

```yaml
steps:
  - uses: actions/checkout@v4

  - uses: actions/setup-python@v5
    with:
      python-version: '3.12'
      cache: 'pip'

  - run: pip install -r requirements.txt

  - run: ruff check app/              # Lint

  - run: black --check app/           # Format check

  - run: pytest --cov=app             # Test + coverage
    env:
      DATABASE_URL: sqlite:///test.db

  - run: mypy app/                    # Type check
```

---

## Matrix Build

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12']
    os: [ubuntu-latest, windows-latest]
  fail-fast: false

steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

---

## Job Dependencies

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    needs: lint              # Sequential
    runs-on: ubuntu-latest

  deploy:
    needs: [lint, test]      # Wait for both
    if: github.ref == 'refs/heads/main'
```

---

## Docker Build & Push to GHCR

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Secrets

```yaml
# Access a secret
${{ secrets.MY_SECRET }}

# Built-in token (no setup needed)
${{ secrets.GITHUB_TOKEN }}

# Environment variable from secret
env:
  API_KEY: ${{ secrets.API_KEY }}
```

**Where to add:** Repo → Settings → Secrets and variables → Actions

---

## SSH Deployment

```yaml
- name: Deploy
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/id_ed25519
    chmod 600 ~/.ssh/id_ed25519
    ssh -o StrictHostKeyChecking=no \
      ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} \
      "cd /opt/app && docker compose pull && docker compose up -d"
```

---

## Conditional Execution

```yaml
# Only on main branch
if: github.ref == 'refs/heads/main'

# Only on pull requests
if: github.event_name == 'pull_request'

# Always run (even on failure)
if: always()

# Only on success
if: success()

# Only on failure
if: failure()
```

---

## Context Variables

| Variable | Value |
|----------|-------|
| `${{ github.actor }}` | Username who triggered |
| `${{ github.ref }}` | Branch ref |
| `${{ github.sha }}` | Commit SHA |
| `${{ github.repository }}` | owner/repo |
| `${{ github.event_name }}` | push, pull_request, etc. |
| `${{ github.run_number }}` | Incremental run number |

---

## Environments

```yaml
jobs:
  deploy:
    environment: production    # Uses environment secrets + rules
    runs-on: ubuntu-latest
```

**Setup:** Repo → Settings → Environments → New environment

---

## Branch Protection Checklist

| Rule | Recommended |
|------|-------------|
| Require pull request | Yes |
| Required approvals | 1+ for teams |
| Require status checks | Yes (select CI job) |
| Dismiss stale approvals | Yes |
| Require conversation resolution | Yes |
| Restrict force pushes | Yes |
| Include administrators | Yes for production |

---

## Free Tier Limits

| Runner | Minutes/Month | Multiplier |
|--------|--------------|------------|
| Ubuntu | 2000 | 1x |
| Windows | 2000 | 2x |
| macOS | 2000 | 10x |

---

## Cron Schedule Examples

| Schedule | Cron |
|----------|------|
| Daily at midnight UTC | `0 0 * * *` |
| Every Monday 9 AM UTC | `0 9 * * 1` |
| Every 6 hours | `0 */6 * * *` |
| First of month | `0 0 1 * *` |

---

## CODEOWNERS

```
# .github/CODEOWNERS
*                @team-lead
/backend/        @backend-team
/.github/        @devops-team
Dockerfile       @devops-team
```
