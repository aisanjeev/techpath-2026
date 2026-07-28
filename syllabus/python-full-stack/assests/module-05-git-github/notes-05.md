# Module 05: Git, GitHub & Professional Workflow

## 1. Introduction to Version Control

### What is Version Control?

Version control is a system that tracks changes to files over time. Think of it like a **save system in a video game** — you can go back to any previous save point if something goes wrong.

**Without version control:**
- `project_final.py`
- `project_final_v2.py`
- `project_final_v2_actually_final.py`
- `project_DONT_DELETE_THIS.py`

**With version control (Git):**
- One folder, one project, full history tracked automatically.

### Why Git?

| Feature | Without Git | With Git |
|---------|------------|----------|
| Track changes | Manual copies | Automatic |
| Collaborate | Email files back and forth | Everyone works on same repo |
| Undo mistakes | Hope you have a backup | `git revert` anytime |
| Work on features | Edit main code directly | Use branches safely |
| Know who changed what | Ask everyone | `git log` and `git blame` |

Git is the most widely used version control system in the world. Created by Linus Torvalds (the creator of Linux) in 2005.

---

## 2. Git Setup & Configuration

### Installing Git

**Windows:**
1. Download from [git-scm.com](https://git-scm.com/downloads)
2. Run the installer (keep default options)
3. Verify in terminal:
```bash
git --version
# git version 2.45.0.windows.1
```

**Configure your identity** (do this once after installing):
```bash
git config --global user.name "Rahul Sharma"
git config --global user.email "rahul@techpath.biz"

# Set default branch name to main
git config --global init.defaultBranch main

# Set VS Code as default editor
git config --global core.editor "code --wait"

# View all config
git config --list
```

---

## 3. Git Basics — The Core Workflow

### The Three Areas of Git

```
Working Directory  -->  Staging Area  -->  Repository
  (your files)         (ready to save)    (saved history)
      |                     |                   |
   git add            git commit           git log
```

Think of it like packing a courier:
1. **Working Directory** = Items on your desk
2. **Staging Area** = Items you put in the box
3. **Repository** = Box sealed and shipped (committed)

### Initializing a Repository

```bash
# Create a new project folder
mkdir techpath-portfolio
cd techpath-portfolio

# Initialize Git
git init
# Output: Initialized empty Git repository in .../techpath-portfolio/.git/
```

### Your First Commit

```bash
# Create a file
echo "# TechPath Portfolio" > README.md

# Check status — shows untracked file
git status

# Add file to staging area
git add README.md

# Commit with a message
git commit -m "feat: add project README"
```

### Essential Commands

| Command | What It Does | Example |
|---------|-------------|---------|
| `git init` | Start a new repo | `git init` |
| `git status` | Show current state | `git status` |
| `git add <file>` | Stage a file | `git add app.py` |
| `git add .` | Stage all changes | `git add .` |
| `git commit -m "msg"` | Save staged changes | `git commit -m "fix: login bug"` |
| `git log` | View commit history | `git log --oneline` |
| `git diff` | Show unstaged changes | `git diff` |
| `git diff --staged` | Show staged changes | `git diff --staged` |

### Practical Example — Tracking a Python Project

```bash
# Rahul is building a calculator app at TechPath Institute
mkdir calculator && cd calculator
git init

# Create the main file
cat > calculator.py << 'EOF'
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print("TechPath Calculator")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
EOF

# Stage and commit
git add calculator.py
git commit -m "feat: add basic calculator with add and subtract"

# Check log
git log --oneline
# a1b2c3d feat: add basic calculator with add and subtract
```

### Viewing History

```bash
# Compact log
git log --oneline

# Detailed log with changes
git log -p

# Log with graph (useful with branches)
git log --oneline --graph --all

# Show a specific commit
git show a1b2c3d

# Who changed each line? (blame)
git blame calculator.py
```

---

## 4. The .gitignore File

A `.gitignore` file tells Git which files to **not track**. This is critical for keeping secrets, build files, and OS junk out of your repo.

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# Environment files (contain secrets!)
.env
.env.local
.env.production

# IDE files
.vscode/
.idea/
.cursor/

# OS files
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite3

# Logs
*.log
EOF

git add .gitignore
git commit -m "chore: add .gitignore for Python project"
```

**Important:** If you accidentally committed a secret file before adding `.gitignore`:
```bash
# Remove from tracking (keeps the local file)
git rm --cached .env
git commit -m "chore: remove .env from tracking"
```

---

## 5. Branching

### What are Branches?

Branches let you work on features independently without affecting the main code. Think of it like making a photocopy of your notebook — you can experiment on the copy, and if it works out, paste it back into the original.

```
main:     A --- B --- C
                 \
feature:          D --- E
```

### Creating and Switching Branches

```bash
# See current branch
git branch
# * main

# Create a new branch
git branch feature/add-multiply

# Switch to it
git switch feature/add-multiply
# or (older way): git checkout feature/add-multiply

# Create and switch in one command
git switch -c feature/add-divide
# or: git checkout -b feature/add-divide
```

### Branch Naming Conventions

| Prefix | Use For | Example |
|--------|---------|---------|
| `feature/` | New features | `feature/user-login` |
| `fix/` | Bug fixes | `fix/calculator-error` |
| `docs/` | Documentation | `docs/update-readme` |
| `refactor/` | Code cleanup | `refactor/split-modules` |
| `test/` | Adding tests | `test/calculator-tests` |

### Practical Example — Feature Branch Workflow

```bash
# Priya is adding a multiply function
git switch -c feature/add-multiply

# Edit calculator.py — add multiply function
cat >> calculator.py << 'EOF'

def multiply(a, b):
    return a * b
EOF

git add calculator.py
git commit -m "feat: add multiply function"

# Switch back to main
git switch main

# The multiply function is NOT here — it's only on the feature branch
cat calculator.py
```

### Merging Branches

Once a feature is complete, merge it back into `main`.

```bash
# Make sure you're on main
git switch main

# Merge the feature branch
git merge feature/add-multiply
# Output: Fast-forward merge

# Delete the merged branch (cleanup)
git branch -d feature/add-multiply
```

### Types of Merges

**Fast-Forward Merge** — When `main` hasn't changed since the branch was created:
```
Before:  main: A --- B
                      \
         feat:         C --- D

After:   main: A --- B --- C --- D
```

**Three-Way Merge** — When both branches have new commits:
```
Before:  main: A --- B --- E
                      \
         feat:         C --- D

After:   main: A --- B --- E --- M  (M = merge commit)
                      \         /
         feat:         C --- D
```

### Handling Merge Conflicts

When two branches change the **same line** in the same file, Git cannot auto-merge. You must resolve it manually.

```bash
# Amit and Sneha both edit line 1 of greeting.py
# Amit's branch: message = "Hello from Bhopal!"
# Sneha's branch: message = "Hello from Pune!"

# When merging, Git shows:
<<<<<<< HEAD
message = "Hello from Bhopal!"
=======
message = "Hello from Pune!"
>>>>>>> feature/sneha-greeting

# Fix it by choosing one (or combining):
message = "Hello from TechPath Institute, Bhopal!"

# Then:
git add greeting.py
git commit -m "fix: resolve greeting merge conflict"
```

**Tips for avoiding conflicts:**
- Pull latest changes before starting work
- Keep branches short-lived
- Communicate with your team about which files you are editing

### Git Stash

Save your work temporarily without committing (like putting papers in a drawer):

```bash
# You're working on something but need to switch branches urgently
git stash
# Your changes are saved, working directory is clean

# Switch branch, do your work, come back
git switch main
# ... do something ...
git switch feature/my-work

# Get your stashed changes back
git stash pop

# List all stashes
git stash list

# Apply a specific stash without removing it
git stash apply stash@{0}
```

### Rebase (Advanced)

Rebase moves your branch's commits on top of another branch, creating a linear history:

```bash
# Instead of merge (which creates merge commits):
git switch feature/add-divide
git rebase main

# Your branch now starts from the latest main commit
```

```
Before rebase:
main: A --- B --- E
             \
feat:         C --- D

After rebase:
main: A --- B --- E
                    \
feat:                C' --- D'
```

**Golden rule:** Never rebase commits that have been pushed and shared with others.

### Cherry-Pick

Pick a specific commit from another branch:

```bash
# Get commit hash from log
git log --oneline feature/experiment
# x1y2z3 feat: add useful helper function

# Apply just that one commit to current branch
git cherry-pick x1y2z3
```

---

## 6. Remote Repositories & GitHub

### What is GitHub?

GitHub is a platform that hosts Git repositories online. It adds collaboration features like pull requests, issues, and project boards.

```
Local Repo (your laptop)  <--->  Remote Repo (GitHub)
     git push -->                    <-- git pull
```

### Creating a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click **"+"** → **"New repository"**
3. Name it (e.g., `techpath-calculator`)
4. Choose **Public** or **Private**
5. Do NOT initialize with README (we already have one locally)
6. Click **Create repository**

### Connecting Local to Remote

```bash
# Add remote (copy URL from GitHub)
git remote add origin https://github.com/rahul-sharma/techpath-calculator.git

# Push your code
git push -u origin main
# -u sets upstream so future pushes just need: git push
```

### Push, Pull, and Fetch

```bash
# Push local changes to GitHub
git push

# Pull remote changes to your local (fetch + merge)
git pull

# Fetch changes without merging (just download)
git fetch
git log origin/main  # See what changed

# Push a new branch to GitHub
git push -u origin feature/add-divide
```

### Fork vs Clone

| Action | What It Does | When to Use |
|--------|-------------|-------------|
| **Clone** | Copy a repo to your computer | Your own project or team project |
| **Fork** | Copy someone else's repo to YOUR GitHub | Contributing to open source |

```bash
# Clone
git clone https://github.com/techpath/sample-project.git

# Fork: Click "Fork" button on GitHub, then clone YOUR fork
git clone https://github.com/your-username/sample-project.git
```

---

## 7. Pull Requests (PRs)

A Pull Request is a way to propose changes. It says: "I made changes on my branch, please review and merge them into main."

### Creating a Pull Request

1. Push your feature branch to GitHub:
```bash
git push -u origin feature/add-multiply
```

2. Go to GitHub → your repository
3. Click **"Compare & pull request"** (yellow banner)
4. Fill in:
   - **Title:** `feat: add multiply function to calculator`
   - **Description:** What you changed and why
5. Click **"Create pull request"**

### PR Description Template

```markdown
## What does this PR do?
Adds a multiply function to the calculator module.

## Changes
- Added `multiply(a, b)` function in `calculator.py`
- Added tests in `test_calculator.py`

## How to Test
1. Run `python calculator.py`
2. Run `pytest test_calculator.py`

## Screenshots
(if applicable)
```

### Code Review Best Practices

**As a reviewer:**
- Be kind and constructive
- Ask questions instead of demanding ("Could we use a list comprehension here?" vs "Use a list comprehension")
- Approve only when code is correct AND readable
- Test the branch locally if needed

**As a PR author:**
- Keep PRs small (under 300 lines ideally)
- Write a clear description
- Respond to all review comments
- Don't take feedback personally — it's about the code, not you

### Merging a Pull Request

On GitHub:
1. After approval, click **"Merge pull request"**
2. Choose merge strategy:
   - **Create a merge commit** (default, keeps full history)
   - **Squash and merge** (combines all commits into one)
   - **Rebase and merge** (linear history)
3. Delete the branch after merging (cleanup)

---

## 8. GitHub Issues & Projects

### Issues

Issues are tasks, bug reports, or feature requests. They're like a to-do list for your project.

**Creating an Issue:**
1. Go to your repo → **Issues** → **New Issue**
2. Write a clear title: `Bug: calculator crashes on division by zero`
3. Add description, labels, and assign someone

**Common Labels:**
| Label | Meaning |
|-------|---------|
| `bug` | Something is broken |
| `enhancement` | New feature request |
| `documentation` | Docs need updating |
| `good first issue` | Easy for beginners |
| `help wanted` | Extra attention needed |

**Linking Issues to PRs:**
In your PR description, write `Closes #5` — when the PR is merged, issue #5 auto-closes.

### GitHub Projects (Kanban Boards)

GitHub Projects let you organize issues visually on a board:

```
| To Do          | In Progress     | Review          | Done            |
|----------------|-----------------|-----------------|-----------------|
| #1 Add login   | #3 Fix bug      | #5 Add tests    | #2 Setup repo   |
| #4 Add search  |                 |                 | #6 Add README   |
```

**Setting up a Project:**
1. Go to your repo → **Projects** → **New Project**
2. Choose **Board** view (Kanban)
3. Add columns: To Do, In Progress, Review, Done
4. Add issues to the board
5. Drag issues between columns as work progresses

**Milestones:**
Group related issues into milestones (e.g., "v1.0 Release"):
1. Go to **Issues** → **Milestones** → **New Milestone**
2. Set a due date
3. Add issues to the milestone
4. Track progress as a percentage

---

## 9. Conventional Commits

### What are Conventional Commits?

A standard format for commit messages that makes history readable and enables automation.

### Format

```
<type>(<optional scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | When to Use | Example |
|------|------------|---------|
| `feat` | New feature | `feat: add search functionality` |
| `fix` | Bug fix | `fix: resolve login timeout` |
| `docs` | Documentation only | `docs: update installation guide` |
| `style` | Formatting (no logic change) | `style: fix indentation in models.py` |
| `refactor` | Code restructure (no feature/fix) | `refactor: split utils into modules` |
| `test` | Adding or fixing tests | `test: add unit tests for calculator` |
| `chore` | Maintenance tasks | `chore: update dependencies` |

### Examples

```bash
# Good commit messages
git commit -m "feat: add student registration endpoint"
git commit -m "fix: prevent division by zero in calculator"
git commit -m "docs: add API usage examples to README"
git commit -m "refactor: extract validation into separate module"
git commit -m "test: add edge case tests for grade calculator"
git commit -m "chore: upgrade FastAPI to 0.111.0"

# Bad commit messages
git commit -m "fixed stuff"          # What stuff?
git commit -m "update"               # Update what?
git commit -m "asdfgh"               # Meaningless
git commit -m "changes"              # Not helpful
```

### Why Conventional Commits Matter

1. **Readable history** — `git log --oneline` tells a story
2. **Auto-changelogs** — tools can generate changelogs from commits
3. **Semantic versioning** — `feat` = minor bump, `fix` = patch bump
4. **Team alignment** — everyone writes messages the same way

---

## 10. Pre-commit Hooks

### What are Git Hooks?

Git hooks are scripts that run automatically at certain points in the Git workflow. **Pre-commit hooks** run before every commit — they check your code quality.

```
You run: git commit -m "feat: add login"
                |
        Pre-commit hooks run:
        [1] ruff (linting)      --> PASS
        [2] black (formatting)  --> FAIL! (unformatted code)
                |
        Commit is BLOCKED until you fix it
```

### Setting Up pre-commit

```bash
# Install the pre-commit framework
pip install pre-commit

# Create config file
cat > .pre-commit-config.yaml << 'EOF'
repos:
  # Ruff — fast Python linter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Black — code formatter
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  # isort — sort imports
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  # General checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
EOF

# Install the hooks
pre-commit install
# Output: pre-commit installed at .git/hooks/pre-commit

# Run on all files (first time)
pre-commit run --all-files
```

### What Each Tool Does

| Tool | Purpose | What It Catches |
|------|---------|-----------------|
| **ruff** | Linting (find errors) | Unused imports, undefined variables, bad practices |
| **black** | Code formatting | Inconsistent spacing, line length, quote style |
| **isort** | Import sorting | Unorganized imports |

### Example — Before and After

**Before (messy code):**
```python
import os
import sys
from collections import OrderedDict
import json
from pathlib import Path

def   calculate_fee( course_name,duration ):
    base_fee=15000
    if duration>6:
        discount=0.1
    else:
        discount=0
    return base_fee*duration*(1-discount)
```

**After pre-commit runs:**
```python
import json
import os
import sys
from collections import OrderedDict
from pathlib import Path


def calculate_fee(course_name, duration):
    base_fee = 15000
    if duration > 6:
        discount = 0.1
    else:
        discount = 0
    return base_fee * duration * (1 - discount)
```

### Ruff Configuration

Add a `ruff.toml` or section in `pyproject.toml`:

```toml
# ruff.toml
line-length = 88
target-version = "py311"

[lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[lint.isort]
known-first-party = ["app"]
```

---

## 11. Writing a Professional README

A README is the first thing people see when they visit your repository. A good README makes your project look professional and helps others understand and use your code.

### README Structure

```markdown
# Project Name

Short description (1-2 lines).

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features
- Feature 1
- Feature 2

## Tech Stack
- Python 3.11
- FastAPI
- SQLAlchemy

## Installation

### Prerequisites
- Python 3.11+
- pip

### Steps
\```bash
git clone https://github.com/username/project.git
cd project
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
\```

## Usage
\```bash
python main.py
\```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/students | List all students |
| POST | /api/students | Add a student |

## Project Structure
\```
project/
|-- app/
|   |-- main.py
|   |-- models.py
|   |-- routes.py
|-- tests/
|-- requirements.txt
|-- README.md
\```

## Contributing
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License
```

### Badges (shields.io)

Badges are small status images. Generate them at [shields.io](https://shields.io):

```markdown
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![Build](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml)
![License](https://img.shields.io/badge/license-MIT-green)
```

### Markdown Syntax Quick Reference

| Syntax | Output |
|--------|--------|
| `# Heading 1` | Large heading |
| `## Heading 2` | Medium heading |
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `` `code` `` | `code` |
| `[text](url)` | Hyperlink |
| `![alt](url)` | Image |
| `- item` | Bullet list |
| `1. item` | Numbered list |
| `> quote` | Blockquote |
| `---` | Horizontal line |

---

## 12. GitHub Actions — CI/CD

### What is CI/CD?

- **CI (Continuous Integration):** Automatically test and lint code every time someone pushes changes
- **CD (Continuous Deployment):** Automatically deploy code after tests pass

```
Developer pushes code
        |
  GitHub Actions triggers
        |
  [1] Install dependencies
  [2] Run linter (ruff)
  [3] Run formatter check (black)
  [4] Run tests (pytest)
        |
   All pass?
   /        \
 YES         NO
  |           |
 Merge     Block merge,
 allowed   show errors
```

### Your First Workflow

GitHub Actions uses YAML files stored in `.github/workflows/`.

```yaml
# .github/workflows/ci.yml

name: TechPath CI Pipeline

# When to run
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

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
          python-version: "3.11"

      # Step 3: Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Step 4: Lint with ruff
      - name: Lint with ruff
        run: ruff check .

      # Step 5: Check formatting with black
      - name: Check formatting
        run: black --check .

      # Step 6: Run tests
      - name: Run tests
        run: pytest -v
```

### Understanding the Workflow File

| Section | Meaning |
|---------|---------|
| `name` | Name shown in GitHub Actions tab |
| `on` | Trigger events (push, pull_request) |
| `jobs` | Groups of steps to run |
| `runs-on` | Machine type (ubuntu-latest) |
| `steps` | Individual commands to execute |
| `uses` | Pre-built action from marketplace |
| `run` | Shell command to execute |

### Workflow Triggers

```yaml
on:
  push:
    branches: [main, develop]    # Run on push to these branches
  pull_request:
    branches: [main]              # Run on PRs targeting main
  schedule:
    - cron: '0 9 * * 1'          # Every Monday at 9 AM
  workflow_dispatch:               # Manual trigger button
```

### Viewing Results

1. Push code → Go to your repo on GitHub
2. Click **"Actions"** tab
3. See your workflow runs — green check = pass, red X = fail
4. Click a run to see detailed logs for each step

---

## 13. Complete Workflow — Putting It All Together

Here is the complete professional workflow that Vikram follows at TechPath Institute:

### Step 1: Start a New Feature

```bash
# Always start from latest main
git switch main
git pull

# Create feature branch
git switch -c feature/student-registration
```

### Step 2: Write Code with Quality Tools

```bash
# Work on your code...
# Pre-commit hooks auto-check on every commit

git add app/routes/students.py app/models/student.py
git commit -m "feat: add student registration endpoint"
# Pre-commit runs: ruff, black, isort
# If something fails, fix it and commit again
```

### Step 3: Push and Create PR

```bash
git push -u origin feature/student-registration
# Go to GitHub, create Pull Request
# CI pipeline runs automatically
```

### Step 4: Code Review

- Teammate (Ananya) reviews the PR
- She leaves comments and suggestions
- Vikram makes changes, pushes again
- CI re-runs on new commits

### Step 5: Merge and Clean Up

```bash
# After approval, merge on GitHub (squash and merge)
# Delete the remote branch on GitHub

# Locally:
git switch main
git pull
git branch -d feature/student-registration
```

---

## 14. Common Git Problems and Solutions

| Problem | Solution |
|---------|----------|
| Committed to wrong branch | `git stash`, switch branch, `git stash pop` |
| Need to undo last commit (keep files) | `git reset --soft HEAD~1` |
| Need to undo last commit (discard files) | `git reset --hard HEAD~1` |
| Accidentally deleted a file | `git restore filename.py` |
| Want to see what changed | `git diff` (unstaged) or `git diff --staged` |
| Merge conflict | Open file, fix the `<<<<` markers, add and commit |
| Forgot to add a file to last commit | `git add file && git commit --amend` |
| Need to rename a branch | `git branch -m old-name new-name` |
| Want to undo a pushed commit safely | `git revert <commit-hash>` |

---

## 15. Git Cheat Sheet

```
SETUP
  git init                          Create new repo
  git clone <url>                   Copy remote repo

DAILY WORK
  git status                        Check current state
  git add <file>                    Stage file
  git add .                         Stage all changes
  git commit -m "message"           Commit staged changes
  git push                          Upload to remote
  git pull                          Download from remote

BRANCHING
  git branch                        List branches
  git switch -c <name>              Create + switch branch
  git switch <name>                 Switch branch
  git merge <branch>                Merge branch into current
  git branch -d <name>              Delete branch

HISTORY
  git log --oneline                 Compact history
  git log --graph --all             Visual branch history
  git diff                          Show changes
  git blame <file>                  Who changed each line

UNDO
  git restore <file>                Discard changes in file
  git reset --soft HEAD~1           Undo commit, keep changes
  git stash                         Temporarily save changes
  git stash pop                     Restore stashed changes

REMOTE
  git remote add origin <url>       Connect to GitHub
  git push -u origin <branch>       Push branch first time
  git fetch                         Download without merge
```

---

## Summary

| Topic | Key Takeaway |
|-------|-------------|
| Git Basics | Track changes with init, add, commit, push, pull |
| Branching | Work on features independently, merge when done |
| GitHub | Host repos, collaborate with PRs, track work with Issues |
| Merge Conflicts | Resolve manually when same lines are edited |
| Conventional Commits | Use `feat:`, `fix:`, `docs:` prefixes for clarity |
| Pre-commit Hooks | Automate code quality checks before every commit |
| README | Your project's front page — make it professional |
| GitHub Actions | Automate testing and linting on every push |
