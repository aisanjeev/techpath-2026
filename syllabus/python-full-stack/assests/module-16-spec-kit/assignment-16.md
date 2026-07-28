# Module 16 — Assignment: Build Your Spec-Kit

**Deadline:** End of Week 16
**Submission:** GitHub repository with all documents in a `docs/` folder

---

## Task 1: Write a PRD (30 marks)

Pick one of the following product ideas (or propose your own with instructor approval):

| # | Product Idea | Target Users |
|---|-------------|-------------|
| 1 | **Student Attendance Tracker** — Trainers mark attendance, students see their percentage | Trainers, students, admin at a coaching institute |
| 2 | **Hostel Mess Menu App** — Daily menu display, feedback, meal booking | Hostel students in Bhopal/Pune/Delhi |
| 3 | **Local Shop Inventory Manager** — Track stock, sales, and generate bills | Small shop owners (kirana stores) |
| 4 | **Job Application Tracker** — Track applications, interviews, follow-ups | Fresh graduates looking for their first job |

Using the PRD template from class (`code-prd-template.md`), create a complete PRD that includes:

- [ ] Problem statement with specific pain points (at least 3)
- [ ] At least 2 user personas with Indian names and contexts
- [ ] At least 8 user stories using "As a... I want... so that..." format
- [ ] MoSCoW prioritization (Must/Should/Could/Won't for each story)
- [ ] Acceptance criteria for at least 3 user stories (GIVEN/WHEN/THEN format)
- [ ] Non-functional requirements (performance, security, compatibility)
- [ ] Out of scope section (at least 3 features NOT in this version)
- [ ] 6-week timeline with weekly milestones

**File name:** `docs/PRD.md`

---

## Task 2: Design the API Specification (30 marks)

Create an OpenAPI 3.0 specification (YAML) for your chosen product with:

- [ ] At least 8 API endpoints covering CRUD operations
- [ ] Authentication endpoint (login)
- [ ] At least 3 reusable schemas in `components/schemas`
- [ ] Proper HTTP methods (GET for read, POST for create, PATCH for update, DELETE for remove)
- [ ] Request body examples with Indian-context data
- [ ] Error response schemas (400, 401, 404, 409)
- [ ] Pagination parameters (skip, limit) on list endpoints
- [ ] The spec must render without errors in Swagger Editor (https://editor.swagger.io)

**File name:** `docs/api-spec.yaml`

**Verification:** Paste your YAML into Swagger Editor. Take a screenshot showing it renders without errors. Include the screenshot in your submission.

---

## Task 3: Design the Database Schema (20 marks)

Create a database schema document that includes:

- [ ] ERD (Entity-Relationship Diagram) — use dbdiagram.io or draw.io
  - At least 4 tables
  - Show primary keys, foreign keys, and relationship types (1:N, M:N)
- [ ] Table definitions with column names, types, and constraints
- [ ] SQLAlchemy model code for all tables (Python file)
- [ ] Seed data script with at least 5 records per table (Indian names, Indian cities)
- [ ] Migration plan: what order to create tables (considering foreign key dependencies)

**Files:**
- `docs/database-schema.md` — ERD image/link + table definitions
- `models.py` — SQLAlchemy model code
- `seed_data.py` — Seed data script

---

## Task 4: Sprint Planning Board (20 marks)

Set up a GitHub Projects board for your product:

- [ ] Create a GitHub repository for your capstone project
- [ ] Set up a GitHub Projects board with columns: Backlog, In Progress, In Review, Done
- [ ] Create at least 12 GitHub Issues (one per feature/task)
- [ ] Each issue must have:
  - Clear title
  - Description with acceptance criteria
  - Labels (e.g., `backend`, `frontend`, `bug`, `enhancement`)
  - Assigned to a milestone (Sprint 1 through Sprint 6)
- [ ] Create 6 milestones (Sprint 1 through Sprint 6)
- [ ] Move at least 3 issues to "In Progress" to simulate active sprint

**Submission:** Share the GitHub Projects board link

---

## Grading Rubric

| Criteria | Excellent (90-100%) | Good (70-89%) | Needs Work (<70%) |
|----------|-------------------|---------------|-------------------|
| PRD completeness | All sections filled with specific, measurable details | Most sections filled, some vague | Missing sections or very vague |
| API spec quality | Renders in Swagger Editor, consistent schemas, good examples | Renders but inconsistent or missing examples | Errors in Swagger Editor |
| DB schema | Clear ERD, proper relationships, working SQLAlchemy code | ERD present but relationships unclear | No ERD or broken code |
| Sprint board | 12+ well-written issues with labels and milestones | 8-11 issues, some missing details | Fewer than 8 issues |

**Total: 100 marks**
