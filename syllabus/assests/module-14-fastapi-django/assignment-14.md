# Module 14 — Assignment: Build a REST API

**Deadline:** End of Week 24
**Submission:** Python project folder + Postman screenshots

---

## Build: Student Management REST API with FastAPI

Create a complete REST API for managing students, courses, and marks.

### Task 1: API Setup & CRUD — 35 marks

**Endpoints:**
| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/students` | List all students (with pagination) |
| `GET` | `/api/students/{id}` | Get one student |
| `POST` | `/api/students` | Create a student |
| `PUT` | `/api/students/{id}` | Update a student |
| `DELETE` | `/api/students/{id}` | Delete a student |
| `GET` | `/api/courses` | List all courses |
| `POST` | `/api/courses` | Create a course |

**Requirements:**
- Use Pydantic models for request validation
- Validate: name (2-50 chars), email (valid format), marks (0-100)
- Return proper status codes (201 for create, 404 for not found)
- Use consistent response format: `{"success": true, "data": {...}}`

### Task 2: Database Integration — 25 marks
- Use SQLite with `sqlite3` or SQLAlchemy
- Create tables: `students` and `courses` with foreign key
- All data persists across server restarts
- Use parameterized queries (no f-strings in SQL)

### Task 3: Search & Filter — 20 marks
- `GET /api/students?course=ADCA` — filter by course
- `GET /api/students?city=Bhopal` — filter by city
- `GET /api/students?search=rahul` — search by name
- `GET /api/students?sort=marks&order=desc` — sort
- `GET /api/students?page=1&limit=10` — pagination

### Task 4: Testing with Postman — 20 marks
- Create a Postman collection with all endpoints
- Test each endpoint with valid and invalid data
- Screenshot each request/response
- Test error cases (duplicate email, invalid marks, student not found)

### Project Structure
```
student-api/
├── main.py          (FastAPI app + routes)
├── models.py        (Pydantic schemas)
├── database.py      (SQLite connection + queries)
├── requirements.txt (fastapi, uvicorn)
```

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| CRUD endpoints | All work with proper status codes | Most work | Only GET works |
| Validation | Pydantic models, error messages | Basic validation | No validation |
| Database | SQLite integrated, data persists | In-memory list | No persistence |
| Search/filter | All filters work, pagination | Basic filter | No filtering |
| Testing | Full Postman collection, edge cases | Basic testing | No screenshots |
