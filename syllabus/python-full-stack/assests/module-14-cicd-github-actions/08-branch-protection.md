# Branch Protection & Status Checks

**Module 14 — CI/CD with GitHub Actions | Topic 8**

---

## Why Protect Branches?

Without branch protection, any developer can push directly to `main` — potentially deploying broken code to production. Branch protection rules enforce quality gates.

> **Analogy:** Think of branch protection like security at an airport. You cannot board the plane (merge to main) without passing through security checks (CI pipeline) and having a valid boarding pass (code review approval).

---

## Setting Up Branch Protection

### Step-by-Step

1. Go to your GitHub repository
2. Click **Settings** → **Branches** (in left sidebar)
3. Under "Branch protection rules", click **Add rule**
4. Enter `main` as the branch name pattern
5. Configure the rules (see below)
6. Click **Create**

---

## Essential Protection Rules

### Rule 1: Require Pull Request Before Merging

**What it does:** Nobody can push directly to `main`. All changes must go through a pull request.

**Settings:**
- Require a pull request before merging: **Enabled**
- Required number of approvals: **1** (or 2 for teams)
- Dismiss stale pull request approvals: **Enabled**

**Why it matters:**
```
Without PR requirement:
  Amit pushes buggy code directly to main → Production breaks → Customers affected

With PR requirement:
  Amit opens PR → Priya reviews → Finds bug → Amit fixes → PR approved → Merged safely
```

### Rule 2: Require Status Checks to Pass

**What it does:** The CI pipeline must pass before the PR can be merged.

**Settings:**
- Require status checks to pass before merging: **Enabled**
- Require branches to be up to date: **Enabled**
- Search and select your CI job name (e.g., "Lint & Test")

**How it works:**

```
Rahul opens PR:
  ├── CI Pipeline starts automatically
  │   ├── Lint: ✅ Passed
  │   ├── Test: ❌ Failed (3 tests broken)
  │   └── Status: FAILED
  │
  └── GitHub: "Merge blocked — required checks failed"

Rahul fixes the tests, pushes again:
  ├── CI Pipeline runs again
  │   ├── Lint: ✅ Passed
  │   ├── Test: ✅ Passed
  │   └── Status: PASSED
  │
  └── GitHub: "All checks passed — ready to merge"
```

### Rule 3: Require Conversation Resolution

**What it does:** All review comments must be resolved before merging.

If Priya comments "This function needs error handling" on the PR, Rahul must address it and resolve the conversation before the merge button becomes available.

### Rule 4: Restrict Force Pushes

**What it does:** Prevents `git push --force` to the protected branch.

Force pushing rewrites history and can destroy other people's work. This should always be disabled for `main`.

### Rule 5: Require Linear History

**What it does:** Only allows merge commits or squash merges — prevents messy merge histories.

**Recommended:** Enable "Squash merging" so each PR becomes a single commit on main.

---

## Recommended Configuration

### For Student Projects (Solo Developer)

| Rule | Setting |
|------|---------|
| Require PR | Optional (can skip for solo work) |
| Require status checks | **Enabled** (CI must pass) |
| Required approvals | 0 |
| Force push protection | **Enabled** |
| Require linear history | Optional |

### For Team Projects (2-4 Developers)

| Rule | Setting |
|------|---------|
| Require PR | **Enabled** |
| Required approvals | **1** |
| Require status checks | **Enabled** |
| Dismiss stale approvals | **Enabled** |
| Require conversation resolution | **Enabled** |
| Force push protection | **Enabled** |
| Require linear history | **Enabled** |

### For Production (Company)

| Rule | Setting |
|------|---------|
| Require PR | **Enabled** |
| Required approvals | **2** |
| Require status checks | **Enabled** |
| Require branches up to date | **Enabled** |
| Dismiss stale approvals | **Enabled** |
| Require conversation resolution | **Enabled** |
| Force push protection | **Enabled** |
| Include administrators | **Enabled** (even admins follow rules) |
| Restrict who can push | Only deploy bots |

---

## Status Checks — Connecting CI to Branch Protection

### Step 1: Name Your CI Jobs Clearly

```yaml
jobs:
  lint-and-test:
    name: "CI: Lint & Test"     # This name appears in branch protection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .
      - run: pytest
```

### Step 2: Select the Job as Required

In branch protection settings:
1. Enable "Require status checks to pass"
2. Search for "CI: Lint & Test"
3. Select it as a required check

Now, every PR must have this check passing before it can be merged.

### Multiple Required Checks

You can require multiple checks:

```yaml
jobs:
  lint:
    name: "CI: Lint"
    # ...

  test:
    name: "CI: Test"
    # ...

  security:
    name: "CI: Security Scan"
    # ...
```

In branch protection, select all three. All must pass.

---

## The PR Workflow with Branch Protection

Here is what the complete workflow looks like for a developer:

### 1. Create a Branch

```bash
git checkout -b feature/user-registration
```

### 2. Write Code and Tests

```bash
# Write your feature code
# Write tests for the feature
# Run tests locally: pytest
```

### 3. Push and Create PR

```bash
git push -u origin feature/user-registration
# Then create a PR on GitHub targeting main
```

### 4. CI Runs Automatically

GitHub Actions triggers on the pull request:
- Lint check runs
- Tests run
- Coverage is checked

### 5. Code Review

A teammate reviews the code:
- Reads the changes
- Leaves comments or suggestions
- Approves or requests changes

### 6. Address Feedback

Fix any issues raised in the review:

```bash
git add .
git commit -m "Address review feedback: add input validation"
git push
# CI runs again automatically
```

### 7. Merge

Once CI passes and reviews are approved:
- Click "Squash and merge" on GitHub
- The feature branch can be deleted

### 8. Automatic Deployment

The merge to `main` triggers the deployment workflow:
- Docker image is built
- Image is pushed to GHCR
- App is deployed to the server

---

## CODEOWNERS — Automatic Review Assignments

Create a `CODEOWNERS` file to automatically assign reviewers based on which files change.

```
# .github/CODEOWNERS

# Default reviewers for everything
*                       @team-lead

# Backend code needs backend team review
/backend/               @backend-team
/backend/app/models.py  @database-admin

# Frontend code
/frontend/              @frontend-team

# CI/CD changes need DevOps review
/.github/               @devops-team
Dockerfile              @devops-team
docker-compose.yml      @devops-team

# Security-sensitive files
/backend/app/auth/      @security-team
```

When a PR changes `backend/app/models.py`, `@database-admin` is automatically added as a reviewer.

---

## Protected Branches for Multiple Environments

```
main      → Production (protected: 2 approvals, all CI checks)
develop   → Staging (protected: 1 approval, CI checks)
feature/* → Development (no protection)
```

### Protecting the Develop Branch

1. Settings → Branches → Add rule
2. Branch name pattern: `develop`
3. Require PR: Yes
4. Required approvals: 1
5. Require status checks: Yes

---

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| "Required check not found" | The CI workflow must have run at least once for the check name to appear |
| Admin wants to bypass rules | Enable "Include administrators" to enforce rules for everyone |
| Stale approval after new push | Enable "Dismiss stale approvals" — pushes invalidate old approvals |
| CI passes but can't merge | Check if "Require branches to be up to date" is enabled — rebase your branch |
| Someone force pushed to main | Enable "Restrict force pushes" |

---

## Practice Exercise

1. Create a branch protection rule for `main` in your repository
2. Enable "Require status checks" and select your CI job
3. Try pushing directly to main — it should be blocked
4. Create a PR, let CI run, and merge through the PR
5. Set up a CODEOWNERS file for your project

---

*Congratulations! You now have a complete CI/CD setup with GitHub Actions — from automated testing to deployment with proper branch protection.*
