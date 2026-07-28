# GitHub Workflow — Fork, Clone, Pull Requests & Code Review

**Module 05 — Git, GitHub & Professional Workflow | Topic 3**

---

## Git vs GitHub

| Git | GitHub |
|-----|--------|
| Software you install on your computer | Website/platform (github.com) |
| Tracks changes locally | Hosts your repositories online |
| Works offline | Requires internet |
| Command-line tool | Web interface + API |
| Created by Linus Torvalds (2005) | Created by Tom Preston-Werner (2008) |

**Think of it this way:** Git is the engine. GitHub is the road and the parking lot.

Other platforms similar to GitHub: **GitLab**, **Bitbucket**, **Azure DevOps**.

---

## GitHub Account Setup

1. Go to https://github.com and create an account
2. Use your professional email
3. Choose a clean username (this will be on your resume)
4. Set up SSH keys (recommended for security):

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "rahul@email.com"

# Copy the public key
cat ~/.ssh/id_ed25519.pub
```

5. Add the key to GitHub: Settings > SSH and GPG keys > New SSH key

---

## Fork and Clone — Contributing to Other Projects

### Fork

A **fork** is your personal copy of someone else's repository on GitHub. You can freely experiment with changes without affecting the original project.

**How to fork:**
1. Go to the repository on GitHub (e.g., `github.com/techpath/python-course`)
2. Click the **Fork** button (top right)
3. GitHub creates a copy under your account: `github.com/rahul/python-course`

### Clone

**Clone** downloads a repository from GitHub to your computer.

```bash
# Clone your fork
git clone git@github.com:rahul/python-course.git
cd python-course

# Add the original repository as "upstream"
git remote add upstream git@github.com:techpath/python-course.git

# Verify remotes
git remote -v
# origin    git@github.com:rahul/python-course.git (fetch)
# origin    git@github.com:rahul/python-course.git (push)
# upstream  git@github.com:techpath/python-course.git (fetch)
# upstream  git@github.com:techpath/python-course.git (push)
```

### Keeping Your Fork Updated

```bash
# Get the latest from the original repo
git fetch upstream

# Merge into your main branch
git checkout main
git merge upstream/main

# Push the update to your fork
git push origin main
```

---

## Pull Requests (PRs) — The Core of Team Collaboration

A **Pull Request** is a proposal to merge your changes into another branch (usually `main`). It lets your team review the code before it goes live.

### Creating a Pull Request

**Step 1:** Push your feature branch to GitHub

```bash
git push -u origin feature/user-registration
```

**Step 2:** Open GitHub and create the PR

1. Go to your repository on GitHub
2. Click **Compare & pull request** (appears automatically after pushing)
3. Fill in the PR form:

```markdown
## Summary
- Add user registration with email validation
- Connect to FastAPI backend endpoint
- Include password strength indicator

## Changes
- `src/components/RegisterForm.tsx` — New registration form
- `src/services/auth.service.ts` — API call for registration
- `src/utils/validation.ts` — Email and password validators

## How to Test
1. Go to /register
2. Fill in the form with a valid email
3. Submit and check the console for the API response

## Screenshots
(attach screenshots if UI changes)
```

**Step 3:** Request reviewers and submit

### PR Best Practices

| Do | Do Not |
|----|--------|
| Keep PRs small (under 400 lines) | Submit 2000-line mega PRs |
| One feature per PR | Mix unrelated changes |
| Write a clear description | Leave the description empty |
| Add screenshots for UI changes | Expect reviewers to guess |
| Respond to review comments | Ignore feedback |
| Test before creating PR | Push broken code |

---

## Code Review — Reading and Reviewing Others' Code

### As a Reviewer

When someone asks you to review their PR:

1. **Read the description** — Understand what the PR does
2. **Check the diff** — Look at the code changes tab
3. **Leave comments** — Click the `+` button next to any line to add a comment
4. **Approve, Request Changes, or Comment:**

| Action | When to Use |
|--------|-------------|
| **Approve** | Code looks good, no issues |
| **Request Changes** | Issues that must be fixed before merging |
| **Comment** | Suggestions or questions, not blocking |

### Review Checklist

- [ ] Does the code do what the PR says?
- [ ] Are there any bugs or edge cases?
- [ ] Is the code readable and well-structured?
- [ ] Are there proper error handling?
- [ ] Are there any security issues (hardcoded passwords, SQL injection)?
- [ ] Does it follow the project's coding style?
- [ ] Are there tests for the new code?

### As the PR Author — Responding to Reviews

```markdown
## Common review comment responses:

"Good catch! Fixed in commit abc123."

"I chose this approach because... [explain reasoning]"

"You're right, I've refactored this. Please re-review."
```

---

## Handling Merge Conflicts in PRs

When your PR has conflicts with the target branch:

**Method 1: Merge main into your branch**

```bash
git checkout feature/user-registration
git pull origin main
# Resolve conflicts in your editor
git add .
git commit -m "Resolve merge conflicts with main"
git push
```

**Method 2: Rebase onto main**

```bash
git checkout feature/user-registration
git rebase origin/main
# Resolve conflicts in your editor
git add .
git rebase --continue
git push --force-with-lease   # Required after rebase
```

**Note:** `--force-with-lease` is safer than `--force` — it fails if someone else pushed to the branch.

---

## Fork Workflow — Contributing to Open Source

```
1. Fork the repo on GitHub
2. Clone your fork locally
3. Create a feature branch
4. Make changes, commit, push to your fork
5. Open a PR from your fork to the original repo
6. Maintainers review and merge your PR
7. Sync your fork with the original
```

```bash
# Full example: Contributing a typo fix to an open source project
git clone git@github.com:rahul/open-source-project.git
cd open-source-project
git remote add upstream git@github.com:original-author/open-source-project.git

git checkout -b fix/readme-typo
# ... fix the typo ...
git add README.md
git commit -m "Fix typo in README installation instructions"
git push -u origin fix/readme-typo
# Go to GitHub → Create Pull Request from your fork to upstream
```

---

## GitHub Features for Collaboration

### Issues

Issues track bugs, feature requests, and tasks.

```markdown
## Bug Report

**Description:** Login page crashes when email field is empty

**Steps to Reproduce:**
1. Go to /login
2. Leave email field empty
3. Click "Login"

**Expected:** Show validation error
**Actual:** Page crashes with TypeError

**Environment:** Chrome 120, Windows 11
```

### Labels

| Label | Use |
|-------|-----|
| `bug` | Something is broken |
| `feature` | New feature request |
| `documentation` | Documentation updates |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |
| `priority: high` | Must be fixed soon |

### Linking PRs to Issues

```markdown
# In your PR description:
Closes #42
Fixes #15
Resolves #7
```

When the PR is merged, the linked issues are automatically closed.

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Fork | Your personal copy of another's repo on GitHub |
| Clone | Download a repo to your computer |
| Pull Request | Proposal to merge your code into another branch |
| Code Review | Team members check your code quality |
| Merge Conflict | Two branches changed the same lines — manual fix needed |
| Issues | Track bugs, features, and tasks |
| `upstream` | Remote pointing to the original repo (not your fork) |

---

*TechPath Institute — Python Full Stack Development*
