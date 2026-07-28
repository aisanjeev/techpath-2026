# Building a Test Pipeline

**Module 14 — CI/CD with GitHub Actions | Topic 4**

---

## The Test Pipeline

A test pipeline is the most important part of CI/CD. Every time someone pushes code, this pipeline automatically checks:

1. Are dependencies installed correctly?
2. Does the code follow style rules? (linting)
3. Do all tests pass?
4. How much code is covered by tests?

If any step fails, the developer is notified immediately.

---

## Step 1: Install Dependencies

### Using pip

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.12'
      cache: 'pip'              # Cache pip packages between runs

  - name: Install dependencies
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
```

### Using Poetry

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.12'

  - name: Install Poetry
    run: pip install poetry

  - name: Configure Poetry
    run: poetry config virtualenvs.create false

  - name: Install dependencies
    run: poetry install --no-interaction
```

### Why Caching Matters

Without caching, every CI run downloads all packages from scratch. With `cache: 'pip'`, downloaded packages are stored and reused.

| Without Cache | With Cache |
|--------------|------------|
| Install: 45 seconds | Install: 5 seconds |
| Downloads every time | Reuses cached packages |
| Uses more bandwidth | Faster builds |

---

## Step 2: Linting with Ruff

**Ruff** is a fast Python linter written in Rust. It catches code quality issues.

```yaml
  - name: Lint with ruff
    run: ruff check app/ tests/
```

### What Ruff Catches

| Rule | Example |
|------|---------|
| Unused imports | `import os` (but os is never used) |
| Undefined names | Using a variable before defining it |
| Style violations | Wrong indentation, line too long |
| Common bugs | `except:` without exception type |
| Security issues | Using `eval()` on user input |

### Ruff Configuration

Add to `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I"]   # Error, pyflakes, warning, isort
ignore = ["E501"]                 # Ignore line length (optional)

[tool.ruff.lint.isort]
known-first-party = ["app"]
```

### Formatting Check with Black

```yaml
  - name: Check formatting
    run: black --check app/ tests/
```

`black --check` does not modify files — it only reports if formatting is wrong. The developer must run `black app/` locally to fix it.

---

## Step 3: Running Tests with Pytest

```yaml
  - name: Run tests
    run: pytest tests/ -v
    env:
      DATABASE_URL: sqlite+aiosqlite:///./test.db
      SECRET_KEY: test-secret-key-for-ci
```

### Pytest Options for CI

| Flag | Purpose |
|------|---------|
| `-v` | Verbose — show test names |
| `-x` | Stop on first failure |
| `--tb=short` | Short tracebacks |
| `-q` | Quiet — minimal output |
| `--timeout=30` | Fail tests that take > 30 seconds |
| `-n auto` | Run tests in parallel (needs pytest-xdist) |

### Using a Test Database

For CI, you typically use SQLite (no setup needed):

```yaml
env:
  DATABASE_URL: sqlite+aiosqlite:///./test.db
```

For integration tests that need PostgreSQL:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      DATABASE_URL: postgresql+asyncpg://testuser:testpass@localhost:5432/testdb

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

The `services` section spins up a PostgreSQL container alongside your tests.

---

## Step 4: Code Coverage

Coverage measures what percentage of your code is tested.

```yaml
  - name: Run tests with coverage
    run: |
      pip install pytest-cov
      pytest --cov=app --cov-report=term-missing --cov-report=html
```

### Understanding Coverage Output

```
---------- coverage: platform linux, python 3.12.4 ----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/__init__.py             2      0   100%
app/main.py                45      3    93%   67-69
app/models.py              30      0   100%
app/routes.py              60     12    80%   45-50, 78-83
-----------------------------------------------------
TOTAL                     137     15    89%
```

| Column | Meaning |
|--------|---------|
| Stmts | Total lines of code |
| Miss | Lines not covered by any test |
| Cover | Percentage covered |
| Missing | Specific uncovered line numbers |

### Enforcing Minimum Coverage

```yaml
  - name: Check coverage threshold
    run: pytest --cov=app --cov-fail-under=80
```

This fails the CI if coverage drops below 80%.

### Uploading Coverage Report

```yaml
  - name: Run tests with coverage
    run: pytest --cov=app --cov-report=html

  - name: Upload coverage report
    uses: actions/upload-artifact@v4
    if: always()
    with:
      name: coverage-report
      path: htmlcov/
      retention-days: 7
```

The HTML report is downloadable from the Actions run page.

---

## Step 5: Type Checking with Mypy (Optional)

```yaml
  - name: Type check
    run: mypy app/ --ignore-missing-imports
```

Mypy checks that your type annotations are correct:

```python
# This passes mypy
def add(a: int, b: int) -> int:
    return a + b

# This fails mypy — returning str instead of int
def add(a: int, b: int) -> int:
    return str(a + b)    # Error: Incompatible return value type
```

---

## Complete Test Pipeline

Putting it all together:

```yaml
# .github/workflows/ci.yml

name: CI — Lint, Test & Coverage

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    name: Code Quality & Tests
    runs-on: ubuntu-latest

    env:
      DATABASE_URL: sqlite+aiosqlite:///./test.db
      SECRET_KEY: ci-test-secret-key
      PYTHONDONTWRITEBYTECODE: 1

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
          pip install ruff black pytest-cov mypy

      - name: Lint with ruff
        run: ruff check app/

      - name: Check formatting with black
        run: black --check app/ tests/

      - name: Run tests with coverage
        run: |
          pytest tests/ \
            --cov=app \
            --cov-report=term-missing \
            --cov-report=html \
            --cov-fail-under=70 \
            -v

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-report
          path: htmlcov/
          retention-days: 7

      - name: Type check with mypy
        run: mypy app/ --ignore-missing-imports
        continue-on-error: true    # Don't fail the pipeline for type errors (yet)
```

### What `continue-on-error: true` Does

For steps that you want to monitor but not block on (like mypy when first introducing types), `continue-on-error: true` lets the step fail without failing the whole workflow.

---

## Common Pipeline Failures and Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError` | Missing dependency | Add package to `requirements.txt` |
| Ruff errors | Code style violation | Run `ruff check --fix app/` locally |
| Black formatting | Code not formatted | Run `black app/` locally |
| Test failures | Bug in code or test | Debug locally with `pytest -x -v` |
| Coverage below threshold | Not enough tests | Write more tests |
| Import errors | Circular imports, wrong paths | Fix import structure |

---

## Practice Exercise

1. Create a `ci.yml` workflow with all 4 steps (install, lint, test, coverage)
2. Push code with a lint error — see the pipeline fail
3. Fix the error and push again — see it pass
4. Add `--cov-fail-under=50` and see if your coverage meets the bar
5. Download the HTML coverage report from the Actions artifacts

---

*Next Topic: Docker Build & Push — building and pushing Docker images in CI.*
