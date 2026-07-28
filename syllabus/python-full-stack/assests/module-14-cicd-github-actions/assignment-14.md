# Module 14 — Assignment: CI/CD with GitHub Actions

**Deadline:** End of Week 24
**Submission:** GitHub repository link with working workflows (Actions tab must show green runs)

---

## Task 1: Hello World Workflow — 15 marks

Create your first GitHub Actions workflow that runs on every push.

**What to do:**
1. Create a new GitHub repository called `cicd-practice`
2. Add a file `.github/workflows/hello.yml`
3. The workflow should:
   - Run on every push to any branch
   - Have a job called `greet` that runs on `ubuntu-latest`
   - Print "Namaste from TechPath Institute, Bhopal!" using `echo`
   - Print the current date and time
   - Print which branch triggered the workflow using `${{ github.ref }}`

**Deliverables:**
- [ ] Workflow file committed at `.github/workflows/hello.yml`
- [ ] At least 1 successful run visible in the **Actions** tab
- [ ] Screenshot of the green checkmark on your commit

---

## Task 2: CI Pipeline — Lint & Test — 30 marks

Build a CI pipeline that automatically lints and tests a Python project.

**What to do:**
1. In the same `cicd-practice` repo, create a small Python project:
   - `app/main.py` — a simple function (e.g., `calculate_gst(price, rate)` that returns price with GST)
   - `app/__init__.py` — empty file
   - `tests/test_main.py` — at least 5 test cases for your function
   - `requirements.txt` — include `pytest`, `pytest-cov`, `ruff`
2. Create `.github/workflows/ci.yml` with:
   - Trigger on push and pull_request to main
   - Matrix build: Python 3.11 and 3.12
   - Steps: checkout, setup Python, cache pip, install deps, lint with ruff, run pytest with coverage
   - Coverage must be reported in the logs

**Deliverables:**
- [ ] Python project with at least 5 tests (all passing)
- [ ] CI workflow with matrix build (3.11 + 3.12)
- [ ] Pip caching configured
- [ ] Ruff lint passing
- [ ] Coverage report visible in the Actions logs
- [ ] At least 2 successful runs visible

**Rubric:**

| Criteria | Marks |
|----------|-------|
| Working Python project with tests | 8 |
| Matrix build (both versions pass) | 5 |
| Pip caching configured correctly | 4 |
| Ruff lint step passes | 5 |
| Coverage report in logs | 5 |
| Clean, well-commented workflow YAML | 3 |

---

## Task 3: Docker Build & Push to GHCR — 30 marks

Create a CD workflow that builds a Docker image and pushes it to GitHub Container Registry.

**What to do:**
1. Add a `Dockerfile` to your `cicd-practice` repo:
   - Use `python:3.12-slim` as base image
   - Copy your app code
   - Install dependencies
   - Set the entry point (e.g., `CMD ["python", "-m", "pytest"]` or run your app)
2. Create `.github/workflows/cd.yml` with:
   - Trigger on push to main only
   - Set proper permissions (`contents: read`, `packages: write`)
   - Steps: checkout, setup Docker Buildx, login to GHCR, build and push image
   - Tag the image with both `latest` and the commit SHA
3. Verify the image appears in your GitHub profile under **Packages**

**Deliverables:**
- [ ] Working `Dockerfile`
- [ ] CD workflow that builds and pushes to GHCR
- [ ] Image visible in GitHub Packages (screenshot)
- [ ] Image tagged with both `latest` and commit SHA
- [ ] At least 1 successful CD run in the Actions tab

**Rubric:**

| Criteria | Marks |
|----------|-------|
| Working Dockerfile | 7 |
| GHCR login step works | 5 |
| Build and push action configured | 8 |
| Dual tagging (latest + SHA) | 5 |
| Image visible in GitHub Packages | 5 |

---

## Task 4: Full Pipeline with Branch Protection — 25 marks

Connect everything into a complete CI/CD pipeline with branch protection.

**What to do:**
1. Set up branch protection on `main`:
   - Require Pull Request before merging
   - Require the CI workflow to pass before merging
   - Enable "Require branches to be up to date before merging"
2. Demonstrate the full flow:
   - Create a feature branch (`feature/add-discount`)
   - Add a new function (e.g., `calculate_discount(price, percent)`) with tests
   - Push the feature branch and create a Pull Request
   - Show the CI checks running on the PR
   - Merge the PR after CI passes
   - Show the CD pipeline running after the merge
3. Add a CI status badge to your `README.md`

**Deliverables:**
- [ ] Branch protection configured (screenshot of settings)
- [ ] Pull Request created with CI checks visible
- [ ] PR merged after CI passes
- [ ] CD pipeline runs after merge (screenshot)
- [ ] Status badge visible in README.md
- [ ] Complete GitHub repo link

**Rubric:**

| Criteria | Marks |
|----------|-------|
| Branch protection configured correctly | 6 |
| PR created from feature branch | 4 |
| CI checks visible on PR | 5 |
| CD runs after merge | 5 |
| Status badge in README | 3 |
| Clean commit history | 2 |

---

## Total Marks: 100

| Task | Topic | Marks |
|------|-------|-------|
| Task 1 | Hello World Workflow | 15 |
| Task 2 | CI Pipeline — Lint & Test | 30 |
| Task 3 | Docker Build & Push to GHCR | 30 |
| Task 4 | Full Pipeline + Branch Protection | 25 |
| **Total** | | **100** |

---

## Submission Guidelines

1. Push all code to a **public** GitHub repository named `cicd-practice`
2. Make sure the **Actions** tab shows your workflow runs (green checkmarks)
3. Submit the GitHub repository URL
4. Include screenshots of:
   - Successful CI run (Actions tab)
   - Docker image in GitHub Packages
   - Branch protection settings
   - Pull Request with CI checks
5. **Late submission:** 5 marks deducted per day after the deadline
