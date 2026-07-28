# Module 17 — Assignment: Capstone Project Delivery

**Deadline:** End of Week 17 (progress check); Final submission end of Week 18
**Submission:** GitHub repository link + live deployment URL

---

## Task 1: Backend API with Database (30 marks)

Build a complete backend for your capstone project with:

- [ ] FastAPI or Django project with proper folder structure
- [ ] PostgreSQL database with at least 4 tables (models)
- [ ] Alembic migrations (or Django migrations) — at least 1 initial migration
- [ ] At least 8 API endpoints:
  - 1 authentication endpoint (login)
  - 4 CRUD endpoints (Create, Read, Update, Delete)
  - 1 list endpoint with pagination (skip/limit)
  - 1 filtered query endpoint (filter by batch/city/status/etc.)
  - 1 report/aggregate endpoint (e.g., attendance summary)
- [ ] Pydantic schemas for request validation and response serialization
- [ ] Error handling — 400, 401, 404, 409 responses with clear messages
- [ ] Seed data script with at least 10 records using Indian names and cities
- [ ] Swagger docs accessible at `/docs`

**Verification:** Share a screenshot of Swagger UI showing all endpoints.

---

## Task 2: Frontend with Responsive UI (25 marks)

Build a frontend that connects to your backend API:

- [ ] At least 4 pages/views:
  - Login page
  - Dashboard/home page (shows summary data)
  - Main feature page (e.g., mark attendance, add items, track applications)
  - Report/analytics page
- [ ] Responsive design — works on mobile (375px) and desktop (1280px)
- [ ] Forms with client-side validation (required fields, email format, etc.)
- [ ] Loading states — show "Loading..." while API calls are in progress
- [ ] Error states — show user-friendly messages when API calls fail
- [ ] Uses HTMX or JavaScript `fetch()` to call your API

**Use either:**
- Option A: Standalone HTML/CSS/JS + HTMX (served by FastAPI or separately)
- Option B: Django templates (if using Django backend)

**Verification:** Share screenshots on mobile and desktop showing the same page.

---

## Task 3: AI Feature Integration (25 marks)

Add at least one AI-powered feature using LangChain or LangGraph:

**Option A: RAG Chatbot (Recommended)**
- [ ] Chat interface in the frontend (text input + response area)
- [ ] Backend endpoint that accepts a question and returns an AI answer
- [ ] LangChain chain or LangGraph agent that queries your database
- [ ] System prompt that restricts the AI to your domain (e.g., attendance queries only)
- [ ] At least 3 example queries that work correctly:
  - "What is Rahul's attendance percentage?"
  - "Which students have less than 75% attendance?"
  - "How many classes were held this month?"

**Option B: AI Agent**
- [ ] LangGraph agent with at least 2 tools (e.g., query DB, send notification)
- [ ] Agent can answer multi-step questions
- [ ] Agent has proper error handling (graceful failure when AI service is down)

**Option C: AI Workflow**
- [ ] AI-powered feature (e.g., resume analyzer, sentiment analysis, content generator)
- [ ] Input: user uploads or enters data
- [ ] Output: AI-generated insights displayed in the UI

**Verification:** Record a short screen recording (1-2 minutes) showing the AI feature working with 3 different queries/inputs.

---

## Task 4: CI/CD, Deployment, and Documentation (20 marks)

### CI/CD Pipeline (8 marks)
- [ ] GitHub Actions workflow file (`.github/workflows/ci-cd.yml`)
- [ ] Workflow runs on push to `develop` and PR to `main`
- [ ] At least these checks:
  - Linting (ruff or flake8)
  - Tests (pytest with at least 5 test cases)
  - Coverage report
- [ ] Green checkmark on at least one successful run

### Deployment (6 marks)
- [ ] App deployed and accessible via a public URL
- [ ] Database running in production (Render PostgreSQL, Supabase, or Neon)
- [ ] Environment variables properly configured (not hardcoded)
- [ ] Health check endpoint returns 200 OK

### Documentation (6 marks)
- [ ] Professional README.md with:
  - Project description (2-3 sentences)
  - Live demo link
  - Tech stack table
  - Setup instructions (clone, install, configure, run)
  - Screenshots of the app
  - Architecture diagram
  - Author info with GitHub and LinkedIn links
- [ ] `.env.example` file with all required environment variables (no real values)
- [ ] API documentation accessible via Swagger UI at `/docs`

**Verification:** Share the GitHub repo URL and the live deployment URL.

---

## Grading Rubric

| Category | Excellent (90-100%) | Good (70-89%) | Needs Work (<70%) |
|----------|-------------------|---------------|-------------------|
| Backend | 8+ endpoints, clean code, proper error handling, seed data | 5-7 endpoints, basic error handling | Fewer than 5 endpoints, no validation |
| Frontend | 4+ pages, responsive, good UX, loading/error states | 3 pages, mostly responsive | Fewer than 3 pages, not responsive |
| AI Feature | Working AI with 3+ demo queries, proper prompt engineering | AI works but limited queries | AI feature broken or placeholder only |
| CI/CD + Deploy | Pipeline green, app live, good README | Pipeline exists but has issues, app deployed | No pipeline, not deployed |

**Total: 100 marks**

---

## Bonus Points (Up to 10 extra marks)

- [ ] +3: Authentication with JWT (login required for protected pages)
- [ ] +2: Rate limiting on API endpoints
- [ ] +2: Comprehensive test suite (10+ test cases with 70%+ coverage)
- [ ] +3: Custom domain name configured (e.g., myapp.techpath.biz)
