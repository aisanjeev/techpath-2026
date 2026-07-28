# Jobs, Runners & Matrix Builds

**Module 14 — CI/CD with GitHub Actions | Topic 3**

---

## Understanding Jobs

A **job** is a set of steps that run on the same virtual machine (runner). Think of each job as a separate worker — it gets a fresh, clean machine with nothing installed.

### Key Properties of Jobs

| Property | What It Means |
|----------|--------------|
| Fresh environment | Each job starts with a clean machine — nothing from other jobs |
| Parallel by default | Multiple jobs run at the same time |
| Can depend on other jobs | Use `needs` to run sequentially |
| Can have conditions | Use `if` to skip jobs |
| Runs on a runner | You choose the OS (Ubuntu, Windows, macOS) |

### Multiple Jobs — Parallel

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff && ruff check .

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pytest && pytest

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install safety && safety check
```

All three jobs start at the same time on three separate machines. The workflow finishes when all three are done.

### Sequential Jobs with `needs`

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .

  test:
    runs-on: ubuntu-latest
    needs: lint              # Waits for lint to pass
    steps:
      - uses: actions/checkout@v4
      - run: pytest

  build:
    runs-on: ubuntu-latest
    needs: test              # Waits for test to pass
    steps:
      - run: docker build -t my-app .

  deploy:
    runs-on: ubuntu-latest
    needs: build             # Waits for build to pass
    if: github.ref == 'refs/heads/main'
    steps:
      - run: echo "Deploying..."
```

```
lint → test → build → deploy
```

### Fan-Out and Fan-In

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  unit-tests:
    runs-on: ubuntu-latest
    needs: lint
    steps: [...]

  integration-tests:
    runs-on: ubuntu-latest
    needs: lint
    steps: [...]

  deploy:
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]    # Wait for BOTH
    steps: [...]
```

```
         lint
        /    \
unit-tests  integration-tests
        \    /
        deploy
```

---

## Runners

A **runner** is the virtual machine that executes your job. GitHub provides free hosted runners.

### Available Runners

| Runner | OS | CPU | RAM | Disk |
|--------|----|-----|-----|------|
| `ubuntu-latest` | Ubuntu 22.04 | 2 cores | 7 GB | 14 GB |
| `ubuntu-24.04` | Ubuntu 24.04 | 2 cores | 7 GB | 14 GB |
| `windows-latest` | Windows Server 2022 | 2 cores | 7 GB | 14 GB |
| `macos-latest` | macOS 14 (Sonoma) | 3 cores | 14 GB | 14 GB |

### Which Runner to Use?

| Your App | Use Runner |
|----------|-----------|
| Python web app (FastAPI, Django) | `ubuntu-latest` |
| Cross-platform Python library | Matrix with all three |
| Node.js / Frontend | `ubuntu-latest` |
| Windows-specific | `windows-latest` |

**For 99% of Python web projects, use `ubuntu-latest`.** It is the fastest and uses the least free-tier minutes.

### Free Tier Limits

| Runner OS | Minutes per Month (Free) | Minute Multiplier |
|-----------|--------------------------|-------------------|
| Ubuntu | 2000 | 1x |
| Windows | 2000 | 2x (uses 2 min per 1 min) |
| macOS | 2000 | 10x (uses 10 min per 1 min) |

> **Tip:** A typical Python CI run takes 2-5 minutes. At 2000 free minutes/month on Ubuntu, you can run 400-1000 CI runs per month — more than enough for most projects.

---

## Matrix Builds

A **matrix build** runs the same job with different configurations — like different Python versions, operating systems, or database backends.

> **Analogy:** Imagine testing a recipe in different kitchens — a gas stove, an induction stove, and an OTG oven. The recipe is the same, but you want to make sure it works everywhere. That is what matrix builds do for code.

### Testing Multiple Python Versions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

This creates **3 parallel jobs** — one for each Python version. GitHub shows them as:

```
test (3.10) ✓
test (3.11) ✓
test (3.12) ✗  ← Found a bug on 3.12!
```

### Multi-Dimensional Matrix

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.11', '3.12']
        database: [sqlite, postgres]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pytest
        env:
          DATABASE: ${{ matrix.database }}
```

This creates **2 x 2 x 2 = 8 jobs**:

| OS | Python | Database |
|----|--------|----------|
| Ubuntu | 3.11 | SQLite |
| Ubuntu | 3.11 | PostgreSQL |
| Ubuntu | 3.12 | SQLite |
| Ubuntu | 3.12 | PostgreSQL |
| Windows | 3.11 | SQLite |
| Windows | 3.11 | PostgreSQL |
| Windows | 3.12 | SQLite |
| Windows | 3.12 | PostgreSQL |

> **Warning:** Matrix builds can use up free minutes quickly. 8 jobs x 3 minutes each = 24 minutes per push. Use matrix builds wisely.

### Excluding Specific Combinations

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.11', '3.12']
    exclude:
      - os: windows-latest
        python-version: '3.11'     # Skip Python 3.11 on Windows
```

### Including Extra Combinations

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12']
    include:
      - python-version: '3.12'
        experimental: true          # Add an extra variable for 3.12
```

### Fail-Fast

```yaml
strategy:
  fail-fast: false    # Don't cancel other jobs when one fails
  matrix:
    python-version: ['3.10', '3.11', '3.12']
```

By default, `fail-fast` is `true` — if one matrix job fails, all others are cancelled. Set it to `false` if you want to see results for all combinations.

---

## Sharing Data Between Jobs

Since each job runs on a fresh machine, you need special mechanisms to share data.

### Artifacts — Sharing Files

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest --cov=app --cov-report=html

      # Upload test coverage report
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/

  review:
    runs-on: ubuntu-latest
    needs: build
    steps:
      # Download the coverage report from the build job
      - uses: actions/download-artifact@v4
        with:
          name: coverage-report
          path: coverage/

      - run: ls coverage/
```

### Outputs — Sharing Small Values

```yaml
jobs:
  version:
    runs-on: ubuntu-latest
    outputs:
      app-version: ${{ steps.get-version.outputs.version }}
    steps:
      - id: get-version
        run: echo "version=1.2.3" >> $GITHUB_OUTPUT

  deploy:
    needs: version
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying version ${{ needs.version.outputs.app-version }}"
```

---

## Job Permissions

Control what your workflow can access:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read        # Read repo code
      packages: write       # Push to GHCR
      id-token: write       # OIDC for cloud deployments
```

---

## Practical Example — Complete Multi-Job Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install ruff black
      - run: ruff check app/
      - run: black --check app/

  test:
    name: Tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app
        env:
          DATABASE_URL: sqlite+aiosqlite:///./test.db

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t my-app .
      - run: echo "Image built successfully"
```

---

## Practice Exercise

1. Create a workflow with two parallel jobs: lint and test
2. Add a third job (build) that depends on both
3. Add a matrix build to test Python 3.11 and 3.12
4. Add a condition so the build job only runs on the main branch
5. Push and watch all jobs in the Actions tab

---

*Next Topic: Building a Test Pipeline — install, lint, test, and coverage.*
