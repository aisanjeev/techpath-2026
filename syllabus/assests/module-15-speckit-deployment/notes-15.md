# Module 15 — Spec-Kit Development & Deployment — Quick Revision Notes

---

## What is a Spec-Kit?
- A **specification kit** is a complete project plan + documentation package
- Contains: PRD (Product Requirements), wireframes, tech stack decisions, API specs, deployment plan
- Used in real companies before building software

## Project Planning Documents

### PRD (Product Requirements Document)
```markdown
## Product Name: [Name]
## Problem: What problem does it solve?
## Target Users: Who will use it?
## Features:
  - Must Have (MVP)
  - Nice to Have (v2)
## Tech Stack: Frontend, Backend, Database
## Timeline: Week-by-week milestones
```

### User Stories
```
As a [user type], I want to [action], so that [benefit].

Example:
As a student, I want to track my attendance, so that I know my percentage.
As an admin, I want to add courses, so that students can enroll.
```

---

## Git & GitHub

### Essential Commands
```bash
git init                          # start tracking
git status                        # check current state
git add .                         # stage all changes
git commit -m "message"           # save snapshot
git log --oneline                 # view history
git push origin main              # upload to GitHub
git pull origin main              # download latest
git branch feature-name           # create branch
git checkout feature-name         # switch branch
git merge feature-name            # merge into current
```

### Git Workflow
```
main (production) ← develop ← feature-branch
1. Create branch: git branch feature-login
2. Switch to it: git checkout feature-login
3. Write code + commit
4. Switch to main: git checkout main
5. Merge: git merge feature-login
6. Push: git push origin main
```

### .gitignore
```
# Python
__pycache__/
*.pyc
.env
venv/

# Node
node_modules/
.next/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## Deployment

### GitHub Pages (Static Sites)
- Free hosting for HTML/CSS/JS
- Settings → Pages → Source: main
- URL: `username.github.io/repo-name`

### Vercel (Frontend)
- Connect GitHub repo → auto-deploy on push
- Great for: Next.js, Astro, React
- Free `.vercel.app` domain

### Railway / Render (Backend)
- Connect GitHub → auto-deploy
- Supports: Python, Node.js, Docker
- Free tier available

### VPS (Full Control)
```bash
# SSH into server
ssh user@your-server-ip

# Pull latest code
cd /path/to/project
git pull origin main

# Restart service
sudo systemctl restart myapp
```

---

## Docker Basics

### Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Commands
```bash
docker build -t myapp .            # build image
docker run -p 8000:8000 myapp      # run container
docker ps                          # list running
docker stop container_id           # stop
docker-compose up                  # run with compose
```

### docker-compose.yml
```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./data/app.db
    volumes:
      - ./data:/app/data
```

---

## Environment Variables
```bash
# .env file (NEVER commit this)
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key
DEBUG=true
API_KEY=abc123
```

```python
# Python — reading env vars
import os
from dotenv import load_dotenv

load_dotenv()
secret = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG", "false") == "true"
```

---

## README Template
```markdown
# Project Name

Short description of what it does.

## Tech Stack
- Frontend: HTML/CSS/Tailwind
- Backend: FastAPI + SQLite
- Deployment: Vercel + Railway

## Setup
1. Clone: `git clone url`
2. Install: `pip install -r requirements.txt`
3. Run: `uvicorn main:app --reload`

## API Endpoints
| Method | URL | Description |
|--------|-----|-------------|

## Screenshots
```
