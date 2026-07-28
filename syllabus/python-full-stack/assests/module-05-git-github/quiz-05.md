# Quiz — Git, GitHub & Professional Workflow

**Module 05 | 15 Questions**

---

### Q1. What does `git init` do?

- A) Downloads a repository from GitHub
- B) Creates a new Git repository in the current directory ✅
- C) Pushes code to a remote server
- D) Installs Git on your computer

> **Explanation:** git init initializes a new Git repository in the current directory by creating a hidden .git folder that tracks all version history.

---

### Q2. Which command moves files from the Working Directory to the Staging Area?

- A) git commit
- B) git push
- C) git add ✅
- D) git status

> **Explanation:** git add stages files, marking them as ready to be included in the next commit. git commit then saves the staged changes to the repository.

---

### Q3. What is the purpose of a `.gitignore` file?

- A) To list files that should be deleted from the project
- B) To specify files and folders that Git should NOT track ✅
- C) To ignore error messages in the terminal
- D) To hide files from other team members

> **Explanation:** .gitignore tells Git which files and folders to ignore — typically secrets (.env), dependencies (node_modules, venv), build outputs (dist), and OS files (.DS_Store).

---

### Q4. What happens during a Git merge conflict?

- A) Git automatically picks the newer version
- B) Both versions are deleted
- C) Git marks the conflicting lines and asks you to resolve manually ✅
- D) The merge is cancelled and cannot be completed

> **Explanation:** When two branches modify the same lines of the same file, Git cannot decide which version to keep. It marks the conflicting sections with special markers and waits for you to resolve them manually.

---

### Q5. Which command creates a new branch AND switches to it in one step?

- A) git branch feature/login
- B) git checkout -b feature/login ✅
- C) git merge feature/login
- D) git push origin feature/login

> **Explanation:** git checkout -b creates a new branch and immediately switches to it. The alternative modern syntax is git switch -c. Without -b, git checkout only switches to an existing branch.

---

### Q6. What does `git stash` do?

- A) Permanently deletes uncommitted changes
- B) Pushes changes to a remote branch
- C) Temporarily saves uncommitted changes so you can switch branches ✅
- D) Creates a new commit with all changes

> **Explanation:** git stash saves your uncommitted changes to a temporary storage area. You can then switch branches, do other work, and later restore your stashed changes with git stash pop.

---

### Q7. What is the difference between `git merge` and `git rebase`?

- A) Merge deletes the branch, rebase keeps it
- B) Merge creates a merge commit preserving history, rebase replays commits for a linear history ✅
- C) Merge only works locally, rebase works with remote
- D) There is no difference, they do the same thing

> **Explanation:** Merge preserves the branch structure by creating a merge commit, keeping a non-linear history. Rebase moves your commits on top of another branch, creating a clean linear history but rewriting commit hashes.

---

### Q8. What is a Pull Request (PR) on GitHub?

- A) A command to download code from GitHub
- B) A request to pull data from an API
- C) A proposal to merge changes from one branch into another, with code review ✅
- D) A way to report bugs on a repository

> **Explanation:** A Pull Request is a GitHub feature that lets you propose merging your branch into another branch (usually main). Team members can review the code, leave comments, and approve or request changes before merging.

---

### Q9. What tool does `pre-commit` install as?

- A) A Python linter
- B) A Git hook that runs automatically before each commit ✅
- C) A GitHub Action
- D) A code formatter

> **Explanation:** pre-commit installs as a Git hook — a script that runs automatically before every git commit. If any check fails (linting, formatting, secrets detection), the commit is blocked until the issues are fixed.

---

### Q10. What does the Conventional Commits prefix `fix:` indicate?

- A) A new feature was added
- B) A bug was fixed ✅
- C) Code was reformatted
- D) Documentation was updated

> **Explanation:** In Conventional Commits, fix: indicates a bug fix. Other prefixes: feat: for new features, docs: for documentation, style: for formatting, refactor: for restructuring, test: for tests, chore: for maintenance.

---

### Q11. In a GitHub Actions workflow, what does `needs: lint` mean on a job?

- A) The job requires the lint tool to be installed
- B) The job will only run if the 'lint' job completes successfully ✅
- C) The job needs to run linting before tests
- D) The lint job runs in parallel with this job

> **Explanation:** needs: lint creates a dependency — this job will only start running after the lint job completes successfully. If the lint job fails, this job is skipped. Without needs, jobs run in parallel.

---

### Q12. What is the purpose of `git remote add upstream <url>`?

- A) To push code to a new repository
- B) To add a reference to the original repository when working with a fork ✅
- C) To merge two repositories together
- D) To create a backup of the repository

> **Explanation:** When you fork a repository, 'origin' points to your fork. Adding 'upstream' creates a reference to the original repository so you can fetch its latest changes and keep your fork synchronized.

---

### Q13. What does `ruff` do in a Python project?

- A) Formats code to a consistent style
- B) Runs unit tests
- C) Checks code for errors, style issues, and potential bugs (linting) ✅
- D) Manages Python package dependencies

> **Explanation:** Ruff is a fast Python linter that checks code for errors, unused imports, style violations, potential bugs, and more. It can also auto-fix many issues with the --fix flag.

---

### Q14. Which file in a GitHub repository defines the CI/CD workflow?

- A) .github/workflows/*.yml ✅
- B) .gitignore
- C) package.json
- D) Dockerfile

> **Explanation:** GitHub Actions workflows are defined in YAML files inside the .github/workflows/ directory. GitHub automatically detects and runs these workflows based on their trigger events.

---

### Q15. Why should you NEVER rebase commits that have been pushed to a shared remote branch?

- A) Rebase makes the code run slower
- B) Rebase changes commit hashes, causing conflicts for everyone who has the old commits ✅
- C) Rebase deletes the remote branch
- D) Rebase only works on the main branch

> **Explanation:** Rebase rewrites commit history by creating new commits with different hashes. If others have already pulled the old commits, their history will conflict with the rewritten one, causing a mess for the entire team.

---

**Score Guide:**
- 13-15 correct: Excellent — you are ready for professional Git workflows
- 10-12 correct: Good — review the topics you missed
- 7-9 correct: Fair — practice more with hands-on exercises
- Below 7: Needs improvement — go through each topic again carefully

---

*TechPath Institute — Python Full Stack Development*
