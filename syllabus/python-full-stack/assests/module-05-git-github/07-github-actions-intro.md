# GitHub Actions — Your First CI/CD Pipeline

**Module 05 — Git, GitHub & Professional Workflow | Topic 7**

---

## What is CI/CD?

**CI (Continuous Integration):** Automatically run tests every time someone pushes code. Catch bugs before they reach production.

**CD (Continuous Deployment):** Automatically deploy your app when code is merged to the main branch.

**Real-world analogy:** Imagine a car factory. CI is the quality inspection line — every car part is tested before assembly. CD is the automatic shipping — once a car passes inspection, it goes straight to the showroom without manual steps.

### Why CI/CD?

| Without CI/CD | With CI/CD |
|---------------|-----------|
| "It works on my machine" | Tests run on a standard server |
| Manual testing before every deploy | Automated test suite |
| Developer forgets to run tests | Tests run on every push |
| Deploying at 2 AM manually | Automatic deployment on merge |
| Bugs reach production | Bugs caught before merge |

---

## What is GitHub Actions?

GitHub Actions is GitHub's built-in CI/CD tool. It runs **workflows** — automated scripts triggered by events (push, pull request, schedule).

### Key Concepts

| Concept | What It Is | Analogy |
|---------|-----------|---------|
| **Workflow** | A complete automation pipeline | A recipe |
| **Event** | What triggers the workflow (push, PR, schedule) | "Start cooking when guests arrive" |
| **Job** | A set of steps that run on one machine | One dish in the recipe |
| **Step** | A single task within a job | One instruction (chop onions) |
| **Action** | A reusable step made by the community | A pre-made spice mix |
| **Runner** | The server that runs the job | The kitchen |

---

## Your First Workflow

Create the file `.github/workflows/tests.yml`:

```yaml
# .github/workflows/tests.yml
name: Run Tests

# When to run this workflow
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# What to do
jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # Step 1: Get the code
      - name: Checkout code
        uses: actions/checkout@v4

      # Step 2: Set up Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Step 3: Install dependencies
      - name: Install dependencies
        run: |
          cd backend
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Step 4: Run linter
      - name: Lint with ruff
        run: |
          cd backend
          ruff check app/

      # Step 5: Run tests
      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v
```

### Breaking It Down

**`name:`** — The name shown in the GitHub Actions tab.

**`on:`** — Events that trigger the workflow:
```yaml
on:
  push:
    branches: [main, develop]    # Run on push to main or develop
  pull_request:
    branches: [main]             # Run on PRs targeting main
```

**`jobs:`** — The actual work:
```yaml
jobs:
  test:                          # Job name
    runs-on: ubuntu-latest       # Machine to run on
    steps:                       # List of steps
      - name: Step description
        run: command             # Shell command
      - name: Use community action
        uses: actions/setup-python@v5  # Pre-built action
        with:
          python-version: "3.12"       # Action input
```

---

## Common Workflow Patterns

### Run Tests on Multiple Python Versions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

This creates 3 parallel jobs — one for each Python version.

### Lint + Test + Build (Multi-Job Pipeline)

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check app/

  test:
    runs-on: ubuntu-latest
    needs: lint                    # Only run if lint passes
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=app

  build:
    runs-on: ubuntu-latest
    needs: test                    # Only run if test passes
    if: github.ref == 'refs/heads/main'  # Only on main branch
    steps:
      - uses: actions/checkout@v4
      - run: echo "Building for production..."
```

### Caching Dependencies (Faster Builds)

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: "3.12"

  - name: Cache pip packages
    uses: actions/cache@v4
    with:
      path: ~/.cache/pip
      key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      restore-keys: |
        ${{ runner.os }}-pip-

  - run: pip install -r requirements.txt
  - run: pytest tests/
```

Caching stores downloaded packages so they do not need to be downloaded every time.

---

## Environment Variables and Secrets

### Using Secrets

Store sensitive data (API keys, passwords) in GitHub Secrets:
1. Go to Repository > Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Add name and value (e.g., `DATABASE_URL` = `postgresql://...`)

```yaml
steps:
  - name: Run tests with database
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      SECRET_KEY: ${{ secrets.SECRET_KEY }}
    run: pytest tests/
```

### Using Environment Variables

```yaml
env:
  PYTHON_VERSION: "3.12"
  APP_ENV: "testing"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
```

---

## Practical Example: Full Python Project CI

```yaml
# .github/workflows/ci.yml
name: Python CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.12"

jobs:
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install tools
        run: pip install ruff black

      - name: Check formatting
        run: black --check app/ tests/

      - name: Lint
        run: ruff check app/ tests/

  test:
    name: Tests
    runs-on: ubuntu-latest
    needs: quality
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests with coverage
        run: pytest tests/ -v --cov=app --cov-report=term-missing

      - name: Check coverage threshold
        run: pytest tests/ --cov=app --cov-fail-under=80
```

---

## Viewing Workflow Results

### On GitHub

1. Go to your repository
2. Click the **Actions** tab
3. See a list of workflow runs with status icons:
   - Green checkmark = passed
   - Red X = failed
   - Yellow circle = running

### Status Badges

Add a badge to your README showing CI status:

```markdown
![CI](https://github.com/techpath/student-portal/actions/workflows/ci.yml/badge.svg)
```

### Workflow Run Details

Click on a workflow run to see:
- Which jobs ran and their status
- Log output for each step
- Time taken
- Which commit triggered it

---

## Common Triggers

| Trigger | When |
|---------|------|
| `push` | Code is pushed to specified branches |
| `pull_request` | A PR is opened, updated, or reopened |
| `schedule` | On a cron schedule |
| `workflow_dispatch` | Manual trigger from the Actions tab |
| `release` | A release is published |

```yaml
# Run every day at midnight UTC
on:
  schedule:
    - cron: '0 0 * * *'

# Allow manual trigger
on:
  workflow_dispatch:
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| CI/CD | Automate testing and deployment |
| Workflow | YAML file defining the automation pipeline |
| Jobs | Groups of steps that run on a machine |
| Steps | Individual commands or actions |
| Matrix | Test across multiple versions in parallel |
| Secrets | Store sensitive values securely |
| Cache | Speed up workflows by caching dependencies |
| Badges | Show CI status on your README |

---

*TechPath Institute — Python Full Stack Development*
