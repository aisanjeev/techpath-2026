# API Testing — pytest + httpx TestClient

**Module 06 — FastAPI: Modern API Development | Topic 8**

---

## Why Test Your API?

| Without Tests | With Tests |
|---------------|-----------|
| "I think it works" | "I know it works — 47 tests pass" |
| Bug found in production by users | Bug caught before deployment |
| Afraid to change code (might break something) | Refactor confidently — tests catch regressions |
| Manual testing with Swagger after every change | Automated tests run in seconds |

### Types of Tests

| Type | What It Tests | Example |
|------|--------------|---------|
| **Unit test** | A single function in isolation | Test `hash_password()` returns a hash |
| **Integration test** | Multiple components working together | Test endpoint + database + validation |
| **End-to-end (E2E) test** | The entire system | Test login → create student → verify |

For APIs, **integration tests** are the most valuable — they test the endpoint, validation, database, and response format all at once.

---

## Setup

### Install Dependencies

```bash
pip install pytest pytest-asyncio httpx
```

### Test Configuration

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session():
    """Create tables and provide a test database session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(db_session):
    """Provide an HTTP test client with test database."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
```

**Key concepts:**
- **In-memory database** — Tests use a temporary database that is created fresh for each test
- **dependency_overrides** — Replace the real database with the test database
- **AsyncClient** — Makes HTTP requests to your app without starting a real server

---

## Writing Tests

### Test Structure (AAA Pattern)

Every test follows the **Arrange-Act-Assert** pattern:

```python
async def test_something(client):
    # Arrange — Set up the data
    data = {"name": "Rahul", "email": "rahul@email.com"}

    # Act — Call the endpoint
    response = await client.post("/api/v1/students", json=data)

    # Assert — Check the result
    assert response.status_code == 201
    assert response.json()["name"] == "Rahul"
```

### Testing CRUD Endpoints

```python
# tests/test_students.py
import pytest

# ── CREATE ──
@pytest.mark.asyncio
async def test_create_student(client):
    response = await client.post("/api/v1/students", json={
        "name": "Rahul Sharma",
        "email": "rahul@email.com",
        "city": "Bhopal",
        "fee_paid": 15000
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Rahul Sharma"
    assert data["email"] == "rahul@email.com"
    assert data["city"] == "Bhopal"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_student_duplicate_email(client):
    # Create first student
    await client.post("/api/v1/students", json={
        "name": "Rahul", "email": "rahul@email.com"
    })
    # Try to create another with the same email
    response = await client.post("/api/v1/students", json={
        "name": "Rahul 2", "email": "rahul@email.com"
    })
    assert response.status_code == 409  # Conflict

@pytest.mark.asyncio
async def test_create_student_invalid_email(client):
    response = await client.post("/api/v1/students", json={
        "name": "Rahul", "email": "not-an-email"
    })
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_create_student_missing_name(client):
    response = await client.post("/api/v1/students", json={
        "email": "rahul@email.com"
    })
    assert response.status_code == 422

# ── READ ──
@pytest.mark.asyncio
async def test_get_student(client):
    # Create a student first
    create_resp = await client.post("/api/v1/students", json={
        "name": "Priya Patel", "email": "priya@email.com", "city": "Pune"
    })
    student_id = create_resp.json()["id"]

    # Get the student
    response = await client.get(f"/api/v1/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Priya Patel"

@pytest.mark.asyncio
async def test_get_student_not_found(client):
    response = await client.get("/api/v1/students/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_students(client):
    # Create multiple students
    for i in range(5):
        await client.post("/api/v1/students", json={
            "name": f"Student {i}", "email": f"student{i}@email.com"
        })

    response = await client.get("/api/v1/students")
    assert response.status_code == 200
    assert len(response.json()) == 5

@pytest.mark.asyncio
async def test_list_students_with_filters(client):
    await client.post("/api/v1/students", json={
        "name": "Amit", "email": "amit@email.com", "city": "Bhopal"
    })
    await client.post("/api/v1/students", json={
        "name": "Sneha", "email": "sneha@email.com", "city": "Pune"
    })

    response = await client.get("/api/v1/students?city=Bhopal")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["city"] == "Bhopal"

# ── UPDATE ──
@pytest.mark.asyncio
async def test_update_student(client):
    create_resp = await client.post("/api/v1/students", json={
        "name": "Rahul", "email": "rahul@email.com", "city": "Bhopal"
    })
    student_id = create_resp.json()["id"]

    response = await client.patch(f"/api/v1/students/{student_id}", json={
        "city": "Indore", "fee_paid": 20000
    })
    assert response.status_code == 200
    assert response.json()["city"] == "Indore"
    assert response.json()["fee_paid"] == 20000
    assert response.json()["name"] == "Rahul"  # Unchanged field

# ── DELETE ──
@pytest.mark.asyncio
async def test_delete_student(client):
    create_resp = await client.post("/api/v1/students", json={
        "name": "Delete Me", "email": "delete@email.com"
    })
    student_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/students/{student_id}")
    assert response.status_code == 204

    # Verify it is gone
    get_resp = await client.get(f"/api/v1/students/{student_id}")
    assert get_resp.status_code == 404
```

---

## Testing Authentication

```python
# tests/test_auth.py
import pytest

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/api/v1/auth/register", json={
        "name": "Rahul Sharma",
        "email": "rahul@email.com",
        "password": "SecurePass123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "rahul@email.com"
    assert "password" not in response.json()  # Never expose password!

@pytest.mark.asyncio
async def test_login(client):
    # Register first
    await client.post("/api/v1/auth/register", json={
        "name": "Rahul", "email": "rahul@email.com", "password": "SecurePass123"
    })

    # Login
    response = await client.post("/api/v1/auth/login", json={
        "email": "rahul@email.com", "password": "SecurePass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Rahul", "email": "rahul@email.com", "password": "SecurePass123"
    })

    response = await client.post("/api/v1/auth/login", json={
        "email": "rahul@email.com", "password": "WrongPassword"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint(client):
    # Register and login
    await client.post("/api/v1/auth/register", json={
        "name": "Rahul", "email": "rahul@email.com", "password": "SecurePass123"
    })
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "rahul@email.com", "password": "SecurePass123"
    })
    token = login_resp.json()["access_token"]

    # Access protected endpoint with token
    response = await client.get("/api/v1/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "rahul@email.com"

@pytest.mark.asyncio
async def test_protected_endpoint_no_token(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401  # or 403
```

---

## Helper Fixtures

Create reusable fixtures to reduce code duplication:

```python
# tests/conftest.py (add to existing)

@pytest_asyncio.fixture
async def sample_student(client):
    """Create and return a sample student."""
    response = await client.post("/api/v1/students", json={
        "name": "Rahul Sharma",
        "email": "rahul@email.com",
        "city": "Bhopal",
        "fee_paid": 15000
    })
    return response.json()

@pytest_asyncio.fixture
async def auth_headers(client):
    """Register a user and return auth headers."""
    await client.post("/api/v1/auth/register", json={
        "name": "Test User", "email": "test@email.com", "password": "TestPass123"
    })
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "test@email.com", "password": "TestPass123"
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Usage in tests
@pytest.mark.asyncio
async def test_with_auth(client, auth_headers):
    response = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_students.py

# Run a specific test function
pytest tests/test_students.py::test_create_student

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Stop on first failure
pytest -x

# Run tests matching a keyword
pytest -k "login"
```

### Coverage Report

```bash
pytest --cov=app --cov-report=term-missing

# Output:
# Name                          Stmts   Miss  Cover   Missing
# -----------------------------------------------------------
# app/api/v1/endpoints/auth.py     45      3    93%   67-69
# app/api/v1/endpoints/students.py 52      0   100%
# app/crud/student.py              38      2    95%   45, 62
# -----------------------------------------------------------
# TOTAL                           135      5    96%
```

---

## Error Handling Tests

```python
@pytest.mark.asyncio
async def test_validation_error_format(client):
    response = await client.post("/api/v1/students", json={
        "name": "",        # Too short (min_length=2)
        "email": "bad",    # Invalid email
        "fee_paid": -100   # Negative (ge=0)
    })
    assert response.status_code == 422
    errors = response.json()["detail"]
    # Verify the error contains field information
    error_fields = [e["loc"][-1] for e in errors]
    assert "name" in error_fields or "email" in error_fields
```

---

## Test Organization

```
tests/
├── conftest.py           # Shared fixtures (db, client, auth)
├── test_students.py      # Student endpoint tests
├── test_courses.py       # Course endpoint tests
├── test_auth.py          # Authentication tests
├── test_enrollments.py   # Enrollment tests
└── test_utils.py         # Utility function unit tests
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| pytest | Python testing framework |
| httpx AsyncClient | Makes HTTP requests to your app in tests |
| conftest.py | Shared test fixtures |
| dependency_overrides | Replace real database with test database |
| AAA pattern | Arrange → Act → Assert |
| Fixtures | Reusable setup code for tests |
| Coverage | Measure how much code your tests cover |
| `pytest -v` | Verbose output showing each test |

---

*TechPath Institute — Python Full Stack Development*
