# Module 05 — Assignment: Git, GitHub & Professional Workflow

**Deadline:** End of Week 8
**Submission:** GitHub repository links + screenshots of PRs, Actions runs, and project board
**Total Marks:** 100

---

## Task 1: Initialize a Professional Repository — 25 marks

Create a new GitHub repository for a Python project called `techpath-student-manager`.

**Requirements:**

1. **Initialize the repo locally:**
   - Run `git init` and make at least 5 meaningful commits (not "test" or "update")
   - Each commit must follow conventional commit format (`feat:`, `fix:`, `docs:`, `chore:`)
   - Example commits:
     - `chore: initialize project structure`
     - `feat: add student model with name, roll, and course fields`
     - `feat: add function to calculate grade from marks`
     - `docs: add installation instructions to README`
     - `chore: add .gitignore for Python project`

2. **Create a proper `.gitignore`:**
   - Must ignore: `__pycache__/`, `.venv/`, `.env`, `.vscode/`, `*.db`, `*.pyc`
   - Add comments explaining each section

3. **Write a professional README.md:**
   - Project title and one-line description
   - At least 2 badges (Python version, license) using shields.io
   - Features list
   - Installation steps (clone, create venv, install requirements)
   - Usage instructions with code example
   - Project folder structure
   - Contributing section
   - License section

4. **Push to GitHub:**
   - Create a public repository on GitHub
   - Push all commits
   - Verify the README renders correctly on GitHub

**Submission:** GitHub repository URL

---

## Task 2: Branch Workflow & Pull Requests — 25 marks

Using the repository from Task 1, practice a professional branching workflow.

**Requirements:**

1. **Create and merge 3 feature branches:**

   - **Branch 1:** `feature/add-student`
     - Add a function `add_student(name, roll_number, course, city)` in `student_manager.py`
     - Commit: `feat: add student creation function`
     - Create a Pull Request on GitHub with a proper description
     - Merge using "Squash and merge"

   - **Branch 2:** `feature/search-student`
     - Add a function `search_student(roll_number)` that returns student details
     - Commit: `feat: add student search by roll number`
     - Create a Pull Request
     - Merge using "Create a merge commit"

   - **Branch 3:** `feature/display-all`
     - Add a function `display_all_students()` that prints all students in a formatted table
     - Use Indian names: Rahul (Bhopal), Priya (Delhi), Amit (Pune), Sneha (Indore), Karan (Hyderabad)
     - Commit: `feat: add display all students with formatted output`
     - Create a Pull Request
     - Merge using "Rebase and merge"

2. **Create a merge conflict and resolve it:**
   - Create two branches from `main`: `feature/greeting-v1` and `feature/greeting-v2`
   - In both branches, edit the same line in the same file (e.g., a welcome message)
   - Merge `feature/greeting-v1` into `main` first
   - Then try merging `feature/greeting-v2` — a conflict will happen
   - Resolve the conflict manually, commit, and complete the merge
   - Take a screenshot of the conflict in your editor

3. **Use conventional commits throughout:**
   - Every commit must use a proper prefix (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`)

**Submission:** GitHub repository URL + screenshots of all 4 Pull Requests (3 features + 1 conflict resolution)

---

## Task 3: Pre-commit Hooks & Code Quality — 25 marks

Set up automated code quality checks using pre-commit hooks.

**Requirements:**

1. **Create a Python project** with at least 3 files:
   - `app/main.py` — entry point
   - `app/utils.py` — helper functions
   - `app/models.py` — data models (use dataclasses)

2. **Intentionally write messy code** (you will fix it):
   - Unused imports (`import os` when os is not used)
   - Bad formatting (inconsistent spacing, long lines)
   - Unsorted imports (stdlib, third-party, local mixed up)
   - Missing trailing newlines
   - Trailing whitespace

3. **Set up pre-commit hooks:**
   - Install pre-commit: `pip install pre-commit`
   - Create `.pre-commit-config.yaml` with these hooks:
     - `ruff` (linting with auto-fix)
     - `ruff-format` (formatting)
     - `black` (code formatting)
     - `isort` (import sorting, with `--profile black`)
     - `trailing-whitespace` (from pre-commit-hooks)
     - `end-of-file-fixer` (from pre-commit-hooks)
     - `check-yaml` (from pre-commit-hooks)
   - Run `pre-commit install`

4. **Run pre-commit and fix all issues:**
   - Run `pre-commit run --all-files`
   - Take a screenshot showing the first run (some hooks will FAIL)
   - Fix all issues (let ruff and black auto-fix where possible)
   - Run again until all hooks PASS
   - Take a screenshot showing all hooks passing

5. **Commit the clean code:**
   - `chore: add pre-commit hooks configuration`
   - `style: fix all linting and formatting issues`

**Submission:** GitHub repository URL + screenshots of pre-commit output (before and after fixing)

---

## Task 4: GitHub Actions CI Pipeline — 25 marks

Create a working CI/CD pipeline using GitHub Actions.

**Requirements:**

1. **Project setup:**
   - Create a Python project with at least 2 Python files
   - Create `requirements.txt` with: `pytest`, `ruff`, `black`
   - Write at least 3 test functions in `tests/test_app.py`:
     - Test a function that calculates course fee with GST (18%)
     - Test a function that validates email format
     - Test a function that calculates grade from percentage

2. **Create the workflow file** at `.github/workflows/ci.yml`:
   - Name: `TechPath CI Pipeline`
   - Trigger on: push to `main` and `develop`, pull requests to `main`
   - Steps:
     - Checkout code
     - Set up Python 3.11
     - Install dependencies from `requirements.txt`
     - Run `ruff check .`
     - Run `black --check .`
     - Run `pytest -v`

3. **Trigger the pipeline:**
   - Push to GitHub and verify the pipeline runs
   - Take a screenshot of the Actions tab showing a green (passing) run
   - Intentionally break a test, push, and take a screenshot of a red (failing) run
   - Fix the test and push again to get green

4. **Add a status badge** to your README:
   - Copy the badge markdown from Actions tab
   - Add it to the top of your README.md
   - The badge should show "passing" status

**Submission:** GitHub repository URL + screenshots of passing and failing pipeline runs + README with badge

---

## Rubric

| Criteria | Excellent (Full Marks) | Good (75%) | Needs Work (50%) | Incomplete (25%) |
|----------|----------------------|------------|------------------|------------------|
| **Commit quality** | All commits use conventional format with clear, descriptive messages | Most commits follow the format | Some commits are vague or missing prefix | Random or meaningless commit messages |
| **.gitignore & README** | Comprehensive .gitignore with comments; README has badges, structure, installation, usage | .gitignore covers basics; README has most sections | Minimal .gitignore; README is sparse | Missing .gitignore or README |
| **Branching & PRs** | 3+ feature branches with clean PRs, conflict resolved correctly | 2 branches with PRs, conflict attempted | 1 branch, no PR or unresolved conflict | No branches used |
| **Pre-commit hooks** | All hooks configured and passing, before/after screenshots | Most hooks set up, minor issues | Partial setup, some hooks not working | Not attempted or broken config |
| **GitHub Actions** | Working pipeline with pass/fail screenshots and badge in README | Pipeline works but missing screenshots or badge | Pipeline created but has errors | Not attempted |
| **Code quality** | Clean, formatted, linted code throughout all tasks | Mostly clean with minor issues | Several formatting or lint issues | Messy, unformatted code |
