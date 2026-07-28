# Pre-Commit Hooks — Automated Code Quality

**Module 05 — Git, GitHub & Professional Workflow | Topic 5**

---

## What are Git Hooks?

Git hooks are scripts that run automatically before or after certain Git events (like commit, push, merge). They act as **quality gates** — catching problems before they enter your codebase.

**Real-world analogy:** Think of airport security. Before you board the plane (commit), your bag goes through a scanner (pre-commit hook). If something is not allowed, you fix it before boarding. No one gets on the plane with a problem.

### Types of Hooks

| Hook | When It Runs | Use Case |
|------|-------------|----------|
| `pre-commit` | Before a commit is created | Lint, format, check for secrets |
| `commit-msg` | After you write the commit message | Enforce message format |
| `pre-push` | Before a push to remote | Run tests |
| `post-merge` | After a merge completes | Install new dependencies |

We focus on **pre-commit** hooks — the most useful for daily development.

---

## The Pre-Commit Framework

`pre-commit` is a Python tool that manages and runs hooks automatically.

### Installation

```bash
pip install pre-commit

# Verify
pre-commit --version
# pre-commit 3.7.0
```

### Setup

Create a file named `.pre-commit-config.yaml` in your project root:

```yaml
# .pre-commit-config.yaml
repos:
  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace       # Remove trailing spaces
      - id: end-of-file-fixer         # Ensure files end with newline
      - id: check-yaml                # Validate YAML files
      - id: check-json                # Validate JSON files
      - id: check-added-large-files   # Prevent large files (> 500KB)
      - id: check-merge-conflict      # Check for merge conflict markers
      - id: detect-private-key        # Prevent committing private keys

  # Python formatter
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black
        language_version: python3.12

  # Python linter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.8
    hooks:
      - id: ruff
        args: [--fix]                  # Auto-fix what it can
      - id: ruff-format               # Ruff's built-in formatter

  # Import sorter
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]   # Make isort compatible with black
```

### Installing the Hooks

```bash
# Install hooks into your .git directory
pre-commit install

# Output: pre-commit installed at .git/hooks/pre-commit
```

Now, every time you run `git commit`, these hooks run automatically.

### Running Hooks Manually

```bash
# Run on all files (useful for first-time setup)
pre-commit run --all-files

# Run a specific hook
pre-commit run black --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

---

## Python Code Quality Tools

### Ruff — The Fast Python Linter

Ruff checks your Python code for errors, style issues, and potential bugs. It is extremely fast (written in Rust).

```bash
# Install
pip install ruff

# Check for issues
ruff check app/

# Auto-fix issues
ruff check app/ --fix

# Format code (like Black)
ruff format app/
```

**What Ruff catches:**

```python
# BAD: Unused import (F401)
import os  # You never use 'os' in this file

# BAD: Undefined variable (F821)
print(user_name)  # Variable 'user_name' was never defined

# BAD: Comparison to None (E711)
if user == None:  # Should be: if user is None

# BAD: Mutable default argument (B006)
def add_item(items=[]):  # Should be: items=None
```

**Ruff configuration in `pyproject.toml`:**

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "UP",   # pyupgrade
]
ignore = ["E501"]  # Ignore line-too-long (handled by formatter)
```

### Black — The Python Formatter

Black formats your Python code automatically. It is "opinionated" — there is only one correct style, so your entire team writes code that looks the same.

```bash
# Install
pip install black

# Format a file
black app.py

# Format entire directory
black app/

# Check without changing (useful in CI)
black app/ --check
```

**Before Black:**

```python
x = {  'a':37,'b':42,
'c':927}
y = 'hello ''world'
z = 'hello '+'world'
if very_long_variable_name is not None and another_variable is not None and yet_another is not None:
    do_something()
```

**After Black:**

```python
x = {"a": 37, "b": 42, "c": 927}
y = "hello " "world"
z = "hello " + "world"
if (
    very_long_variable_name is not None
    and another_variable is not None
    and yet_another is not None
):
    do_something()
```

### isort — Import Sorter

isort organizes your Python imports into the correct order.

```bash
pip install isort
isort app/
```

**Before isort:**

```python
from app.models import Student
import os
from datetime import datetime
import json
from fastapi import FastAPI
from sqlalchemy import select
import sys
```

**After isort:**

```python
import json
import os
import sys
from datetime import datetime

from fastapi import FastAPI
from sqlalchemy import select

from app.models import Student
```

**Order:** Standard library > Third-party packages > Local imports. Alphabetical within each group.

---

## Commit Message Conventions

Good commit messages help your team understand the project history.

### Conventional Commits Format

```
<type>(<scope>): <short description>

<optional body>
```

**Types:**

| Type | Use For | Example |
|------|---------|---------|
| `feat` | New feature | `feat(auth): add Google OAuth login` |
| `fix` | Bug fix | `fix(api): handle empty email in registration` |
| `docs` | Documentation | `docs(readme): add setup instructions` |
| `style` | Formatting, no logic change | `style: format with black` |
| `refactor` | Code restructuring | `refactor(db): simplify query builder` |
| `test` | Adding or fixing tests | `test(auth): add JWT expiry tests` |
| `chore` | Maintenance tasks | `chore: update dependencies` |
| `ci` | CI/CD changes | `ci: add Python 3.12 to test matrix` |

### Enforcing Commit Messages with commitlint

Add to `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.2.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [feat, fix, docs, style, refactor, test, chore, ci]
```

Install the commit-msg hook:

```bash
pre-commit install --hook-type commit-msg
```

Now Git will reject messages like `"update"` or `"fix stuff"` and require proper format.

---

## Complete Project Setup

Here is a full setup for a Python project with all quality tools:

### pyproject.toml

```toml
[tool.black]
line-length = 100
target-version = ["py312"]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "SIM", "UP"]
ignore = ["E501"]

[tool.isort]
profile = "black"
line_length = 100
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.2.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

### First-Time Team Setup

```bash
# After cloning the repository:
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit run --all-files   # Fix any existing issues
```

---

## What Happens When You Commit

```bash
git add .
git commit -m "feat(auth): add login page"

# Pre-commit hooks run automatically:
# check-yaml...........................................................Passed
# check-json...........................................................Passed
# trailing-whitespace..................................................Fixed
# end-of-file-fixer....................................................Passed
# detect-private-key...................................................Passed
# ruff.................................................................Passed
# ruff-format..........................................................Passed
# black................................................................Passed
# conventional-pre-commit..............................................Passed
```

If any hook fails, the commit is blocked. Fix the issue, re-stage, and commit again.

---

## Summary

| Tool | Purpose |
|------|---------|
| `pre-commit` | Framework for running Git hooks |
| `ruff` | Fast Python linter (finds errors) |
| `black` | Python code formatter (consistent style) |
| `isort` | Import sorter (clean imports) |
| Conventional Commits | Standard format for commit messages |
| `.pre-commit-config.yaml` | Configuration file listing all hooks |

---

*TechPath Institute — Python Full Stack Development*
