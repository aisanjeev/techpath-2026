# Module 15 — Assignment: Complete Spec-Kit + Deployment

**Deadline:** End of Week 26
**Submission:** GitHub repo + deployed URLs + spec-kit document

---

## Build a Complete Project Spec-Kit

Choose one of your previous projects (portfolio website, student API, expense tracker) OR build a new small project, and create a full spec-kit around it.

### Task 1: Project Documentation — 25 marks

Create these documents in your repo:

**README.md** — must include:
- Project name and description
- Tech stack list
- Setup instructions (step-by-step)
- API endpoints table (if applicable)
- Screenshots (at least 2)
- Author and license

**SPEC.md** — must include:
- Problem statement (what this solves)
- Target users
- Feature list (MVP vs Nice-to-Have)
- User stories (at least 5)
- Tech stack decisions with reasons (why FastAPI over Django, why SQLite, etc.)
- Database schema (table diagrams)
- API design (endpoints + request/response examples)

### Task 2: Git Workflow — 25 marks

Demonstrate proper Git usage:
- At least 10 meaningful commits (not "update", "fix", but descriptive messages)
- Use at least 2 branches (main + feature branch)
- Create a Pull Request on GitHub and merge it
- Proper `.gitignore` (no `__pycache__`, `.env`, `node_modules`)
- No secrets committed (check with `git log --all -p | grep -i "password\|secret\|key"`)

### Task 3: Deployment — 30 marks

Deploy your project live:

**Frontend** (if applicable):
- Deploy to GitHub Pages or Vercel
- Working live URL
- Responsive on mobile

**Backend API** (if applicable):
- Deploy to Railway, Render, or PythonAnywhere
- API accessible from the live URL
- Environment variables configured (not hardcoded secrets)

### Task 4: Docker (Bonus) — 20 marks

Create a `Dockerfile` that:
- Uses `python:3.11-slim` base image
- Installs dependencies from `requirements.txt`
- Runs the server with `uvicorn`
- Works with `docker build` and `docker run`

Create a `docker-compose.yml` if your project has multiple services.

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Documentation | Complete README + SPEC | README only | No documentation |
| Git history | Meaningful commits, branches, PR | Commits exist | Single commit |
| Deployment | Live + working + env vars | Live but broken | Not deployed |
| .gitignore | Proper exclusions, no secrets | Basic .gitignore | Missing or has secrets |
| Docker | Dockerfile + compose work | Dockerfile only | No Docker |
