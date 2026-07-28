# Cheat Sheet — Git, GitHub & Professional Workflow

**Module 05 | Quick Reference Card**

---

## Git Setup

```bash
git config --global user.name "Your Name"
git config --global user.email "you@email.com"
git config --global init.defaultBranch main
```

## Basic Workflow

```bash
git init                          # Start tracking
git clone <url>                   # Download a repo
git status                        # Check what changed
git diff                          # See line changes
git add <file>                    # Stage a file
git add .                         # Stage all files
git commit -m "message"           # Save snapshot
git push                          # Upload to GitHub
git pull                          # Download from GitHub
git log --oneline                 # View history
```

## Branching

```bash
git branch                        # List branches
git branch <name>                 # Create branch
git checkout <name>               # Switch branch
git checkout -b <name>            # Create + switch
git merge <name>                  # Merge into current
git branch -d <name>              # Delete merged branch
git branch -D <name>              # Force delete branch
```

## Stash

```bash
git stash                         # Save work temporarily
git stash push -m "description"   # Save with message
git stash list                    # See all stashes
git stash pop                     # Restore + remove
git stash apply                   # Restore, keep stash
git stash drop stash@{0}          # Delete a stash
```

## Undoing Things

```bash
git restore <file>                # Discard changes (CAREFUL!)
git restore --staged <file>       # Unstage a file
git commit --amend -m "new msg"   # Fix last commit message
git revert <hash>                 # Undo a commit safely
git rebase main                   # Replay on top of main
git cherry-pick <hash>            # Copy one commit
```

## Remote

```bash
git remote add origin <url>       # Connect to GitHub
git remote -v                     # View remotes
git push -u origin main           # First push
git push origin --delete <branch> # Delete remote branch
git fetch upstream                # Get upstream changes
```

## Branch Naming

| Pattern | Use |
|---------|-----|
| `feature/name` | New feature |
| `fix/name` | Bug fix |
| `hotfix/name` | Urgent fix |
| `refactor/name` | Code cleanup |
| `docs/name` | Documentation |

## Merge Conflict Resolution

```bash
# 1. Git marks conflicts in the file:
<<<<<<< HEAD
your version
=======
their version
>>>>>>> branch-name

# 2. Edit file — choose correct version
# 3. Remove conflict markers
# 4. Stage and commit:
git add <file>
git commit -m "Resolve merge conflict"
```

## Conventional Commits

```
feat(scope): add new feature
fix(scope): fix a bug
docs(scope): update docs
style(scope): formatting only
refactor(scope): restructure code
test(scope): add tests
chore(scope): maintenance
ci(scope): CI/CD changes
```

## .gitignore (Python)

```gitignore
__pycache__/
*.pyc
venv/
.env
.env.local
.vscode/
.idea/
*.db
node_modules/
dist/
```

## Pre-Commit Setup

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
pre-commit autoupdate
```

## .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: detect-private-key
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Python Tools

```bash
ruff check app/              # Lint
ruff check app/ --fix        # Auto-fix
black app/                   # Format
isort app/                   # Sort imports
```

## GitHub Actions (Minimal)

```yaml
# .github/workflows/tests.yml
name: Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

## GitHub Actions Keywords

| Keyword | Meaning |
|---------|---------|
| `on:` | Event triggers |
| `jobs:` | Groups of steps |
| `runs-on:` | Machine type |
| `steps:` | Individual tasks |
| `uses:` | Community action |
| `run:` | Shell command |
| `needs:` | Job dependency |
| `env:` | Environment variables |
| `secrets.*` | Encrypted secrets |
| `matrix:` | Multiple versions |

## Pull Request Template

```markdown
## Summary
- What this PR does

## Changes
- Files changed and why

## How to Test
1. Steps to verify

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] No console.log or print statements
```

## README Sections

1. Title + Description
2. Badges
3. Screenshots
4. Features
5. Tech Stack
6. Getting Started / Installation
7. Environment Variables
8. API Docs
9. Project Structure
10. Contributing
11. License

---

*TechPath Institute — Python Full Stack Development*
