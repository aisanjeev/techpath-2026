# CI/CD with GitHub Actions — Quiz

**Module 14 | 15 Questions**

---

### Q1. What does CI stand for in CI/CD?

- A) Code Installation
- B) Continuous Integration — automatically merging and testing code frequently ✅
- C) Complete Implementation
- D) Central Infrastructure

> **Explanation:** Continuous Integration means developers frequently merge their code changes into a shared repository, and each merge is automatically verified by building and running tests.

---

### Q2. What is the key difference between Continuous Delivery and Continuous Deployment?

- A) Continuous Delivery is faster
- B) Continuous Deployment requires no testing
- C) Continuous Delivery needs manual approval to deploy, while Continuous Deployment is fully automatic ✅
- D) They are the same thing

> **Explanation:** In Continuous Delivery, code is automatically tested and ready to deploy, but a human must approve the deployment. In Continuous Deployment, everything is fully automatic — code goes to production without human intervention.

---

### Q3. Where must GitHub Actions workflow files be stored?

- A) In the root of the repository
- B) In the .github/workflows/ directory ✅
- C) In a ci/ directory
- D) Anywhere in the repository with a .yml extension

> **Explanation:** GitHub Actions workflow files must be YAML files (.yml or .yaml) located in the .github/workflows/ directory. GitHub only looks in this specific location.

---

### Q4. What does 'runs-on: ubuntu-latest' specify in a workflow?

- A) The programming language to use
- B) The Docker image to build
- C) The virtual machine (runner) where the job executes ✅
- D) The GitHub branch to run on

> **Explanation:** The "runs-on" field specifies the runner — the virtual machine that executes the job. "ubuntu-latest" means a fresh Ubuntu Linux VM provided by GitHub.

---

### Q5. What is the purpose of 'needs: lint' in a job definition?

- A) It installs the lint package
- B) It makes the job run only after the "lint" job completes successfully ✅
- C) It includes the lint job's code in this job
- D) It requires the lint tool to be pre-installed

> **Explanation:** The "needs" keyword creates a dependency between jobs. By default, jobs run in parallel. "needs: lint" makes the current job wait for the "lint" job to complete successfully before starting.

---

### Q6. What does a matrix build do in GitHub Actions?

- A) Builds the project in a matrix/grid format
- B) Runs the same job with different configurations (like multiple Python versions) in parallel ✅
- C) Creates a backup of the build
- D) Runs the build on multiple repositories

> **Explanation:** A matrix build creates multiple parallel job instances with different configuration combinations. For example, testing with Python 3.11 and 3.12 creates two parallel jobs — one for each version.

---

### Q7. What tool is used for fast Python linting in a CI pipeline?

- A) pytest
- B) black
- C) ruff ✅
- D) mypy

> **Explanation:** Ruff is a fast Python linter (written in Rust) that catches code quality issues like unused imports, undefined names, and style violations. Black is for formatting, pytest for testing, and mypy for type checking.

---

### Q8. What does 'pytest --cov=app --cov-fail-under=80' do?

- A) Runs tests and fails if more than 80 tests fail
- B) Runs tests with code coverage and fails if coverage is below 80% ✅
- C) Runs only 80% of the tests
- D) Runs tests on the 80th line of the app

> **Explanation:** The --cov=app flag measures code coverage for the "app" directory, and --cov-fail-under=80 makes the command fail (exit code 1) if less than 80% of the code is covered by tests.

---

### Q9. How do you securely store an API key for use in GitHub Actions?

- A) Put it directly in the workflow YAML file
- B) Store it in a .env file committed to Git
- C) Add it as a GitHub Repository Secret in Settings ✅
- D) Put it in a comment in the code

> **Explanation:** GitHub Repository Secrets are encrypted and stored securely. They are injected into workflows at runtime and automatically masked in logs. Never put secrets in workflow files or committed .env files.

---

### Q10. What is the GITHUB_TOKEN secret?

- A) A token you must manually create and add to secrets
- B) An automatically provided token that lets workflows interact with the GitHub API ✅
- C) Your personal GitHub password
- D) A token for accessing Docker Hub

> **Explanation:** GITHUB_TOKEN is automatically created by GitHub for every workflow run. It allows the workflow to interact with the GitHub API — clone the repo, push to GHCR, comment on PRs, etc. No manual setup is required.

---

### Q11. Which action is used to build and push Docker images to GHCR in CI?

- A) actions/checkout@v4
- B) docker/build-push-action@v6 ✅
- C) actions/setup-python@v5
- D) docker/setup-buildx-action@v3

> **Explanation:** docker/build-push-action@v6 builds Docker images and pushes them to a container registry. It supports features like layer caching (cache-from/cache-to), multi-platform builds, and automatic tagging.

---

### Q12. What does 'cache: pip' do in actions/setup-python?

- A) Installs all pip packages automatically
- B) Caches downloaded pip packages between workflow runs to speed up installation ✅
- C) Removes the pip cache to save space
- D) Creates a backup of pip packages

> **Explanation:** The "cache: pip" option stores downloaded pip packages between workflow runs. Instead of downloading every package from scratch each time (45+ seconds), cached packages are restored instantly (5 seconds).

---

### Q13. What is the simplest rollback strategy when a deployment breaks production?

- A) Delete the entire server and start over
- B) Run 'git revert HEAD' and push, letting CI/CD redeploy the previous working version ✅
- C) Manually edit files on the production server
- D) Wait for the bug to fix itself

> **Explanation:** git revert HEAD creates a new commit that undoes the last change. Pushing this triggers the CI/CD pipeline, which automatically tests, builds, and deploys the reverted code — restoring the previous working state.

---

### Q14. What does branch protection's 'Require status checks to pass' do?

- A) Prevents anyone from creating new branches
- B) Blocks merging a PR until the specified CI jobs pass successfully ✅
- C) Automatically fixes failing tests
- D) Sends an email when tests fail

> **Explanation:** When enabled, the merge button on a PR is disabled until all required status checks (CI jobs) pass. This prevents broken code from being merged into the protected branch.

---

### Q15. Which DORA metric measures how quickly a team can fix production failures?

- A) Deployment Frequency
- B) Lead Time for Changes
- C) Change Failure Rate
- D) Mean Time to Recovery (MTTR) ✅

> **Explanation:** Mean Time to Recovery (MTTR) measures the average time it takes to restore service after a production failure. Elite teams recover in less than 1 hour. It reflects how quickly a team can detect, diagnose, and fix problems.
