# Git Basics — Your Code's Time Machine

**Module 05 — Git, GitHub & Professional Workflow | Topic 1**

---

## What is Git?

Git is a **version control system** — it tracks every change you make to your code and lets you go back to any previous version. Think of it as an "undo" button that works across your entire project and never runs out of memory.

**Real-world analogy:** Imagine writing a college assignment in Google Docs. Google Docs saves every version automatically — you can see what you wrote yesterday, last week, or last month. Git does the same for your code, but with much more control.

### Why Git?

| Without Git | With Git |
|-------------|----------|
| Files named `project_final.py`, `project_final_v2.py`, `project_ACTUAL_final.py` | One file, infinite history |
| Cannot work with teammates on the same file | Multiple people edit simultaneously |
| Accidentally deleted code? Gone forever | Recover any past version in seconds |
| No idea who changed what and when | Full history with author, date, and message |
| Deploying untested code to production | Work on features in isolation (branches) |

---

## Installing Git

### Windows

1. Download from https://git-scm.com/download/win
2. Run the installer (keep default settings)
3. Open **Git Bash** from the Start menu

### Ubuntu/Linux

```bash
sudo apt update
sudo apt install git
```

### Verify Installation

```bash
git --version
# Output: git version 2.43.0 (or similar)
```

### First-Time Setup

```bash
# Set your name (appears in every commit)
git config --global user.name "Rahul Sharma"

# Set your email (must match your GitHub email)
git config --global user.email "rahul@email.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Check your settings
git config --list
```

---

## The Three Areas of Git

Git has three "zones" where your files can live:

```
Working Directory    →    Staging Area    →    Repository
(your files)              (ready to save)      (saved permanently)

  Edit files         git add            git commit
  ─────────────►     ─────────────►     ─────────────►
```

| Area | What It Is | Analogy |
|------|-----------|---------|
| **Working Directory** | Your project folder — the files you see and edit | Your desk where you write |
| **Staging Area** | Files marked as "ready to commit" | The envelope you put finished letters into |
| **Repository (.git)** | The permanent history of all commits | The post office that stores all sent letters |

---

## Essential Git Commands

### git init — Start Tracking a Project

```bash
# Create a new project folder
mkdir my-project
cd my-project

# Initialize Git in this folder
git init
# Output: Initialized empty Git repository in /home/rahul/my-project/.git/
```

This creates a hidden `.git` folder that stores all version history. Never delete or modify this folder manually.

### git status — Check What Changed

```bash
git status
```

This is the most-used command. It shows:
- Files you modified
- New files Git does not know about yet (untracked)
- Files staged and ready to commit

```
On branch main
Changes not staged for commit:
  modified:   app.py

Untracked files:
  config.py

no changes added to commit
```

**Tip:** Run `git status` after every operation. It tells you exactly what Git sees.

### git add — Stage Files for Commit

```bash
# Stage a specific file
git add app.py

# Stage multiple files
git add app.py config.py

# Stage all changed and new files
git add .

# Stage all files matching a pattern
git add *.py
```

### git commit — Save a Snapshot

```bash
# Commit with a message
git commit -m "Add user login feature"

# Commit with a multi-line message
git commit -m "Add user login feature

- Created login form component
- Added password hashing with bcrypt
- Connected to database for user lookup"
```

**Writing good commit messages:**

| Good | Bad |
|------|-----|
| `Add user login with bcrypt hashing` | `update` |
| `Fix crash when email field is empty` | `fix bug` |
| `Remove unused imports from utils.py` | `changes` |
| `Update README with setup instructions` | `stuff` |

**Rules for commit messages:**
1. Start with a verb: Add, Fix, Update, Remove, Refactor
2. Keep the first line under 50 characters
3. Explain *what* and *why*, not *how*

### git log — View Commit History

```bash
# Full log
git log

# Compact one-line log
git log --oneline

# Show last 5 commits
git log --oneline -5

# Show log with file changes
git log --stat

# Show log as a graph (useful with branches)
git log --oneline --graph --all
```

**Example output of `git log --oneline`:**

```
a3b4c5d (HEAD -> main) Add user login feature
f1e2d3c Create database models
b8a7c6d Initial project setup
```

### git diff — See What Changed

```bash
# See unstaged changes (what you modified but haven't added yet)
git diff

# See staged changes (what you added but haven't committed yet)
git diff --staged

# See changes between two commits
git diff a3b4c5d f1e2d3c

# See changes in a specific file
git diff app.py
```

---

## Working with Remote Repositories

A **remote** is a copy of your repository stored on a server (like GitHub). It lets you back up your code and collaborate with others.

### git remote — Connect to GitHub

```bash
# Add a remote (usually done once after git init)
git remote add origin https://github.com/rahul/my-project.git

# View remotes
git remote -v
# origin  https://github.com/rahul/my-project.git (fetch)
# origin  https://github.com/rahul/my-project.git (push)
```

### git push — Upload to GitHub

```bash
# Push to the main branch (first time, set upstream)
git push -u origin main

# After the first push, just:
git push
```

### git pull — Download from GitHub

```bash
# Pull latest changes from the remote
git pull

# This is equivalent to:
git fetch + git merge
```

### git clone — Download an Entire Repository

```bash
# Clone a repository from GitHub
git clone https://github.com/techpath/python-course.git

# Clone into a specific folder
git clone https://github.com/techpath/python-course.git my-folder
```

---

## .gitignore — Files Git Should Ignore

Some files should never be tracked: passwords, API keys, temporary files, build outputs.

Create a file named `.gitignore` in your project root:

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
*.egg-info/

# Virtual environment
venv/
.venv/
env/

# IDE files
.vscode/
.idea/
*.swp

# Environment variables (SECRETS!)
.env
.env.local
.env.production

# OS files
.DS_Store
Thumbs.db

# Build output
dist/
build/
node_modules/

# Database files
*.db
*.sqlite3
```

**Important:** Add `.gitignore` BEFORE your first commit. If you accidentally commit a secret file, it stays in the history even after you delete it.

---

## Undoing Things

### Unstage a File (Undo git add)

```bash
git restore --staged app.py
```

### Discard Changes (Undo edits to a file)

```bash
# WARNING: This permanently discards your changes!
git restore app.py
```

### Amend the Last Commit (Fix a typo in the message)

```bash
git commit --amend -m "Corrected commit message"
```

### Revert a Commit (Undo a commit safely)

```bash
# Creates a NEW commit that undoes the changes of the specified commit
git revert a3b4c5d
```

---

## The Complete Workflow

Here is the daily workflow every developer follows:

```
1. Pull latest changes       →  git pull
2. Edit your files           →  (write code)
3. Check what changed        →  git status
4. Review your changes       →  git diff
5. Stage the files           →  git add .
6. Commit with a message     →  git commit -m "Add feature X"
7. Push to GitHub            →  git push
```

**Example session:**

```bash
# Morning: Get latest code from the team
git pull

# Work on a new feature...
# (edit files)

# Check status
git status
# modified: app.py
# new file: utils/helpers.py

# Review changes
git diff

# Stage and commit
git add app.py utils/helpers.py
git commit -m "Add helper functions for date formatting"

# Push to GitHub
git push
```

---

## Summary

| Command | What It Does |
|---------|-------------|
| `git init` | Start tracking a new project |
| `git status` | See what changed |
| `git add <file>` | Stage a file for commit |
| `git commit -m "msg"` | Save a snapshot |
| `git log --oneline` | View commit history |
| `git diff` | See line-by-line changes |
| `git push` | Upload to GitHub |
| `git pull` | Download from GitHub |
| `git clone <url>` | Download an entire repo |
| `git restore <file>` | Discard changes |
| `.gitignore` | List files Git should ignore |

---

*TechPath Institute — Python Full Stack Development*
