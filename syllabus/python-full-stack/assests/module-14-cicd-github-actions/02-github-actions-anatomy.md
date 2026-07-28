# GitHub Actions Anatomy — The YAML Workflow File

**Module 14 — CI/CD with GitHub Actions | Topic 2**

---

## Where Workflows Live

GitHub Actions workflows are YAML files stored in a specific folder in your repository:

```
your-repo/
├── .github/
│   └── workflows/
│       ├── ci.yml          ← Your CI pipeline
│       ├── deploy.yml      ← Your deployment pipeline
│       └── scheduled.yml   ← Scheduled tasks
├── app/
├── tests/
└── README.md
```

**Rules:**
- Files must be in `.github/workflows/`
- Files must have `.yml` or `.yaml` extension
- You can have as many workflow files as you want
- Each file defines one workflow

---

## The Basic Structure

Every workflow file has these sections:

```yaml
# 1. NAME — What is this workflow called?
name: CI Pipeline

# 2. TRIGGERS — When does it run?
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# 3. JOBS — What does it do?
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        run: echo "Running tests..."
```

Let us break down each section.

---

## Section 1: Name

```yaml
name: CI Pipeline
```

This appears in the GitHub Actions tab. Use a clear, descriptive name.

Good names: `CI Pipeline`, `Deploy to Production`, `Nightly Tests`
Bad names: `workflow1`, `test`, `stuff`

---

## Section 2: Triggers (on)

The `on` section defines **when** the workflow runs.

### Push Trigger

```yaml
# Run when code is pushed to main or develop
on:
  push:
    branches: [main, develop]
```

```yaml
# Run on push to any branch
on: push
```

```yaml
# Run only when specific files change
on:
  push:
    branches: [main]
    paths:
      - 'app/**'
      - 'tests/**'
      - 'requirements.txt'
```

### Pull Request Trigger

```yaml
# Run when a PR targets main
on:
  pull_request:
    branches: [main]
```

```yaml
# Run on specific PR events
on:
  pull_request:
    types: [opened, synchronize, reopened]
```

### Schedule Trigger (Cron)

```yaml
# Run every day at 2 AM UTC
on:
  schedule:
    - cron: '0 2 * * *'
```

Cron format: `minute hour day-of-month month day-of-week`

| Schedule | Cron Expression |
|----------|----------------|
| Every day at midnight | `0 0 * * *` |
| Every Monday at 9 AM | `0 9 * * 1` |
| Every 6 hours | `0 */6 * * *` |
| First of every month | `0 0 1 * *` |

### Manual Trigger (workflow_dispatch)

```yaml
# Allow running manually from GitHub UI
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy to which environment?'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

This adds a "Run workflow" button in the Actions tab.

### Multiple Triggers

```yaml
# Combine triggers
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:
```

---

## Section 3: Jobs

Jobs define **what** the workflow does. Each job runs on a separate virtual machine.

### Single Job

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

### Multiple Jobs

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check .

  test:
    runs-on: ubuntu-latest
    needs: lint                    # Run after lint passes
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest

  deploy:
    runs-on: ubuntu-latest
    needs: test                    # Run after test passes
    if: github.ref == 'refs/heads/main'   # Only on main branch
    steps:
      - run: echo "Deploying..."
```

**By default, jobs run in parallel.** Use `needs` to make them sequential.

---

## Understanding Steps

Steps are the individual tasks within a job.

### Action Steps (uses)

```yaml
steps:
  # Use a pre-built action from the marketplace
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.12'
      cache: 'pip'                # Cache pip packages for speed
```

**`uses`** runs a pre-built action. The format is `owner/repo@version`.

Common actions:

| Action | Purpose |
|--------|---------|
| `actions/checkout@v4` | Clone your repo |
| `actions/setup-python@v5` | Install Python |
| `actions/setup-node@v4` | Install Node.js |
| `actions/cache@v4` | Cache dependencies |
| `docker/build-push-action@v6` | Build & push Docker |
| `docker/login-action@v3` | Login to Docker registry |

### Command Steps (run)

```yaml
steps:
  # Run shell commands
  - name: Install dependencies
    run: pip install -r requirements.txt

  # Multi-line commands
  - name: Run full test suite
    run: |
      pip install pytest pytest-cov
      pytest --cov=app --cov-report=term-missing
      echo "Tests completed!"
```

**`run`** executes shell commands directly.

---

## Environment Variables

```yaml
jobs:
  test:
    runs-on: ubuntu-latest

    # Job-level env vars
    env:
      DATABASE_URL: sqlite:///test.db
      PYTHONDONTWRITEBYTECODE: 1

    steps:
      - name: Step with its own env var
        run: echo "Testing on $DATABASE_URL"
        env:
          DEBUG: true
```

### GitHub Context Variables

GitHub provides built-in variables:

| Variable | Value |
|----------|-------|
| `${{ github.actor }}` | Username who triggered the workflow |
| `${{ github.ref }}` | Branch ref (e.g., `refs/heads/main`) |
| `${{ github.sha }}` | Full commit SHA |
| `${{ github.repository }}` | Repo name (e.g., `rahul/my-app`) |
| `${{ github.event_name }}` | Trigger type (push, pull_request) |
| `${{ github.run_number }}` | Incremental run number |

---

## Conditional Execution

```yaml
steps:
  # Only run on main branch
  - name: Deploy
    if: github.ref == 'refs/heads/main'
    run: echo "Deploying to production"

  # Only run on PRs
  - name: Comment on PR
    if: github.event_name == 'pull_request'
    run: echo "This is a PR"

  # Always run (even if previous steps fail)
  - name: Cleanup
    if: always()
    run: echo "Cleaning up..."

  # Only run if previous steps succeeded
  - name: Notify
    if: success()
    run: echo "All good!"

  # Only run if previous steps failed
  - name: Alert
    if: failure()
    run: echo "Something went wrong!"
```

---

## Complete Example — FastAPI CI Workflow

```yaml
# .github/workflows/ci.yml

name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Lint & Test
    runs-on: ubuntu-latest

    env:
      DATABASE_URL: sqlite+aiosqlite:///./test.db
      SECRET_KEY: test-secret-key

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint with ruff
        run: ruff check app/

      - name: Check formatting with black
        run: black --check app/

      - name: Run tests with coverage
        run: pytest --cov=app --cov-report=term-missing

      - name: Type check with mypy
        run: mypy app/
```

---

## Viewing Workflow Results

After pushing, go to your GitHub repository:

1. Click the **Actions** tab
2. Click on the workflow run
3. See each job and step — green (passed) or red (failed)
4. Click on a failed step to see the error message

You can also see status directly on PRs — a green check or red X appears next to the commit.

---

## Practice Exercise

1. Create `.github/workflows/ci.yml` in your project
2. Add a simple workflow that runs on push to main
3. Include steps: checkout, set up Python, install deps, run pytest
4. Push to GitHub and check the Actions tab
5. Make a test fail intentionally and see the red X

---

*Next Topic: Jobs, Runners, and Matrix Builds — running tests across multiple Python versions.*
