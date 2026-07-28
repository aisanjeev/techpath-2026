# Module 16: Spec-Kit Development Methodology

## 1. What is a Spec-Kit?

A **Spec-Kit** is a complete documentation package that transforms a vague product idea into an actionable build plan. Think of it as a blueprint — just like a builder needs an architectural drawing before laying bricks, a developer needs a Spec-Kit before writing code.

### The Spec-Kit Pipeline

```
Idea → PRD → System Design → API Spec → DB Schema → Sprint Plan → Build → Deploy
```

| Document | Purpose | Who Reads It |
|----------|---------|--------------|
| PRD (Product Requirements Document) | What to build and why | Everyone — business, design, dev |
| System Design Doc | How the system works internally | Developers, architects |
| API Specification (OpenAPI) | Exact request/response contracts | Frontend + backend devs |
| Database Schema (ERD) | Data structure and relationships | Backend devs, DBAs |
| Sprint Plan | What gets built when | Project manager, dev team |
| Deployment Checklist | How to ship safely | DevOps, lead developer |

### Why Spec-Kit Matters

Without a Spec-Kit, teams often face:
- **Scope creep** — features keep getting added mid-build
- **Miscommunication** — frontend and backend disagree on API shape
- **Rework** — database redesigns after half the code is written
- **Missed deadlines** — no clear plan means no clear timeline

> **Real-world example:** Rahul and Priya are building a student attendance app for TechPath Institute. Without a Spec-Kit, Rahul builds a REST API returning `{present: true}` while Priya's React app expects `{status: "present", timestamp: "..."}`. Two days of rework.

---

## 2. Writing a PRD (Product Requirements Document)

A PRD answers: **What are we building, for whom, and why?**

### PRD Structure

```markdown
# Product Requirements Document: [Product Name]

## 1. Overview
One paragraph explaining what this product does.

## 2. Problem Statement
What pain point does this solve? Who has this problem?

## 3. Target Users
- Primary: [who]
- Secondary: [who]

## 4. User Stories
- As a [user type], I want to [action] so that [benefit].

## 5. Functional Requirements
| ID  | Feature | Priority | Description |
|-----|---------|----------|-------------|
| FR1 | Login   | Must     | Users can sign in with email/password |

## 6. Non-Functional Requirements
- Performance: Page load under 2 seconds
- Security: Passwords hashed with bcrypt
- Availability: 99.5% uptime

## 7. Acceptance Criteria
- [ ] User can register with email
- [ ] User receives confirmation email
- [ ] User can log in after verification

## 8. Out of Scope
Features we are NOT building in this version.

## 9. Timeline
Milestone dates and delivery expectations.
```

### User Stories — The Building Block

A user story follows this format:

```
As a [user type], I want to [action] so that [benefit].
```

**Good Examples (Indian Context):**

| User Story | Priority |
|-----------|----------|
| As a student, I want to view my attendance percentage so that I can track my eligibility for exams | Must Have |
| As a trainer, I want to mark attendance for my batch so that records are digital and accurate | Must Have |
| As an admin, I want to download attendance reports in Excel so that I can share with management | Should Have |
| As a student, I want to receive a WhatsApp notification when my attendance drops below 75% so that I can improve before it's too late | Could Have |

### MoSCoW Prioritization

| Priority | Meaning | Example |
|----------|---------|---------|
| **Must Have** | App is broken without it | User login, attendance marking |
| **Should Have** | Important but app works without it | Excel export, search/filter |
| **Could Have** | Nice addition if time permits | Dark mode, WhatsApp alerts |
| **Won't Have** | Not in this version | Mobile app, AI predictions |

### Acceptance Criteria

Each user story needs measurable acceptance criteria:

```markdown
### User Story: Student views attendance

**Acceptance Criteria:**
- [ ] Student sees a table with date, subject, status (Present/Absent)
- [ ] Attendance percentage is calculated and shown at the top
- [ ] Data loads within 2 seconds
- [ ] Empty state shows "No attendance records yet" message
- [ ] Works on mobile (responsive table)
```

---

## 3. System Design Document

The system design doc explains **how** the product works technically.

### Architecture Diagram

A typical full-stack architecture:

```
┌─────────────┐     HTTPS      ┌─────────────────┐     SQL      ┌────────────┐
│   Browser   │ ──────────────→ │   FastAPI/Django │ ───────────→ │ PostgreSQL │
│  (React/    │                 │   Backend        │              │ Database   │
│   HTMX)     │ ←────────────── │                  │ ←─────────── │            │
└─────────────┘    JSON         │  + Redis Cache   │              └────────────┘
                                │  + AI Service    │
                                └─────────────────┘
                                       │
                                       │ API Key
                                       ▼
                                ┌─────────────────┐
                                │  OpenAI / Azure  │
                                │  AI API          │
                                └─────────────────┘
```

### Tech Stack Decision Table

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | HTML/CSS/JS + HTMX | Simple, fast, no build step |
| Backend | FastAPI | Async, fast, auto-docs, Python |
| Database | PostgreSQL | Robust, free, full-featured |
| Cache | Redis | Session storage, rate limiting |
| AI | LangChain + OpenAI | RAG chatbot, structured output |
| Deployment | Azure / Render | Free tier available, CI/CD support |
| CI/CD | GitHub Actions | Free for public repos, easy setup |

### Data Models

Define your models before writing a single line of code:

```python
# models.py — Data model definitions

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(15))
    batch = Column(String(50))          # e.g., "Python-Batch-2026-July"
    city = Column(String(50))           # e.g., "Bhopal", "Pune", "Delhi"
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    attendances = relationship("Attendance", back_populates="student")

class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String(10), nullable=False)  # "present" or "absent"
    marked_by = Column(String(100))               # trainer name
    
    student = relationship("Student", back_populates="attendances")
```

### API Contracts

Define every endpoint before coding:

| Method | Endpoint | Request Body | Response | Auth |
|--------|----------|-------------|----------|------|
| POST | `/api/v1/auth/login` | `{email, password}` | `{token, user}` | No |
| GET | `/api/v1/students` | — | `[{id, name, ...}]` | Admin |
| GET | `/api/v1/students/{id}/attendance` | — | `[{date, status}]` | Student/Admin |
| POST | `/api/v1/attendance` | `{student_id, date, status}` | `{id, ...}` | Trainer |
| GET | `/api/v1/reports/attendance` | `?batch=...&month=...` | `[{name, percentage}]` | Admin |

---

## 4. API Spec First — OpenAPI / Swagger

**API-first development** means writing the API specification (OpenAPI/Swagger) before writing any backend code. This ensures frontend and backend teams agree on the contract.

### What is OpenAPI?

OpenAPI (formerly Swagger) is a standard format to describe REST APIs using YAML or JSON.

```yaml
openapi: 3.0.3
info:
  title: TechPath Attendance API
  version: 1.0.0
  description: API for managing student attendance at TechPath Institute

servers:
  - url: http://localhost:8000/api/v1
    description: Local development
  - url: https://api.techpath.biz/api/v1
    description: Production

paths:
  /students:
    get:
      summary: List all students
      tags: [Students]
      parameters:
        - name: batch
          in: query
          schema:
            type: string
          description: Filter by batch name
        - name: skip
          in: query
          schema:
            type: integer
            default: 0
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        "200":
          description: List of students
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/Student"
                      
components:
  schemas:
    Student:
      type: object
      required: [name, email]
      properties:
        id:
          type: integer
          example: 1
        name:
          type: string
          example: "Rahul Sharma"
        email:
          type: string
          format: email
          example: "rahul@example.com"
        batch:
          type: string
          example: "Python-Batch-2026-July"
        city:
          type: string
          example: "Bhopal"
```

### Benefits of API-First

1. **Frontend can start early** — use mock data matching the schema
2. **Auto-generated docs** — Swagger UI, ReDoc
3. **Client code generation** — auto-generate TypeScript types
4. **Validation** — request/response validation for free
5. **Contract testing** — verify API matches the spec

### Tools for API Design

| Tool | Use | Link |
|------|-----|------|
| Swagger Editor | Write and preview OpenAPI specs | https://editor.swagger.io |
| Stoplight Studio | Visual API designer (free) | https://stoplight.io/studio |
| FastAPI | Auto-generates OpenAPI from Python code | Built-in at `/docs` |
| Postman | Test APIs interactively | https://www.postman.com |

---

## 5. Database Schema Design

### Entity-Relationship Diagram (ERD)

An ERD shows tables, columns, and relationships visually.

```
┌─────────────┐       ┌──────────────┐       ┌────────────┐
│   students  │       │  attendances │       │   batches  │
├─────────────┤       ├──────────────┤       ├────────────┤
│ id (PK)     │──┐    │ id (PK)      │   ┌──│ id (PK)    │
│ name        │  └───→│ student_id(FK)│   │  │ name       │
│ email       │       │ date         │   │  │ trainer_id │
│ batch_id(FK)│───────│ status       │   │  │ start_date │
│ phone       │       │ marked_by    │   │  │ end_date   │
│ city        │       └──────────────┘   │  │ city       │
│ is_active   │                          │  └────────────┘
└─────────────┘──────────────────────────┘
```

### Relationship Types

| Type | Example | SQLAlchemy |
|------|---------|-----------|
| One-to-Many | One batch has many students | `relationship("Student", back_populates="batch")` |
| Many-to-Many | Students can have many subjects, subjects have many students | Association table + `secondary=` |
| One-to-One | One student has one profile | `uselist=False` in relationship |

### Migration Plan

Using Alembic (SQLAlchemy's migration tool):

```bash
# Step 1: Create initial migration
alembic revision --autogenerate -m "create students and attendance tables"

# Step 2: Review the generated migration file
# Check the upgrade() and downgrade() functions

# Step 3: Apply migration
alembic upgrade head

# Step 4: If something goes wrong, rollback
alembic downgrade -1
```

### Seed Data Strategy

Always prepare seed data for development and testing:

```python
# seed_data.py — Sample data for development

students_data = [
    {"name": "Rahul Sharma", "email": "rahul@example.com", "batch": "PFS-2026-July", "city": "Bhopal"},
    {"name": "Priya Patel", "email": "priya@example.com", "batch": "PFS-2026-July", "city": "Pune"},
    {"name": "Ananya Gupta", "email": "ananya@example.com", "batch": "PFS-2026-July", "city": "Delhi"},
    {"name": "Vikram Singh", "email": "vikram@example.com", "batch": "PFS-2026-Aug", "city": "Jaipur"},
    {"name": "Neha Reddy", "email": "neha@example.com", "batch": "PFS-2026-Aug", "city": "Hyderabad"},
]

attendance_data = [
    {"student_id": 1, "date": "2026-07-01", "status": "present", "marked_by": "Amit Sir"},
    {"student_id": 1, "date": "2026-07-02", "status": "present", "marked_by": "Amit Sir"},
    {"student_id": 1, "date": "2026-07-03", "status": "absent", "marked_by": "Amit Sir"},
    {"student_id": 2, "date": "2026-07-01", "status": "present", "marked_by": "Amit Sir"},
    {"student_id": 2, "date": "2026-07-02", "status": "absent", "marked_by": "Amit Sir"},
]
```

### Test Data Strategy

| Data Type | Purpose | Example |
|-----------|---------|---------|
| Seed data | Dev environment, demos | 5-10 realistic records |
| Fixture data | Automated tests | Known, predictable data |
| Edge case data | Break things intentionally | Empty strings, max-length values, Unicode names |
| Performance data | Load testing | 10,000+ records via scripts |

---

## 6. Sprint Planning

### Agile with a Small Team (2-Person Team)

You do not need a massive Scrum process. For a 2-person team:

| Concept | What We Do |
|---------|-----------|
| Sprint | 1-week cycles |
| Backlog | GitHub Issues list |
| Sprint Board | GitHub Projects (Kanban) |
| Daily Standup | Quick 5-min chat or async message |
| Sprint Review | Demo what you built at week end |
| Retro | "What went well? What didn't? What to change?" |

### GitHub Projects — Kanban Board

Set up columns:
```
📋 Backlog → 🏗️ In Progress → 👀 In Review → ✅ Done
```

### Writing Good GitHub Issues

```markdown
## Title: Add student attendance API endpoint

### Description
Create a POST endpoint at `/api/v1/attendance` that allows trainers
to mark student attendance.

### Acceptance Criteria
- [ ] Endpoint accepts `{student_id, date, status}` in request body
- [ ] Returns 201 with the created attendance record
- [ ] Returns 404 if student_id doesn't exist
- [ ] Returns 400 if status is not "present" or "absent"
- [ ] Only authenticated trainers can access (403 for students)

### Labels
`backend`, `api`, `priority: high`

### Milestone
Sprint 2 — Core API
```

### Milestones for a Full-Stack Project

| Sprint | Focus | Duration |
|--------|-------|----------|
| Sprint 1 | Setup: project, DB, auth | 1 week |
| Sprint 2 | Core API endpoints (CRUD) | 1 week |
| Sprint 3 | Frontend pages + API integration | 1 week |
| Sprint 4 | AI feature + testing | 1 week |
| Sprint 5 | CI/CD + deployment + polish | 1 week |
| Sprint 6 | Bug fixes, docs, demo prep | 1 week |

---

## 7. Code Review Checklist

### Clean Code Principles

| Principle | Bad Example | Good Example |
|-----------|------------|-------------|
| Meaningful names | `def f(x):` | `def calculate_attendance_percentage(student):` |
| Small functions | 100-line function | Functions under 20 lines each |
| No magic numbers | `if count > 75:` | `MINIMUM_ATTENDANCE = 75; if count > MINIMUM_ATTENDANCE:` |
| DRY (Don't Repeat Yourself) | Copy-paste same validation in 5 endpoints | Extract to a shared function |
| Single Responsibility | One function does DB + validation + email | Split into separate functions |

### SOLID Principles (Simplified)

| Principle | Plain English | Example |
|-----------|--------------|---------|
| **S** — Single Responsibility | Each class does one thing | `AttendanceService` only handles attendance logic |
| **O** — Open/Closed | Add features by extending, not modifying existing code | Use base classes, not if-else chains |
| **L** — Liskov Substitution | Subclasses should work where parent class works | If `EmailNotifier` works, `WhatsAppNotifier` should too |
| **I** — Interface Segregation | Don't force classes to implement methods they don't need | Separate `Readable` and `Writable` interfaces |
| **D** — Dependency Inversion | Depend on abstractions, not concrete classes | Pass `NotifierBase` not `EmailNotifier` directly |

### Code Review Checklist Template

```markdown
## Code Review Checklist

### Correctness
- [ ] Code does what the issue/ticket asks
- [ ] Edge cases handled (empty input, None, large data)
- [ ] Error messages are helpful to the user

### Security
- [ ] No hardcoded passwords, API keys, or secrets
- [ ] User input is validated and sanitized
- [ ] SQL queries use parameterized statements (no raw SQL with f-strings)
- [ ] Authentication checked on protected endpoints

### Code Quality
- [ ] Functions are small and focused (under 20 lines ideal)
- [ ] Variable names are descriptive
- [ ] No commented-out code left behind
- [ ] No print() statements in production code (use logging)

### Testing
- [ ] Unit tests written for new functions
- [ ] Edge case tests included
- [ ] All existing tests still pass

### Documentation
- [ ] Docstrings on public functions
- [ ] README updated if setup steps changed
- [ ] API docs (Swagger) reflect new endpoints
```

---

## 8. Deployment Checklist & Post-Launch

### Pre-Deployment Checklist

```markdown
## Deployment Checklist

### Code Ready
- [ ] All tests pass (`pytest --cov=app`)
- [ ] No linting errors (`ruff check app`)
- [ ] Type checking passes (`mypy app`)
- [ ] Code reviewed and approved

### Configuration
- [ ] Environment variables set on server (.env)
- [ ] Database migrations prepared
- [ ] Static files collected/built
- [ ] CORS settings correct for production domain

### Security
- [ ] DEBUG = False in production
- [ ] SECRET_KEY is strong and unique
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] CORS allows only your frontend domain

### Deployment Steps
1. Push code to `main` branch
2. CI/CD pipeline runs tests
3. Build Docker image (if using containers)
4. Deploy to server
5. Run database migrations: `alembic upgrade head`
6. Verify health check endpoint: `GET /api/v1/health`
7. Smoke test critical flows (login, main feature)
```

### Post-Launch Monitoring

| What to Monitor | Tool | Why |
|----------------|------|-----|
| Server uptime | UptimeRobot (free) | Know when your app goes down |
| Error tracking | Sentry (free tier) | Catch and fix bugs fast |
| API response times | FastAPI built-in `/docs` | Spot slow endpoints |
| Database performance | pgAdmin / DBeaver | Watch slow queries |
| Disk space | Server alerts | Logs and uploads fill up fast |

### Incident Response Basics

When something breaks in production:

```
1. DETECT  — Alert from monitoring tool
2. ASSESS  — How bad is it? Who is affected?
3. COMMUNICATE — Tell users: "We're aware and fixing it"
4. FIX     — Deploy hotfix or rollback
5. VERIFY  — Confirm fix works in production
6. REVIEW  — Write a post-mortem: what happened, why, how to prevent
```

### Post-Mortem Template

```markdown
# Incident Report: [Title]

**Date:** 2026-07-25
**Duration:** 45 minutes
**Severity:** High (users could not log in)

## Summary
The login endpoint returned 500 errors after deploying v2.3.0.

## Root Cause
A missing environment variable (FIREBASE_PROJECT_ID) on the
production server caused Firebase token verification to fail.

## Timeline
- 10:00 — Deployed v2.3.0
- 10:05 — UptimeRobot alert: 500 errors on /api/v1/auth/login
- 10:10 — Checked server logs, found Firebase initialization error
- 10:20 — Added missing env variable, restarted server
- 10:25 — Login working again
- 10:45 — Verified all users can log in

## Action Items
- [ ] Add env variable validation on server startup
- [ ] Add deployment checklist item: verify all env vars
- [ ] Add integration test for login flow in CI pipeline
```

---

## Summary

| Step | Document | Key Question |
|------|----------|-------------|
| 1 | PRD | What are we building and why? |
| 2 | System Design | How does it work technically? |
| 3 | API Spec | What do the endpoints look like? |
| 4 | DB Schema | How is data structured? |
| 5 | Sprint Plan | What gets built when? |
| 6 | Code Review | Is the code clean and secure? |
| 7 | Deploy Checklist | Is it safe to ship? |
| 8 | Post-Launch | How do we monitor and respond? |

The Spec-Kit is your professional toolkit. Every company you join will use some version of this process. Master it now, and you will stand out as a developer who can plan, not just code.
