# CI/CD Pipeline: GitHub Actions for Test, Build, and Deploy

**Module 17 — Full-Stack AI Product: Capstone Development | Topic 5**

---

## What is CI/CD?

CI/CD stands for Continuous Integration and Continuous Deployment. It is an automated pipeline that tests your code, builds your application, and deploys it — every time you push to GitHub.

Think of it like a quality control assembly line in a factory. When Amit at a car factory in Pune finishes assembling an engine, the engine goes through an automated inspection line: first it checks if all parts are present (tests), then it assembles the car body around it (build), and finally it drives the car to the showroom (deploy). If any step fails, the line stops and Amit gets notified.

CI/CD does the same thing for your code.

### CI vs CD

| Term | What It Does | When It Runs |
|------|-------------|-------------|
| **Continuous Integration (CI)** | Runs tests and checks code quality | Every push and pull request |
| **Continuous Deployment (CD)** | Deploys tested code to a server | After CI passes on the main branch |

### Why CI/CD Matters for Your Capstone

| Without CI/CD | With CI/CD |
|--------------|------------|
| You forget to run tests before deploying | Tests run automatically on every push |
| A bug reaches production because you did not test | Broken code is blocked from deploying |
| Deploying means SSH-ing into server and running commands manually | One push to main = automatic deployment |
| Team members break each other's code | Pull requests are tested before merging |

---

## GitHub Actions Basics

GitHub Actions is GitHub's built-in CI/CD platform. It is free for public repositories and offers 2,000 minutes per month for private repos on the free plan.

### Key Concepts

| Concept | What It Is | Analogy |
|---------|-----------|---------|
| **Workflow** | A YAML file that defines the entire pipeline | The factory blueprint |
| **Job** | A set of steps that run on one machine | A workstation on the assembly line |
| **Step** | A single command or action | One task at a workstation |
| **Trigger** | What starts the workflow | The "Start" button on the assembly line |
| **Runner** | The machine that runs your job | The worker at the workstation |
| **Secret** | An encrypted variable (API keys, passwords) | A locked cabinet for sensitive tools |

### Workflow File Location

All workflow files live in `.github/workflows/` in your repository:

```
my-capstone/
|-- .github/
|   |-- workflows/
|       |-- ci.yml          # Test and lint on every push
|       |-- deploy.yml      # Deploy to server on push to main
|-- app/
|-- tests/
|-- ...
```

---

## Writing Your CI Workflow

### Complete CI Workflow (Test + Lint)

Create `.github/workflows/ci.yml`:

```yaml
name: CI - Test and Lint

# When to run this workflow
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    # Set up a PostgreSQL service container for tests
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      # Step 1: Check out the code
      - name: Checkout code
        uses: actions/checkout@v4

      # Step 2: Set up Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      # Step 3: Install Poetry
      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      # Step 4: Cache dependencies (speeds up subsequent runs)
      - name: Cache Poetry dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pypoetry
          key: ${{ runner.os }}-poetry-${{ hashFiles('poetry.lock') }}
          restore-keys: |
            ${{ runner.os }}-poetry-

      # Step 5: Install dependencies
      - name: Install dependencies
        run: poetry install --no-interaction

      # Step 6: Run linting
      - name: Lint with Ruff
        run: poetry run ruff check app tests

      # Step 7: Run type checking
      - name: Type check with MyPy
        run: poetry run mypy app --ignore-missing-imports

      # Step 8: Run tests
      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://test_user:test_password@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-for-ci
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: poetry run pytest tests/ -v --tb=short

      # Step 9: Upload test results (optional but useful)
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results/
```

### Understanding the Workflow

Let us break down each section:

| Section | Purpose | Example |
|---------|---------|---------|
| `name` | Display name in GitHub UI | `CI - Test and Lint` |
| `on` | When to trigger the workflow | Push to main, PRs to main |
| `jobs` | Groups of steps that run together | `test`, `deploy` |
| `runs-on` | What operating system to use | `ubuntu-latest` |
| `services` | Database/Redis containers for tests | PostgreSQL, Redis |
| `steps` | Individual commands to execute | Checkout, install, test |
| `env` | Environment variables for a step | Database URL, API keys |
| `secrets` | Encrypted variables from repo settings | `${{ secrets.API_KEY }}` |

---

## Writing Your CD Workflow (Deploy)

### Deploy to Render

Create `.github/workflows/deploy.yml`:

```yaml
name: CD - Deploy to Production

on:
  push:
    branches: [main]

jobs:
  # First, run all tests
  test:
    name: Run Tests Before Deploy
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      - name: Install dependencies
        run: poetry install --no-interaction
      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://test_user:test_password@localhost:5432/test_db
          SECRET_KEY: test-secret-key
        run: poetry run pytest tests/ -v

  # Deploy only if tests pass
  deploy:
    name: Deploy to Server
    needs: test  # Wait for test job to pass
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/deploy/my-capstone
            git pull origin main
            poetry install --no-interaction
            poetry run alembic upgrade head
            sudo systemctl restart my-capstone

      - name: Notify on success
        if: success()
        run: echo "Deployment successful!"

      - name: Notify on failure
        if: failure()
        run: echo "Deployment failed! Check the logs."
```

### Deploy to VPS (Alternative)

If you are deploying to a VPS (like DigitalOcean or an AWS EC2 instance), the deploy step uses SSH:

```yaml
- name: Deploy to VPS
  uses: appleboy/ssh-action@v1
  with:
    host: ${{ secrets.VPS_HOST }}
    username: ${{ secrets.VPS_USER }}
    key: ${{ secrets.VPS_SSH_KEY }}
    script: |
      cd /var/www/my-capstone
      git pull origin main
      source .venv/bin/activate
      pip install -r requirements.txt
      alembic upgrade head
      sudo systemctl restart capstone-api
```

---

## Setting Up GitHub Secrets

Secrets are encrypted environment variables that your workflow can access but no one can read.

### How to Add Secrets

1. Go to your GitHub repository
2. Click **Settings** (tab) > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add each secret:

| Secret Name | Value | Used For |
|------------|-------|----------|
| `OPENAI_API_KEY` | `sk-your-key-here` | AI feature in tests |
| `SERVER_HOST` | `your-server-ip` | SSH deploy target |
| `SERVER_USER` | `deploy` | SSH username |
| `SSH_PRIVATE_KEY` | Your private key content | SSH authentication |
| `DATABASE_URL` | Production database URL | Database connection |

### Accessing Secrets in Workflows

```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

---

## Automated Testing with Pytest

Your CI pipeline is only as good as your tests. Here is how to write tests that CI can run.

### Test Structure

```
tests/
|-- __init__.py
|-- conftest.py           # Shared test fixtures
|-- test_auth.py          # Authentication tests
|-- test_items.py         # Domain model tests
|-- test_ai.py            # AI feature tests
|-- test_health.py        # Basic health check test
```

### conftest.py — Shared Test Setup

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
```

### Example Tests

```python
# tests/test_health.py
import pytest


@pytest.mark.anyio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.anyio
async def test_api_v1_root(client):
    response = await client.get("/api/v1/")
    assert response.status_code in [200, 404]  # Depends on your setup
```

---

## Handling Failures and Notifications

### What Happens When CI Fails?

When a workflow fails, GitHub shows a red X next to the commit. You can see exactly which step failed by clicking on the workflow run.

### Adding Failure Notifications

You can add a step to notify you when a workflow fails:

```yaml
- name: Notify on failure
  if: failure()
  run: |
    echo "CI failed on commit ${{ github.sha }}"
    echo "Check: https://github.com/${{ github.repository }}/actions"
```

### Common CI Failures and Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError` | Dependency not installed | Add it to `pyproject.toml` and re-run `poetry install` |
| Database connection refused | Service container not ready | Add health check options to service definition |
| Test passes locally but fails in CI | Different environment | Check Python version, environment variables |
| `PermissionError` on deploy | SSH key not configured | Double-check `SSH_PRIVATE_KEY` secret |
| Timeout | Tests take too long | Add `timeout-minutes: 10` to the job |

---

*TechPath Institute — Full-Stack AI Product: Capstone Development*
