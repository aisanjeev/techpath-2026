# FastAPI Introduction — Modern Python APIs

**Module 06 — FastAPI: Modern API Development | Topic 1**

---

## What is an API?

An API (Application Programming Interface) is a way for two software applications to talk to each other. When you open Swiggy on your phone, the app sends a request to Swiggy's server asking "What restaurants are near Bhopal?" — the server sends back a response with restaurant data. That communication happens through an API.

**Real-world analogy:** Think of a restaurant. You (the client) do not walk into the kitchen. Instead, you tell the waiter (API) what you want, and the waiter brings your food from the kitchen (server).

### REST API

REST (Representational State Transfer) is the most common style of API. It uses HTTP methods:

| HTTP Method | Purpose | Example |
|------------|---------|---------|
| **GET** | Read/fetch data | Get list of students |
| **POST** | Create new data | Register a new student |
| **PUT** | Replace/update data | Update student's complete profile |
| **PATCH** | Partial update | Update only the student's city |
| **DELETE** | Remove data | Delete a student record |

---

## What is FastAPI?

FastAPI is a modern Python web framework for building APIs. It was created by Sebastian Ramirez in 2018 and has become the most popular Python API framework.

### Why FastAPI?

| Feature | FastAPI | Flask | Django REST |
|---------|---------|-------|-------------|
| Speed | Very fast (async) | Moderate | Moderate |
| Type checking | Built-in (Pydantic) | Manual | Serializers |
| Auto documentation | Swagger + ReDoc | Manual | Manual |
| Async support | Native | Limited | Limited |
| Learning curve | Easy | Easy | Steep |
| Validation | Automatic | Manual | Serializers |

### Key Advantages

1. **Fast to run** — Built on Starlette (ASGI), one of the fastest Python frameworks
2. **Fast to code** — Type hints and auto-validation reduce boilerplate by 40%
3. **Auto documentation** — Swagger UI and ReDoc generated automatically
4. **Type safety** — Pydantic validates all input/output data
5. **Async support** — Handle thousands of concurrent requests efficiently

---

## ASGI vs WSGI

| Feature | WSGI (Flask, Django) | ASGI (FastAPI) |
|---------|---------------------|----------------|
| Full form | Web Server Gateway Interface | Asynchronous Server Gateway Interface |
| Request handling | One at a time (synchronous) | Many at once (asynchronous) |
| Real-time | Not supported | WebSockets supported |
| Speed | Good | Excellent |
| Server | Gunicorn | Uvicorn |

**Think of it this way:** WSGI is like a single-lane road — one car at a time. ASGI is like a highway — multiple cars move simultaneously.

---

## Installation and Setup

### Install FastAPI and Uvicorn

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install FastAPI with all extras
pip install "fastapi[standard]"

# Or install separately
pip install fastapi uvicorn
```

### Your First API

Create a file `main.py`:

```python
from fastapi import FastAPI

# Create the app instance
app = FastAPI(
    title="TechPath API",
    description="Student Management API for TechPath Institute",
    version="1.0.0"
)

# Define a route (endpoint)
@app.get("/")
def home():
    return {"message": "Welcome to TechPath Institute API!"}

@app.get("/about")
def about():
    return {
        "name": "TechPath Institute",
        "city": "Bhopal",
        "courses": ["Python Full Stack", "Data Science", "React"]
    }
```

### Running the Server

```bash
# Start the development server
uvicorn main:app --reload

# Output:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
```

**Breaking it down:**
- `main` — the file name (main.py)
- `app` — the FastAPI instance variable
- `--reload` — auto-restart when you save changes (development only)

### Custom Host and Port

```bash
# Listen on all interfaces, port 8080
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

---

## Auto-Generated Documentation

FastAPI automatically creates interactive API documentation. No setup needed.

### Swagger UI

Open `http://localhost:8000/docs` in your browser.

Features:
- See all endpoints organized by tags
- Try each endpoint directly from the browser
- See request/response schemas
- Test with different parameters

### ReDoc

Open `http://localhost:8000/redoc` in your browser.

Features:
- Clean, readable documentation
- Three-panel layout
- Better for sharing with non-developers

### OpenAPI JSON

Open `http://localhost:8000/openapi.json` for the raw API specification.

---

## The Request-Response Cycle

```
Client (Browser/App)                    Server (FastAPI)
        |                                      |
        |  ── HTTP Request ──────────────►     |
        |  GET /students?city=Bhopal           |
        |                                      |
        |                              1. Receive request
        |                              2. Validate parameters
        |                              3. Run your function
        |                              4. Serialize response
        |                                      |
        |  ◄────────── HTTP Response ──        |
        |  200 OK                              |
        |  {"students": [...]}                 |
```

### HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|------------|
| **200** | OK | Request succeeded |
| **201** | Created | New resource created (POST) |
| **204** | No Content | Success, nothing to return (DELETE) |
| **400** | Bad Request | Invalid input data |
| **401** | Unauthorized | Not logged in |
| **403** | Forbidden | Logged in but not allowed |
| **404** | Not Found | Resource does not exist |
| **422** | Unprocessable Entity | Validation error (FastAPI default) |
| **500** | Internal Server Error | Bug on the server |

---

## Async Endpoints

FastAPI supports both sync and async endpoints:

```python
# Sync endpoint (simple, for CPU-bound work)
@app.get("/sync")
def sync_endpoint():
    return {"type": "synchronous"}

# Async endpoint (for I/O-bound work: database, API calls, file reads)
@app.get("/async")
async def async_endpoint():
    return {"type": "asynchronous"}
```

**When to use async:**
- Database queries
- External API calls
- File operations
- Any I/O-bound work

**When to use sync:**
- Simple calculations
- CPU-bound work
- When you are unsure (FastAPI handles sync in a thread pool)

---

## Project Structure

For a real project, organize your code like this:

```
techpath-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── core/
│   │   ├── config.py        # Settings (database URL, secrets)
│   │   └── database.py      # Database connection
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── students.py
│   │       │   ├── courses.py
│   │       │   └── auth.py
│   │       └── router.py    # Combines all endpoint routers
│   ├── models/               # SQLAlchemy models
│   │   ├── student.py
│   │   └── course.py
│   ├── schemas/              # Pydantic schemas
│   │   ├── student.py
│   │   └── course.py
│   ├── crud/                 # Database operations
│   │   ├── student.py
│   │   └── course.py
│   └── services/             # Business logic
│       └── email.py
├── tests/
│   ├── test_students.py
│   └── test_courses.py
├── migrations/               # Alembic migrations
├── requirements.txt
├── .env
└── pyproject.toml
```

---

## Configuring the App

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TechPath API",
    description="Student Management API",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI path
    redoc_url="/redoc",      # ReDoc path
)

# Allow frontend to call the API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| API | Interface for apps to communicate |
| REST | Standard pattern using HTTP methods (GET, POST, PUT, DELETE) |
| FastAPI | Modern, fast, auto-documented Python API framework |
| ASGI | Async server interface — handles many requests at once |
| Uvicorn | ASGI server that runs FastAPI |
| Swagger UI | Auto-generated interactive docs at `/docs` |
| `--reload` | Auto-restart server on code changes |

---

*TechPath Institute — Python Full Stack Development*
