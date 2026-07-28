# Backend Development & APIs

**Module 14 — FastAPI & Django | Topic 1**

---

## Frontend vs Backend

| | Frontend | Backend |
|-|----------|---------|
| **What** | What users see | What runs on the server |
| **Languages** | HTML, CSS, JavaScript | Python, Java, Node.js, Go |
| **Handles** | UI, design, interactions | Database, logic, authentication |
| **Runs on** | User's browser | Server |
| **Examples** | React, Vue, Angular | FastAPI, Django, Express |

```
User → Browser (Frontend) → API Request → Server (Backend) → Database
                           ← API Response ←
```

---

## What is an API?

**API** = Application Programming Interface — a way for two programs to talk to each other.

> **Restaurant analogy:**
> - You (frontend) = Customer
> - Waiter (API) = Takes your order and brings food
> - Kitchen (backend) = Prepares the food
> - Pantry (database) = Stores ingredients

### REST API

Most web APIs follow **REST** (Representational State Transfer) rules:

| HTTP Method | Purpose | Example |
|-------------|---------|---------|
| `GET` | Read/fetch data | Get list of students |
| `POST` | Create new data | Add a new student |
| `PUT` | Update entire record | Update student info |
| `PATCH` | Update part of record | Change only email |
| `DELETE` | Remove data | Delete a student |

### API Request & Response

```
Request:  GET /api/students/1
Response: {
    "id": 1,
    "name": "Rahul",
    "age": 20,
    "course": "ADCA"
}
```

### Status Codes

| Code | Meaning |
|------|---------|
| `200` | OK — success |
| `201` | Created — new item created |
| `400` | Bad Request — wrong input |
| `401` | Unauthorized — not logged in |
| `403` | Forbidden — no permission |
| `404` | Not Found — doesn't exist |
| `500` | Server Error — something broke |

---

## FastAPI — Modern Python Web Framework

**FastAPI** is a modern, fast Python framework for building APIs.

| Feature | Detail |
|---------|--------|
| **Speed** | One of the fastest Python frameworks |
| **Type hints** | Uses Python type hints for validation |
| **Auto docs** | Generates API documentation automatically |
| **Async** | Handles many requests at once |
| **Easy to learn** | Simple, clean syntax |

### Setup

```bash
pip install fastapi uvicorn
```

### First API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/students")
def get_students():
    return [
        {"id": 1, "name": "Rahul", "marks": 85},
        {"id": 2, "name": "Priya", "marks": 92}
    ]

@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"id": student_id, "name": "Rahul"}
```

### Run the Server

```bash
uvicorn main:app --reload
# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### POST — Create Data

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    course: str

@app.post("/students")
def create_student(student: Student):
    return {"message": f"Student {student.name} created!", "data": student}
```

### Path & Query Parameters

```python
# Path parameter: /students/1
@app.get("/students/{id}")
def get_student(id: int):
    return {"id": id}

# Query parameter: /students?course=ADCA&limit=10
@app.get("/students")
def list_students(course: str = None, limit: int = 10):
    return {"course": course, "limit": limit}
```

---

## Django — Full-Stack Web Framework

**Django** is a batteries-included Python framework — everything built in.

| Feature | Detail |
|---------|--------|
| **Admin panel** | Auto-generated admin dashboard |
| **ORM** | Database without writing SQL |
| **Templates** | HTML rendering built in |
| **Auth** | Login/logout/permissions built in |
| **Security** | CSRF, XSS protection by default |

### Setup

```bash
pip install django
django-admin startproject mysite
cd mysite
python manage.py runserver
# Server at http://localhost:8000
```

### Django vs FastAPI

| Feature | FastAPI | Django |
|---------|---------|--------|
| **Type** | API framework | Full-stack framework |
| **Best for** | APIs, microservices | Full websites with admin |
| **Speed** | Very fast | Fast |
| **Learning curve** | Easy | Medium |
| **Admin panel** | No (add manually) | Yes (built in) |
| **Database ORM** | SQLAlchemy (external) | Built-in ORM |
| **Templates** | No (use React/Vue) | Yes (built in) |
| **When to use** | API backends, modern apps | CMS, blogs, e-commerce |

---

## Database with Python (SQLAlchemy)

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    course = Column(String(50))

# Connect to database
engine = create_engine("sqlite:///school.db")
Base.metadata.create_all(engine)

# Add a student
with Session(engine) as session:
    new_student = Student(name="Rahul", age=20, course="ADCA")
    session.add(new_student)
    session.commit()
```

---

## Authentication Basics

| Method | How It Works |
|--------|-------------|
| **Session-based** | Server stores login state, sends cookie |
| **Token-based (JWT)** | Server gives token, client sends with each request |
| **OAuth** | Login with Google/GitHub (third-party) |
| **Firebase Auth** | Google's auth service (easy setup) |

### JWT Flow

```
1. User sends username + password
2. Server verifies → creates JWT token
3. Server sends token to client
4. Client stores token (localStorage)
5. Client sends token with every request (Authorization header)
6. Server verifies token → allows access
```

---

## Summary

- **Backend** = server-side logic, databases, APIs
- **API** = how frontend and backend communicate
- **REST** = standard for APIs (GET, POST, PUT, DELETE)
- **FastAPI** = fast, modern Python API framework
- **Django** = full-stack Python framework with admin panel
- **Status codes:** 200=OK, 201=Created, 404=Not Found, 500=Error
- **JWT** = token-based authentication
- FastAPI auto-generates docs at `/docs` endpoint
