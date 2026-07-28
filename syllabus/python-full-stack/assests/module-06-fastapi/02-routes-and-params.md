# Routes and Parameters — Handling Requests

**Module 06 — FastAPI: Modern API Development | Topic 2**

---

## What is a Route?

A route (also called an endpoint) maps a URL path to a Python function. When a client sends a request to that URL, FastAPI runs the corresponding function.

```python
@app.get("/students")      # Route decorator
def get_students():         # Route handler function
    return {"students": []}
```

---

## Path Parameters

Path parameters are **variable parts of the URL**. They extract values directly from the URL path.

```python
# /students/1  → student_id = 1
# /students/42 → student_id = 42
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id}
```

### Type Validation

FastAPI automatically validates the type based on your type hint:

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):  # Must be an integer
    return {"student_id": student_id}

# GET /students/5     → ✅ Works (student_id = 5)
# GET /students/abc   → ❌ 422 Error (not an integer)
# GET /students/3.14  → ❌ 422 Error (not an integer)
```

### Multiple Path Parameters

```python
@app.get("/courses/{course_id}/modules/{module_id}")
def get_module(course_id: int, module_id: int):
    return {
        "course_id": course_id,
        "module_id": module_id
    }
# GET /courses/1/modules/4 → {"course_id": 1, "module_id": 4}
```

### Path Parameter with Enum Validation

```python
from enum import Enum

class CourseCategory(str, Enum):
    python = "python"
    web = "web"
    data = "data"
    devops = "devops"

@app.get("/courses/category/{category}")
def get_courses_by_category(category: CourseCategory):
    return {"category": category, "message": f"Showing {category.value} courses"}

# GET /courses/category/python → ✅ Works
# GET /courses/category/java   → ❌ 422 Error (not a valid category)
```

### Order Matters

Put fixed paths BEFORE path parameters:

```python
# ✅ Correct order
@app.get("/students/me")          # Fixed path first
def get_current_student(): ...

@app.get("/students/{student_id}") # Variable path second
def get_student(student_id: int): ...

# ❌ Wrong order (would never reach /students/me)
@app.get("/students/{student_id}") # This catches everything, including "me"
def get_student(student_id: int): ...

@app.get("/students/me")          # Never reached
def get_current_student(): ...
```

---

## Query Parameters

Query parameters come after the `?` in a URL. They are used for **filtering, sorting, and pagination**.

```
/students?city=Bhopal&limit=10&sort=name
          ↑           ↑        ↑
          key=value pairs separated by &
```

### Basic Query Parameters

```python
@app.get("/students")
def get_students(city: str, limit: int = 10):
    return {"city": city, "limit": limit}

# GET /students?city=Bhopal           → city="Bhopal", limit=10 (default)
# GET /students?city=Pune&limit=5     → city="Pune", limit=5
# GET /students                       → ❌ 422 Error (city is required)
```

### Optional Query Parameters

```python
from typing import Optional

@app.get("/students")
def get_students(
    city: Optional[str] = None,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 10
):
    return {
        "city": city,         # None if not provided
        "is_active": is_active,
        "skip": skip,
        "limit": limit
    }

# GET /students                        → All defaults
# GET /students?city=Bhopal            → city="Bhopal", rest default
# GET /students?is_active=false&limit=5 → is_active=False, limit=5
```

### Query Parameter Validation

```python
from fastapi import Query

@app.get("/students")
def get_students(
    city: Optional[str] = Query(None, min_length=2, max_length=50),
    limit: int = Query(10, ge=1, le=100),  # Between 1 and 100
    search: Optional[str] = Query(None, min_length=1, description="Search by name")
):
    return {"city": city, "limit": limit, "search": search}
```

**Validation parameters:**

| Parameter | Type | Meaning |
|-----------|------|---------|
| `min_length` | str | Minimum string length |
| `max_length` | str | Maximum string length |
| `ge` | int/float | Greater than or equal |
| `le` | int/float | Less than or equal |
| `gt` | int/float | Greater than |
| `lt` | int/float | Less than |
| `regex` | str | Must match this pattern |
| `description` | any | Shows in Swagger docs |
| `example` | any | Shows in Swagger docs |

---

## Request Body

For POST and PUT requests, data comes in the **request body** as JSON. FastAPI uses Pydantic models to validate it.

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

# Define the schema
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    city: str = "Bhopal"          # Optional with default
    fee_paid: float = 0.0
    phone: Optional[str] = None   # Truly optional (can be absent)

# Use in endpoint
@app.post("/students")
def create_student(student: StudentCreate):
    return {
        "message": "Student created",
        "data": student.model_dump()
    }
```

**Request body (JSON):**
```json
{
    "name": "Rahul Sharma",
    "email": "rahul@email.com",
    "city": "Bhopal",
    "fee_paid": 15000
}
```

### Combining Path, Query, and Body

```python
@app.put("/courses/{course_id}")
def update_course(
    course_id: int,                     # Path parameter
    notify_students: bool = False,      # Query parameter
    course: CourseUpdate = ...,         # Request body
):
    return {
        "course_id": course_id,
        "notify": notify_students,
        "updated_data": course.model_dump()
    }

# PUT /courses/5?notify_students=true
# Body: {"title": "Python Advanced", "price": 30000}
```

**How FastAPI decides:**
- If the parameter is in the **path** → path parameter
- If the parameter is a **Pydantic model** → request body
- Everything else → **query parameter**

---

## Response Models

Control what data your endpoint returns:

```python
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    city: str

    model_config = ConfigDict(from_attributes=True)

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    # Even if the database returns extra fields (password, etc.),
    # only fields in StudentResponse are sent to the client
    student = get_from_db(student_id)
    return student
```

### List Response

```python
@app.get("/students", response_model=list[StudentResponse])
def get_students():
    return get_all_from_db()
```

---

## Status Codes

```python
from fastapi import status

@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    return {"message": "Created"}

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    return None  # 204 = no content in response
```

---

## Headers and Cookies

### Reading Headers

```python
from fastapi import Header

@app.get("/info")
def get_info(
    user_agent: str = Header(None),
    accept_language: str = Header(None, alias="accept-language")
):
    return {
        "user_agent": user_agent,
        "language": accept_language
    }
```

### Setting Response Headers

```python
from fastapi import Response

@app.get("/students")
def get_students(response: Response):
    response.headers["X-Total-Count"] = "150"
    response.headers["X-Page"] = "1"
    return {"students": []}
```

---

## APIRouter — Organizing Endpoints

For larger apps, split endpoints into separate files using routers:

```python
# app/api/v1/endpoints/students.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.get("/")
def get_students():
    return {"students": []}

@router.get("/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id}

@router.post("/")
def create_student(student: StudentCreate):
    return {"message": "Created"}
```

```python
# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import students, courses

app = FastAPI()
app.include_router(students.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
```

Now endpoints are available at:
- `GET /api/v1/students`
- `GET /api/v1/students/5`
- `POST /api/v1/students`

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Path params | `/{id}` — extract from URL, type-validated |
| Query params | `?key=value` — for filtering, pagination, sorting |
| Request body | JSON payload, validated by Pydantic model |
| Response model | Controls what fields the client sees |
| `Query()` | Add validation to query parameters |
| `Header()` | Read HTTP headers |
| `APIRouter` | Split endpoints into modules |

---

*TechPath Institute — Python Full Stack Development*
