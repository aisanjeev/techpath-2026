# CI/CD with GitHub Actions

**Module 14 — CI/CD with GitHub Actions | Topic 1**

---

## 1. What is CI/CD?

Think of it this way: you write code, push it to GitHub, and then **automatically** your code gets tested, checked for errors, built into a Docker image, and deployed to the server — all without you lifting a finger. That is CI/CD.

### The Three Stages

| Stage | Full Name | What It Does | Analogy |
|-------|-----------|-------------|---------|
| **CI** | Continuous Integration | Automatically test and check code every time someone pushes | Like a spelling/grammar checker that runs on every essay submission |
| **CD** (Delivery) | Continuous Delivery | Automatically build a deployable package (e.g., Docker image) | Like packaging a product and keeping it ready to ship |
| **CD** (Deployment) | Continuous Deployment | Automatically deploy to production server | Like the package auto-ships the moment it's ready |

```
Developer pushes code → CI runs tests → CD builds image → CD deploys to server
         ↓                    ↓                ↓                    ↓
      Git push          pytest + ruff     Docker build        SSH deploy
```

### Real-World Example

Imagine Priya is working on a FastAPI project for TechPath Institute. Without CI/CD, every time she pushes code, someone has to manually:
1. Pull the code on the server
2. Run tests
3. Check for lint errors
4. Build a Docker image
5. Deploy it

With CI/CD, all of this happens **automatically** when she pushes to GitHub.

---

## 2. DORA Metrics — Measuring DevOps Performance

DORA (DevOps Research and Assessment) defines four key metrics that measure how well a team does CI/CD:

| Metric | What It Measures | Good Target |
|--------|-----------------|-------------|
| **Deployment Frequency** | How often you deploy to production | Multiple times per day |
| **Lead Time for Changes** | Time from code commit to production | Less than 1 day |
| **Change Failure Rate** | % of deployments that cause failures | Less than 15% |
| **Time to Restore** | How fast you recover from a failure | Less than 1 hour |

> **Simple way to remember:** "How often, how fast, how reliable, how quick to fix" — these four questions tell you if your CI/CD pipeline is working well.

---

## 3. GitHub Actions — Overview

GitHub Actions is GitHub's built-in CI/CD tool. It's **free** for public repos and has generous free minutes for private repos.

### Why GitHub Actions?

| Feature | Benefit |
|---------|---------|
| Built into GitHub | No separate service needed — everything in one place |
| Free for public repos | Students and open-source projects pay nothing |
| YAML-based | Easy to read and write (just a text file) |
| Marketplace | 15,000+ pre-built actions you can reuse |
| Matrix builds | Test on multiple Python versions simultaneously |

### Key Terminology

| Term | Meaning | Analogy |
|------|---------|---------|
| **Workflow** | The entire automation pipeline (a YAML file) | A recipe |
| **Event/Trigger** | What starts the workflow (push, PR, schedule) | The "start cooking" signal |
| **Job** | A group of steps that run on one machine | One chef's task list |
| **Step** | A single command or action inside a job | One instruction in the recipe |
| **Runner** | The virtual machine that runs your job | The kitchen where cooking happens |
| **Action** | A reusable, pre-built step from the marketplace | A pre-made spice mix |

---

## 4. Workflow File — Anatomy

Workflow files live in `.github/workflows/` in your repository. They are written in YAML.

### Minimal Example

```yaml
# .github/workflows/hello.yml
name: Hello World                  # Name shown in GitHub UI

on: push                           # Trigger: run on every push

jobs:
  greet:                           # Job name
    runs-on: ubuntu-latest         # Runner: use Ubuntu virtual machine
    steps:
      - name: Say Hello
        run: echo "Namaste from TechPath Institute!"
```

### Full Anatomy

```yaml
name: CI Pipeline                  # 1. Workflow name

on:                                # 2. Triggers (when to run)
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:                              # 3. Jobs (what to do)
  test:                            # Job ID
    runs-on: ubuntu-latest         # 4. Runner
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]  # 5. Matrix (test on both)

    steps:                         # 6. Steps (ordered list)
      - uses: actions/checkout@v4  # Step 1: get code
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Run tests
        run: pytest
```

---

## 5. Triggers — When Does the Workflow Run?

### Common Triggers

```yaml
on:
  # 1. On every push to specific branches
  push:
    branches: [main, develop]

  # 2. On pull request (opened, updated, reopened)
  pull_request:
    branches: [main]

  # 3. On a schedule (cron syntax)
  schedule:
    - cron: "30 5 * * 1"          # Every Monday at 5:30 AM UTC (11:00 AM IST)

  # 4. Manual trigger (click a button in GitHub)
  workflow_dispatch:
    inputs:
      environment:
        description: "Deploy to which environment?"
        required: true
        default: "staging"
        type: choice
        options:
          - staging
          - production
```

### Cron Syntax Cheat Sheet

```
┌───── minute (0-59)
│ ┌───── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌───── month (1-12)
│ │ │ │ ┌───── day of week (0-6, 0 = Sunday)
│ │ │ │ │
* * * * *
```

| Example | Meaning |
|---------|---------|
| `0 6 * * *` | Every day at 6:00 AM UTC (11:30 AM IST) |
| `30 5 * * 1` | Every Monday at 5:30 AM UTC |
| `0 0 1 * *` | First day of every month at midnight |
| `0 */6 * * *` | Every 6 hours |

---

## 6. Jobs, Steps, and Runners

### Jobs

Each job runs on a **separate virtual machine** (runner). Jobs run in **parallel** by default, but you can make one job wait for another.

```yaml
jobs:
  test:                            # Job 1: run tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest

  lint:                            # Job 2: run linter (runs in PARALLEL with test)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .

  deploy:                          # Job 3: deploy (WAITS for test and lint)
    needs: [test, lint]            # This makes it sequential
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```

### Job Dependencies Diagram

```
push to main
    ├── test job ──────┐
    │                  ├──→ deploy job
    └── lint job ──────┘
    (parallel)          (waits for both)
```

### Runners

| Runner | OS | Use When |
|--------|----|----------|
| `ubuntu-latest` | Ubuntu Linux | Most Python/backend projects (recommended) |
| `windows-latest` | Windows | Windows-specific testing |
| `macos-latest` | macOS | iOS/macOS apps |

> **Tip:** Always use `ubuntu-latest` for Python projects — it is the fastest and has the most free minutes.

### Steps

Steps run **sequentially** inside a job. Two types:

```yaml
steps:
  # Type 1: Use a pre-built action (from GitHub Marketplace)
  - uses: actions/checkout@v4       # Action: checks out your code

  # Type 2: Run a shell command
  - name: Install dependencies
    run: pip install -r requirements.txt
```

---

## 7. Matrix Builds — Test on Multiple Versions

A matrix build tests your code on multiple Python versions (or OS, or Node versions) simultaneously.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Run tests
        run: pytest
```

This creates **2 parallel jobs** — one for Python 3.11 and one for Python 3.12. If your code passes on both, you know it is compatible.

### Matrix Visualization

```
push event
    ├── test (Python 3.11) ──→ ✅ Pass
    └── test (Python 3.12) ──→ ✅ Pass
```

---

## 8. Building a CI Pipeline — Step by Step

A typical CI pipeline for a Python project has these stages:

```
Checkout Code → Setup Python → Install Dependencies → Lint → Test → Coverage
```

### Stage 1: Checkout Code

```yaml
- uses: actions/checkout@v4
```
This downloads your repository code into the runner machine.

### Stage 2: Setup Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

### Stage 3: Install Dependencies (with Caching)

```yaml
- name: Cache pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: ${{ runner.os }}-pip-

- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

> **Why cache?** Without caching, pip downloads all packages from the internet every single run. With caching, it reuses previously downloaded packages — making your pipeline **2-3x faster**.

### Stage 4: Lint with Ruff

```yaml
- name: Lint with ruff
  run: ruff check . --output-format=github
```

Ruff is a super-fast Python linter (written in Rust). The `--output-format=github` flag makes errors show as annotations directly on the PR.

### Stage 5: Run Tests with Pytest

```yaml
- name: Run tests
  run: pytest --tb=short -q
```

### Stage 6: Coverage Report

```yaml
- name: Run tests with coverage
  run: |
    pip install pytest-cov
    pytest --cov=app --cov-report=term-missing --cov-report=xml
```

---

## 9. CD Pipeline — Build and Push Docker Image

After tests pass, the CD pipeline builds a Docker image and pushes it to **GHCR** (GitHub Container Registry).

### What is GHCR?

GHCR is like Docker Hub, but built into GitHub. It stores your Docker images right next to your code.

| Feature | Docker Hub | GHCR |
|---------|-----------|------|
| Owner | Docker Inc. | GitHub |
| Free private images | 1 | Unlimited (with GitHub free) |
| Integration | Manual setup | Automatic with GitHub Actions |
| URL | `docker.io/user/image` | `ghcr.io/user/image` |

### CD Workflow Steps

```yaml
deploy:
  needs: test                      # Only deploy if tests pass
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'  # Only on merge to main

  steps:
    # Step 1: Checkout code
    - uses: actions/checkout@v4

    # Step 2: Log in to GHCR
    - name: Log in to GitHub Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    # Step 3: Build and push Docker image
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          ghcr.io/${{ github.repository }}:latest
          ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### Image Tagging Strategy

| Tag | Purpose | Example |
|-----|---------|---------|
| `latest` | Always points to newest build | `ghcr.io/rahul/myapp:latest` |
| `<commit-sha>` | Unique per commit (for rollback) | `ghcr.io/rahul/myapp:a1b2c3d` |
| `v1.2.3` | Semantic version (for releases) | `ghcr.io/rahul/myapp:v1.2.3` |

---

## 10. GitHub Secrets — Storing Sensitive Data

**Never hardcode** passwords, API keys, or tokens in your workflow files. Use GitHub Secrets instead.

### How Secrets Work

```
You store: DATABASE_URL = "mysql://user:pass@db.example.com/mydb"
GitHub encrypts it and stores it securely
In the workflow: ${{ secrets.DATABASE_URL }} — GitHub injects the value at runtime
In logs: *** (GitHub automatically masks secret values)
```

### Adding Secrets

1. Go to your GitHub repo
2. Click **Settings** (tab) → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter name (e.g., `DATABASE_URL`) and value
5. Click **Add secret**

### Common Secrets for a Python Project

| Secret Name | What It Stores | Example Value |
|-------------|---------------|---------------|
| `DATABASE_URL` | Production DB connection | `mysql://user:pass@db.host/mydb` |
| `SECRET_KEY` | JWT/Flask/Django secret key | `super-secret-key-here` |
| `DEPLOY_SSH_KEY` | SSH private key for server access | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DEPLOY_HOST` | Server IP/hostname | `api.techpath.biz` |
| `DEPLOY_USER` | SSH username | `deploy` |
| `AZURE_STORAGE_KEY` | Cloud storage key | `abc123...` |

### Using Secrets in Workflows

```yaml
steps:
  - name: Deploy to server
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      SECRET_KEY: ${{ secrets.SECRET_KEY }}
    run: |
      echo "Deploying with production config..."
      # The actual values are injected but never printed
```

> **Important:** `GITHUB_TOKEN` is a special secret that GitHub creates automatically for every workflow run. You do not need to add it — it is always available. It has permissions to read/write to the repo, push images to GHCR, and more.

---

## 11. Deployment Strategies

### Strategy 1: SSH Deploy (VPS / Cloud VM)

For deploying to a VPS (like the TechPath staging server):

```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@v1
  with:
    host: ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USER }}
    key: ${{ secrets.DEPLOY_SSH_KEY }}
    script: |
      cd /home/deploy/myapp
      docker compose pull
      docker compose up -d
      echo "Deployment complete!"
```

### Strategy 2: Webhook Deploy

Trigger a deployment URL on your server:

```yaml
- name: Trigger deploy webhook
  run: |
    curl -X POST "${{ secrets.DEPLOY_WEBHOOK_URL }}" \
      -H "Authorization: Bearer ${{ secrets.DEPLOY_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d '{"image": "ghcr.io/${{ github.repository }}:latest"}'
```

### Strategy 3: Blue-Green Deployment

Run two identical environments (blue and green). Deploy to the idle one, test it, then switch traffic.

```
Current (blue) ──── users see this
New (green)    ──── deploy here, test it
                     ↓
Switch!        ──── green becomes active, blue becomes idle
```

---

## 12. Branch Protection Rules

Branch protection prevents anyone from pushing directly to `main` — all changes must go through a Pull Request with passing checks.

### Setting Up Branch Protection

1. Go to your repo → **Settings** → **Branches**
2. Click **Add branch protection rule**
3. Branch name pattern: `main`
4. Enable:
   - **Require a pull request before merging**
   - **Require status checks to pass before merging** → select your CI workflow
   - **Require branches to be up to date before merging**
   - **Do not allow bypassing the above settings**

### Why This Matters

| Without Protection | With Protection |
|-------------------|-----------------|
| Anyone can push broken code to main | All code must pass CI before merging |
| No review required | At least 1 reviewer must approve |
| Bugs reach production | Bugs caught before merging |
| Hard to rollback | Easy to revert a PR |

---

## 13. Rollback Strategies

When a deployment goes wrong, you need to quickly go back to the previous working version.

### Strategy 1: Git Revert

```bash
# Find the bad commit
git log --oneline -5

# Revert it (creates a new commit that undoes the changes)
git revert abc1234
git push origin main
# CI/CD will auto-deploy the reverted version
```

### Strategy 2: Deploy Previous Docker Image

```bash
# Your images are tagged by commit SHA
# Find the last working commit SHA
git log --oneline -5

# Pull and run the previous image
docker pull ghcr.io/rahul/myapp:prev-commit-sha
docker compose up -d
```

### Strategy 3: Re-run Previous Workflow

1. Go to **Actions** tab in GitHub
2. Find the last successful deployment
3. Click **Re-run all jobs**

---

## 14. Complete CI/CD Pipeline — Putting It All Together

Here is the full flow for a Python project at TechPath Institute:

```
Developer pushes code to feature branch
    ↓
Opens Pull Request to main
    ↓
CI Pipeline runs automatically:
    ├── Checkout code
    ├── Setup Python 3.11 & 3.12 (matrix)
    ├── Install dependencies (cached)
    ├── Lint with ruff
    ├── Run pytest with coverage
    └── Report results on the PR
    ↓
Reviewer approves the PR (if CI passes)
    ↓
PR merged to main
    ↓
CD Pipeline runs automatically:
    ├── Build Docker image
    ├── Push to GHCR (with commit SHA tag)
    └── Deploy to server via SSH
    ↓
Application is live!
```

### Environment Variables Summary

| Variable | Where It's Set | Used By |
|----------|---------------|---------|
| `GITHUB_TOKEN` | Auto-generated by GitHub | GHCR login, API calls |
| `DATABASE_URL` | GitHub Secrets | App configuration |
| `SECRET_KEY` | GitHub Secrets | JWT/session signing |
| `DEPLOY_HOST` | GitHub Secrets | SSH deployment |
| `DEPLOY_USER` | GitHub Secrets | SSH deployment |
| `DEPLOY_SSH_KEY` | GitHub Secrets | SSH deployment |

---

## 15. Best Practices

| Practice | Why |
|----------|-----|
| Keep workflows fast (under 5 minutes) | Slow pipelines discourage frequent pushes |
| Cache dependencies | Saves 1-2 minutes per run |
| Use matrix builds | Catch version-specific bugs early |
| Pin action versions (`@v4` not `@latest`) | Prevents unexpected breaking changes |
| Never put secrets in code | Use GitHub Secrets for all sensitive data |
| Use branch protection | Prevents broken code from reaching main |
| Tag Docker images with commit SHA | Makes rollback easy |
| Run lint and tests in parallel jobs | Faster feedback |
| Add status badges to README | Quick visibility of pipeline health |

### Adding a Status Badge

Add this to your `README.md`:

```markdown
![CI](https://github.com/USERNAME/REPO/actions/workflows/ci.yml/badge.svg)
```

This shows a green "passing" or red "failing" badge based on your latest CI run.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| CI | Automatically test and lint on every push/PR |
| CD | Automatically build Docker image and deploy on merge to main |
| Workflow | YAML file in `.github/workflows/` |
| Trigger | `on: push`, `pull_request`, `schedule`, `workflow_dispatch` |
| Job | Group of steps on one runner (parallel by default) |
| Matrix | Test on multiple Python versions simultaneously |
| Secrets | Store sensitive data securely (never in code) |
| GHCR | GitHub Container Registry — store Docker images |
| Branch Protection | Require CI to pass before merging to main |
| Rollback | `git revert`, re-deploy old Docker image, or re-run workflow |
| DORA Metrics | Frequency, lead time, failure rate, restore time |
