# Spec-Kit & Project Documentation

**Module 15 — Spec-Kit Development | Topic 1**

---

## What is a Spec-Kit?

A **Spec-Kit** is a complete delivery package for your project. Think of it as the "user manual + blueprint + handover folder" for your software.

| Part | What It Contains |
|------|-----------------|
| **README.md** | Project overview, setup instructions, screenshots |
| **Technical Spec** | Architecture, tech stack, API docs |
| **Setup Guide** | How to install and run the project |
| **Folder Structure** | Map of files and what each does |
| **Environment Config** | .env example with all required variables |
| **Demo/Screenshots** | Visual proof that it works |

> A project without documentation is like a phone without a manual — nobody knows how to use it.

---

## Writing a Great README.md

Every project on GitHub needs a README. Here's the template:

```markdown
# Project Name

One line description of what it does.

## Screenshots

![Home Page](screenshots/home.png)

## Features

- Feature 1
- Feature 2
- Feature 3

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- Database: SQLite

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Installation

1. Clone the repo
   ```bash
   git clone https://github.com/username/project.git
   cd project
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

4. Run the app
   ```bash
   python main.py
   ```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/users | List all users |
| POST | /api/users | Create user |

## Contributing

Pull requests are welcome!

## License

MIT
```

### README Tips

| Do | Don't |
|----|-------|
| Add screenshots | Leave it empty |
| List all setup steps | Assume people know |
| Include .env.example | Share real secrets |
| Write in simple English | Use complex jargon |
| Keep it updated | Let it go stale |

---

## Technical Specification Document

A tech spec explains **how** your project is built (for developers, not users).

### Template

```markdown
# Technical Specification: [Project Name]

## 1. Overview
What the project does and why it exists.

## 2. Architecture
```
Frontend (React) → API (FastAPI) → Database (PostgreSQL)
```

## 3. Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Auth | Firebase |
| Hosting | Vercel + Render |

## 4. Database Schema
- users: id, name, email, role, created_at
- posts: id, title, body, user_id, created_at

## 5. API Design
- GET /api/posts — list all posts
- POST /api/posts — create post (auth required)
- PUT /api/posts/:id — update post

## 6. Authentication
JWT token-based. Firebase handles sign-in,
backend verifies token.

## 7. Folder Structure
```
project/
├── frontend/
│   ├── src/
│   └── public/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   └── tests/
└── README.md
```
```

---

## Environment Variables & Secrets

### What Are Environment Variables?

Settings stored **outside** your code — so you can change them without editing code.

```bash
# .env file
DATABASE_URL=sqlite:///./data/app.db
SECRET_KEY=my-super-secret-key-123
API_KEY=abc123xyz
DEBUG=true
PORT=8000
```

### Rules

| Rule | Why |
|------|-----|
| **Never commit .env** | Contains passwords and secrets |
| **Add .env to .gitignore** | Prevents accidental upload |
| **Create .env.example** | Shows what variables are needed (without real values) |
| **Use different values** per environment | Dev, staging, production |

### .env.example (safe to commit)

```bash
# Copy this to .env and fill in real values
DATABASE_URL=sqlite:///./data/app.db
SECRET_KEY=change-me-to-random-string
API_KEY=your-api-key-here
DEBUG=true
```

### .gitignore Must-Haves

```
.env
.env.local
*.db
node_modules/
__pycache__/
.venv/
```

---

## Folder Structure Best Practices

```
my-project/
├── README.md           ← Project overview
├── .env.example        ← Environment template
├── .gitignore          ← Files to exclude from git
├── requirements.txt    ← Python dependencies
├── package.json        ← JS dependencies
│
├── docs/               ← Documentation
│   ├── tech-spec.md
│   └── api-docs.md
│
├── src/                ← Source code
│   ├── models/         ← Database models
│   ├── routes/         ← API endpoints
│   ├── services/       ← Business logic
│   └── utils/          ← Helper functions
│
├── tests/              ← Tests
│   ├── test_routes.py
│   └── test_models.py
│
└── screenshots/        ← Demo images
    ├── home.png
    └── dashboard.png
```

---

## Summary

- **Spec-Kit** = complete project delivery package (README + docs + config)
- **README.md** = first thing anyone sees — make it clear and complete
- **Tech spec** = architecture + stack + API design for developers
- **.env files** store secrets — never commit them, use .env.example instead
- **.gitignore** prevents accidental upload of sensitive files
- Good documentation makes your project look professional
