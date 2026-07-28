# CI/CD Concepts

**Module 14 — CI/CD with GitHub Actions | Topic 1**

---

## What Is CI/CD?

Imagine Ananya and her team of 4 developers are building a FastAPI application. Every day, each person writes code on their own laptop. At the end of the week, they try to combine everyone's code. Things break. Tests fail. The deployment takes a full day of fixing conflicts.

**CI/CD automates this entire process** — every time someone pushes code, a robot automatically tests it, checks for errors, builds it, and deploys it.

> **Analogy:** Think of CI/CD like a car manufacturing assembly line. Instead of one person building an entire car by hand (slow, error-prone), each station does one specific job automatically — welding, painting, testing brakes. The car moves through the line and comes out ready to drive.

---

## CI — Continuous Integration

**Continuous Integration** means every developer's code is automatically merged and tested multiple times a day.

### Without CI

```
Monday:    Rahul writes feature A
Tuesday:   Priya writes feature B
Wednesday: Amit writes feature C
Thursday:  Sneha writes feature D
Friday:    Everyone merges → CHAOS, conflicts, broken code
Weekend:   Fixing bugs instead of resting
```

### With CI

```
Monday 10 AM:  Rahul pushes code → Auto-test → Green ✓
Monday 2 PM:   Priya pushes code → Auto-test → Green ✓
Monday 4 PM:   Amit pushes code  → Auto-test → Red ✗ (fix immediately!)
Tuesday 9 AM:  Sneha pushes code → Auto-test → Green ✓
```

**CI catches problems early** — when they are small and easy to fix.

### What CI Does Automatically

| Step | What Happens | Tool Example |
|------|-------------|--------------|
| Install dependencies | `pip install -r requirements.txt` | pip, poetry |
| Lint code | Check code style and errors | ruff, flake8 |
| Run tests | Execute all test cases | pytest |
| Check types | Verify type annotations | mypy |
| Measure coverage | How much code is tested? | pytest-cov |
| Build | Compile/package the application | docker build |

---

## CD — Continuous Delivery vs Continuous Deployment

CD has two meanings — people often confuse them.

### Continuous Delivery

Code is automatically tested and **ready to deploy**, but a human clicks the "Deploy" button.

```
Push code → Auto-test → Auto-build → [Manual approval] → Deploy
```

### Continuous Deployment

Code is automatically tested, built, **and deployed** — no human involved.

```
Push code → Auto-test → Auto-build → Auto-deploy (live!)
```

| Feature | Continuous Delivery | Continuous Deployment |
|---------|--------------------|-----------------------|
| Testing | Automated | Automated |
| Building | Automated | Automated |
| Deploying | Manual approval needed | Fully automatic |
| Risk | Lower (human reviews) | Higher (must trust tests) |
| Speed | Slower | Faster |
| Common in | Banks, healthcare, large companies | Startups, SaaS, tech companies |

**For this course, we use Continuous Delivery** — automated testing and building, with manual approval before deploying to production.

---

## The CI/CD Pipeline

A **pipeline** is the complete series of automated steps your code goes through from push to production.

### Typical Python Pipeline

```
Developer pushes code to GitHub
         │
         ▼
    ┌─────────┐
    │  TRIGGER │  ← Push to main, or PR opened
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ INSTALL  │  ← pip install, poetry install
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │   LINT   │  ← ruff check, black --check
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │   TEST   │  ← pytest --cov
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │  BUILD   │  ← docker build -t app .
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │  PUSH    │  ← docker push to GHCR
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ DEPLOY   │  ← Deploy to server
    └─────────┘
```

If any step fails, the pipeline stops and the team is notified.

---

## DORA Metrics — Measuring CI/CD Performance

**DORA** (DevOps Research and Assessment) defines four key metrics used by top engineering teams worldwide:

| Metric | What It Measures | Elite Performance |
|--------|-----------------|-------------------|
| **Deployment Frequency** | How often you deploy to production | Multiple times per day |
| **Lead Time for Changes** | Time from code commit to production | Less than 1 hour |
| **Change Failure Rate** | % of deployments that cause failures | Less than 15% |
| **Mean Time to Recovery (MTTR)** | Time to fix a production failure | Less than 1 hour |

### Why These Matter for Your Career

Indian tech companies (Razorpay, Zerodha, CRED, Swiggy) actively look for developers who understand CI/CD. During interviews, you might be asked:

- "How do you ensure code quality before deployment?"
- "What happens when you push code to the main branch?"
- "How would you set up automated testing?"

Knowing CI/CD well sets you apart from other freshers.

---

## CI/CD Tools

| Tool | Type | Free? | Best For |
|------|------|-------|----------|
| **GitHub Actions** | CI/CD | 2000 min/month free | GitHub repos (this course) |
| Jenkins | CI/CD | Open source | Self-hosted, enterprise |
| GitLab CI | CI/CD | 400 min/month free | GitLab repos |
| CircleCI | CI/CD | 6000 min/month free | Complex pipelines |
| Travis CI | CI | Limited free | Open-source projects |
| Azure DevOps | CI/CD | 1 free parallel job | Microsoft/Azure ecosystem |

**We use GitHub Actions** because:
- It is built into GitHub (no separate tool to set up)
- Generous free tier (2000 minutes/month)
- Huge marketplace of reusable actions
- Industry standard for modern Python projects

---

## CI/CD Benefits — Summary

| Benefit | Without CI/CD | With CI/CD |
|---------|--------------|------------|
| Finding bugs | Days or weeks later | Minutes after pushing |
| Code quality | Depends on discipline | Enforced automatically |
| Deployment | Manual, scary, hours | Automated, confident, minutes |
| Team collaboration | Merge conflicts pile up | Small, frequent merges |
| Feedback | "Wait for QA team" | Instant (pipeline passes/fails) |
| Documentation | "How do we deploy?" | Pipeline IS the documentation |

---

## Real-World CI/CD at Indian Startups

### Example: Razorpay

When a Razorpay developer pushes code:
1. Tests run automatically (200+ test cases)
2. Security scan checks for vulnerabilities
3. Code review is required (at least 2 approvals)
4. Staging deployment happens automatically
5. QA team verifies on staging
6. Production deployment after approval

### Example: A TechPath Student Project

When you push code to your capstone project:
1. Ruff checks code style
2. Pytest runs all tests
3. Docker image is built
4. Image is pushed to GHCR
5. Server pulls and deploys the new image

You will set this up in the next topics.

---

## Key Terms

| Term | Meaning |
|------|---------|
| **Pipeline** | The full automated process from code push to deployment |
| **Job** | A group of steps that run on the same machine |
| **Step** | A single task (install, lint, test, etc.) |
| **Trigger** | What starts the pipeline (push, PR, schedule) |
| **Runner** | The machine that executes your pipeline |
| **Artifact** | Files produced by the pipeline (test reports, built images) |
| **Green build** | All pipeline steps passed |
| **Red build** | One or more steps failed |

---

## Practice Exercise

1. List all the steps you currently do manually to deploy your project
2. Identify which steps can be automated
3. Draw your ideal CI/CD pipeline on paper
4. Research GitHub Actions free tier limits

---

*Next Topic: GitHub Actions Anatomy — understanding the YAML workflow file.*
