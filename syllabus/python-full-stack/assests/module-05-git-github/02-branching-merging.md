# Branching & Merging — Parallel Universes for Your Code

**Module 05 — Git, GitHub & Professional Workflow | Topic 2**

---

## What are Branches?

A branch is an **independent copy** of your code where you can make changes without affecting the main codebase. Think of it like working on a rough draft while the original stays safe.

**Real-world analogy:** Imagine you are writing a novel. The published book is `main`. When you want to add a new chapter, you write it on separate pages (a branch). Only when the chapter is perfect do you insert it into the book (merge).

### Why Use Branches?

| Situation | Without Branches | With Branches |
|-----------|-----------------|---------------|
| Adding a new feature | Risk breaking working code | Develop in isolation, merge when ready |
| Fixing a bug | Must pause current work | Create a hotfix branch, fix, merge, continue |
| Experimenting | Afraid to try new ideas | Create a branch, experiment freely, delete if it fails |
| Team of 5 developers | Everyone edits the same code — chaos | Each person works on their own branch |

---

## Branch Commands

### Creating and Switching Branches

```bash
# See all branches (current branch has a * next to it)
git branch
# * main

# Create a new branch
git branch feature/login

# Switch to the new branch
git checkout feature/login
# Or (modern way):
git switch feature/login

# Create AND switch in one command
git checkout -b feature/login
# Or:
git switch -c feature/login

# See all branches (including remote)
git branch -a
```

### Branch Naming Conventions

| Pattern | Use For | Example |
|---------|---------|---------|
| `feature/name` | New features | `feature/user-login` |
| `fix/name` | Bug fixes | `fix/email-validation` |
| `hotfix/name` | Urgent production fixes | `hotfix/payment-crash` |
| `refactor/name` | Code cleanup | `refactor/database-queries` |
| `docs/name` | Documentation updates | `docs/api-readme` |

**Rules:**
- Use lowercase
- Use hyphens, not spaces or underscores
- Keep it short but descriptive

---

## Merging Branches

When your feature is complete, you merge it back into `main`.

### Fast-Forward Merge

When `main` has not changed since you branched off, Git simply moves the pointer forward.

```bash
# Switch to main
git checkout main

# Merge the feature branch into main
git merge feature/login
# Output: Fast-forward
```

```
Before merge:
main:          A ── B ── C
feature/login:             ── D ── E

After merge (fast-forward):
main:          A ── B ── C ── D ── E
```

### Three-Way Merge

When both branches have new commits, Git creates a **merge commit** that combines both.

```bash
git checkout main
git merge feature/login
# Output: Merge made by the 'ort' strategy.
```

```
Before merge:
main:          A ── B ── C ── F
feature/login:        └── D ── E

After merge:
main:          A ── B ── C ── F ── M (merge commit)
feature/login:        └── D ── E ──┘
```

### Merge Conflicts

When both branches modify the **same lines** of the same file, Git cannot decide which version to keep. This is called a **merge conflict**.

```bash
git merge feature/login
# CONFLICT (content): Merge conflict in app.py
# Automatic merge failed; fix conflicts and then commit the result.
```

**What the conflict looks like in the file:**

```python
def greeting():
<<<<<<< HEAD
    return "Welcome to TechPath!"
=======
    return "Welcome to TechPath Institute!"
>>>>>>> feature/login
```

- `<<<<<<< HEAD` = what is in your current branch (main)
- `=======` = separator
- `>>>>>>> feature/login` = what is in the incoming branch

**How to resolve:**
1. Open the file and choose the correct version (or combine both)
2. Remove the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Save the file
4. Stage and commit

```bash
# After editing the file:
git add app.py
git commit -m "Resolve merge conflict in app.py"
```

---

## Rebase — Rewriting History

Rebase moves your branch's commits **on top of** another branch, creating a linear history.

```bash
# On feature/login branch:
git rebase main
```

```
Before rebase:
main:          A ── B ── C ── F
feature/login:        └── D ── E

After rebase:
main:          A ── B ── C ── F
feature/login:                 └── D' ── E'
```

The commits D and E are replayed on top of F, creating D' and E' (new commit hashes).

### Merge vs Rebase

| Feature | Merge | Rebase |
|---------|-------|--------|
| History | Preserves all branches (non-linear) | Linear, clean history |
| Merge commit | Creates one | Does not create one |
| Safety | Safe — never changes existing commits | Rewrites history — never do on shared branches |
| Best for | Merging to main | Keeping feature branches up-to-date |

**Golden rule:** Never rebase commits that have been pushed to a shared remote branch.

---

## Cherry-Pick — Grab a Single Commit

Cherry-pick lets you copy a specific commit from one branch to another.

```bash
# Copy commit abc1234 to the current branch
git cherry-pick abc1234
```

**Use case:** You fixed a bug on `feature/login` but need the fix on `main` immediately, without merging the entire feature branch.

```bash
git checkout main
git cherry-pick abc1234   # The bug fix commit
```

---

## Stash — Save Work for Later

Stash temporarily saves your uncommitted changes so you can switch branches.

```bash
# Save current changes to the stash
git stash
# Or with a message:
git stash push -m "work in progress: login form"

# See all stashes
git stash list
# stash@{0}: On feature/login: work in progress: login form
# stash@{1}: WIP on main: fixing tests

# Restore the most recent stash
git stash pop

# Restore a specific stash
git stash pop stash@{1}

# Restore without removing from stash list
git stash apply

# Delete a stash
git stash drop stash@{0}

# Delete all stashes
git stash clear
```

**Common scenario:**

```bash
# You're working on feature/login but need to fix a bug on main
git stash                           # Save current work
git checkout main                   # Switch to main
git checkout -b hotfix/crash-fix    # Create hotfix branch
# ... fix the bug ...
git add . && git commit -m "Fix crash on login page"
git checkout main && git merge hotfix/crash-fix
git checkout feature/login          # Go back to your feature
git stash pop                       # Restore your saved work
```

---

## Deleting Branches

```bash
# Delete a local branch (only if fully merged)
git branch -d feature/login

# Force delete (even if not merged)
git branch -D feature/login

# Delete a remote branch
git push origin --delete feature/login
```

---

## Practical Workflow Example

Rahul is working on a user registration feature at TechPath Institute:

```bash
# Step 1: Start from the latest main
git checkout main
git pull origin main

# Step 2: Create a feature branch
git checkout -b feature/user-registration

# Step 3: Work on the feature (multiple commits)
# ... edit files ...
git add .
git commit -m "Add registration form component"

# ... more edits ...
git add .
git commit -m "Add email validation with regex"

# ... more edits ...
git add .
git commit -m "Connect registration to FastAPI backend"

# Step 4: Keep branch updated with main
git checkout main
git pull origin main
git checkout feature/user-registration
git rebase main

# Step 5: Push the branch to GitHub
git push -u origin feature/user-registration

# Step 6: Create a Pull Request on GitHub (next topic)

# Step 7: After PR is approved and merged, clean up
git checkout main
git pull origin main
git branch -d feature/user-registration
```

---

## Summary

| Command | What It Does |
|---------|-------------|
| `git branch` | List branches |
| `git branch name` | Create a branch |
| `git checkout name` / `git switch name` | Switch to a branch |
| `git checkout -b name` | Create and switch |
| `git merge name` | Merge a branch into current |
| `git rebase main` | Replay commits on top of main |
| `git cherry-pick hash` | Copy one specific commit |
| `git stash` | Temporarily save uncommitted changes |
| `git stash pop` | Restore stashed changes |
| `git branch -d name` | Delete a merged branch |

---

*TechPath Institute — Python Full Stack Development*
