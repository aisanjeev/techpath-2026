# Module 06 — Assignment: Build a Complete REST API with FastAPI

**Deadline:** End of Week 12
**Submission:** Python project folder + Swagger UI screenshots + test report
**Total Marks:** 100

---

## Task 1: Student Management CRUD API — 30 marks

Build a complete REST API for managing students at TechPath Institute using FastAPI and SQLAlchemy.

### Endpoints Required

| Method | URL | Description | Status Code |
|--------|-----|-------------|-------------|
| `POST` | `/api/students` | Create a new student | 201 |
| `GET` | `/api/students` | List all students (with pagination) | 200 |
| `GET` | `/api/students/{id}` | Get a single student by ID | 200 |
| `PUT` | `/api/students/{id}` | Update a student (partial update) | 200 |
| `DELETE` | `/api/students/{id}` | Delete a student | 200 |
| `GET` | `/api/stats` | Get summary statistics | 200 |

### Requirements

- **Database:** Use SQLAlchemy with SQLite (async). Create `Student` and `Course` models with a foreign key relationship.
- **Pydantic Validation:**
  - `name`: 2-100 characters, cannot be blank
  - `email`: must contain `@` and a domain, must be unique
  - `marks`: 0-100 range
  - `phone`: optional, must start with `+91` if provided
  - `city`: default to `"Bhopal"`
- **Search & Filter:**
  - `?search=rahul` — search by name (case-insensitive)
  - `?city=Bhopal` — filter by city
  - `?course_id=1` — filter by course
  - `?sort=marks&order=desc` — sort by any column
  - `?skip=0&limit=10` — pagination
- **Consistent response format:** All endpoints must return `{"success": true, "data": ...}` or `{"success": true, "message": "..."}`
- **Error handling:** Return 404 for not found, 409 for duplicate email, 422 for validation errors
- **Seed data:** At least 8 students with Indian names (Rahul, Priya, Amit, Sneha, Vikram, Ananya, Karan, Neha) and Indian cities (Bhopal, Delhi, Pune, Indore, Hyderabad)
- **Stats endpoint:** Return total students, average marks, highest marks, and city-wise student count

### What to Submit
- `main.py` (or organized in multiple files)
- Swagger UI screenshots for: create, list with filters, get by ID, update, delete, and validation error

---

## Task 2: JWT Authentication — 25 marks

Add authentication to your API using JWT tokens.

### Endpoints Required

| Method | URL | Description | Auth |
|--------|-----|-------------|------|
| `POST` | `/api/register` | Register a new user | Public |
| `POST` | `/api/login` | Login and get JWT token | Public |
| `GET` | `/api/me` | Get current user profile | Token required |
| `PUT` | `/api/me` | Update own profile | Token required |
| `GET` | `/api/users` | List all users | Admin only |
| `DELETE` | `/api/users/{id}` | Delete a user | Admin only |

### Requirements

- **Password hashing:** Use `passlib` with bcrypt. Never store plain text passwords.
- **JWT tokens:** Use `python-jose` to create and verify tokens.
  - Token payload must include: `sub` (email), `role`, `exp` (expiry)
  - Token expires after 60 minutes
- **OAuth2PasswordBearer:** Use FastAPI's built-in OAuth2 flow so Swagger UI has a login button
- **Dependencies:**
  - `get_current_user` — extracts token, verifies it, returns user
  - `get_admin_user` — checks if current user has admin role
- **Role-based access:**
  - Students can: register, login, view/update own profile
  - Admins can: everything students can + list all users + delete users
- **Sample users seeded on startup:**
  - Rahul Sharma (admin): rahul@techpath.biz / rahul123
  - Priya Patel (student): priya@techpath.biz / priya123
- **Protect student CRUD routes:** Only logged-in users can create/update/delete students. Anyone can list/view.

### What to Submit
- Auth-related code files
- Swagger UI screenshots showing: register, login (with token), access protected route, admin-only route, 401 error (no token), 403 error (student tries admin route)

---

## Task 3: File Upload, Background Tasks, and WebSocket — 25 marks

Add advanced features to your API.

### Part A: File Upload (10 marks)

| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/students/{id}/photo` | Upload student photo |
| `GET` | `/api/students/{id}/photo` | Get student photo URL |

Requirements:
- Accept only JPEG, PNG, and WebP images
- Maximum file size: 2 MB
- Save files to an `uploads/` folder with unique filenames
- Return the file path and size in the response
- Return 400 error for invalid file type or oversized file

### Part B: Background Tasks (5 marks)

When a new student is created:
- Send a "welcome email" in the background (mock it with a `print()` and a `time.sleep(2)` to simulate delay)
- Log the creation to an `activity.log` file with timestamp, student name, and action
- The API response must return immediately without waiting for the email

### Part C: WebSocket Chat (10 marks)

| Type | URL | Description |
|------|-----|-------------|
| WebSocket | `/ws/chat` | Real-time chat room |

Requirements:
- Use the Connection Manager pattern
- Accept a `username` query parameter
- Broadcast join/leave messages to all connected users
- Broadcast chat messages to all connected users
- Handle disconnections gracefully
- Create a simple HTML test page to test the chat

### What to Submit
- Code files for all three features
- Screenshots: file upload success, file upload error (wrong type), background task log file, WebSocket chat between two browser tabs

---

## Task 4: Testing with pytest — 20 marks

Write a comprehensive test suite for your API.

### Test Cases Required

| Category | Tests | Marks |
|----------|-------|-------|
| Student CRUD | Create student, list students, get by ID, update, delete | 6 |
| Validation | Invalid email, marks > 100, name too short, duplicate email | 4 |
| Authentication | Register, login, access with token, access without token | 4 |
| Role-based access | Admin can delete, student cannot delete, 403 errors | 3 |
| Edge cases | Get non-existent student (404), empty list, update non-existent | 3 |

### Requirements

- Use `pytest` with `TestClient` from FastAPI
- At least **15 test functions**
- Every test must have a clear name (e.g., `test_create_student_success`, `test_login_wrong_password`)
- Test both success and error cases
- Run with coverage: `pytest --cov=. --cov-report=term-missing`
- Achieve at least **80% code coverage**

### Sample Test Structure

```python
# test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_create_student_success():
    response = client.post("/api/students", json={...})
    assert response.status_code == 201
    assert response.json()["success"] is True

def test_create_student_invalid_marks():
    response = client.post("/api/students", json={"marks": 150, ...})
    assert response.status_code == 422
```

### What to Submit
- `test_api.py` (or multiple test files)
- Terminal screenshot showing `pytest -v` output (all tests passing)
- Terminal screenshot showing coverage report (`pytest --cov=.`)

---

## Rubric

| Criterion | Excellent (100%) | Good (75%) | Needs Work (50%) | Incomplete (25%) |
|-----------|---------|------|------------|------------|
| **Task 1: CRUD API (30)** | All endpoints work, validation complete, search/filter/pagination, seed data, stats, clean response format | Most endpoints work, basic validation, some filters missing | Endpoints partially work, minimal validation, no filters | Only 1-2 endpoints, no validation |
| **Task 2: Auth (25)** | Full JWT flow, bcrypt hashing, OAuth2 in Swagger, role-based access, both dependencies | Login/register work, token verification, basic role check | Login works but token handling incomplete, no role-based access | Only registration, no JWT |
| **Task 3: Advanced (25)** | File upload with validation, background tasks working, WebSocket chat with connection manager | File upload works, background task works, basic WebSocket | Only one of the three features complete | Attempted but not functional |
| **Task 4: Testing (20)** | 15+ tests, covers CRUD + auth + validation + errors, 80%+ coverage | 10-14 tests, covers CRUD and some auth, 60%+ coverage | 5-9 tests, only happy paths, below 60% coverage | Fewer than 5 tests |
| **Code Quality (bonus +5)** | Well-organized files, clear comments, proper project structure, requirements.txt | Reasonable organization, some comments | Single file, minimal comments | Messy, no comments |

---

## Project Structure (Recommended)

```
fastapi-project/
├── main.py              # FastAPI app, middleware, startup
├── database.py          # SQLAlchemy engine, session, Base
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # JWT + password hashing
├── routes/
│   ├── students.py      # Student CRUD endpoints
│   ├── auth.py          # Register, login endpoints
│   └── upload.py        # File upload endpoint
├── tests/
│   └── test_api.py      # All test cases
├── uploads/             # Uploaded photos
├── activity.log         # Background task log
├── chat.html            # WebSocket test page
├── requirements.txt
└── README.md
```

## Tips

- Start with Task 1 — get CRUD working first before adding auth
- Use Swagger UI (`/docs`) to test every endpoint as you build
- For Task 2, use Swagger's "Authorize" button to test protected routes
- For Task 4, write tests as you build — it is easier than writing them all at the end
- Keep your code organized — one file per concern is better than one giant file
