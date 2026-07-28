# Module 14 — FastAPI & Django — Quick Revision Notes

---

## Backend Development Basics
- **Frontend** = what users see (HTML/CSS/JS)
- **Backend** = server-side logic, database, APIs
- **API** = Application Programming Interface (how frontend talks to backend)
- **REST API** = uses HTTP methods (GET, POST, PUT, DELETE) with JSON

## HTTP Methods
| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Read data | Get all students |
| `POST` | Create new | Add a student |
| `PUT` | Update existing | Update marks |
| `DELETE` | Remove | Delete a student |

## Status Codes
| Code | Meaning |
|------|---------|
| `200` | OK (success) |
| `201` | Created |
| `400` | Bad Request (invalid data) |
| `401` | Unauthorized (not logged in) |
| `404` | Not Found |
| `422` | Validation Error |
| `500` | Server Error |

---

## FastAPI

### Setup
```bash
pip install fastapi uvicorn
```

### Basic App
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.get("/students")
def get_students():
    return [{"name": "Rahul", "marks": 85}]
```

### Run
```bash
uvicorn main:app --reload
# Opens at http://localhost:8000
# Docs at http://localhost:8000/docs (Swagger UI)
```

### Path Parameters
```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"id": student_id, "name": "Rahul"}
```

### Query Parameters
```python
@app.get("/students")
def list_students(course: str = "all", limit: int = 10):
    return {"course": course, "limit": limit}
# URL: /students?course=ADCA&limit=5
```

### Request Body (POST)
```python
from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str
    course: str = "ADCA"
    marks: int

@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    return {"message": f"Created {student.name}"}
```

### Pydantic Validation
```python
from pydantic import BaseModel, Field, EmailStr

class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    marks: int = Field(ge=0, le=100)
    course: str = "ADCA"
```

### FastAPI Key Features
- Auto-generates API docs (Swagger + ReDoc)
- Type validation with Pydantic
- Async support (`async def`)
- Dependency injection
- Very fast (built on Starlette + Uvicorn)

---

## Django

### Setup
```bash
pip install django
django-admin startproject myproject
cd myproject
python manage.py startapp students
python manage.py runserver
# Opens at http://localhost:8000
```

### Project Structure
```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py    # configuration
│   ├── urls.py        # root URL routing
│   └── wsgi.py
└── students/
    ├── models.py      # database models
    ├── views.py       # request handlers
    ├── urls.py        # app URL routing
    ├── admin.py       # admin panel config
    └── templates/     # HTML templates
```

### Model (Database Table)
```python
# students/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=50, default="ADCA")
    marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

### Migrations
```bash
python manage.py makemigrations    # create migration
python manage.py migrate           # apply to database
```

### Views
```python
# students/views.py
from django.http import JsonResponse
from .models import Student

def student_list(request):
    students = Student.objects.all().values()
    return JsonResponse(list(students), safe=False)
```

### URLs
```python
# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("api/students/", views.student_list),
]
```

### Admin Panel
```python
# students/admin.py
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```
```bash
python manage.py createsuperuser   # create admin user
# Admin at http://localhost:8000/admin/
```

---

## FastAPI vs Django

| Feature | FastAPI | Django |
|---------|---------|--------|
| Best for | APIs, microservices | Full web apps |
| Speed | Very fast | Moderate |
| Learning | Easier | More to learn |
| Database | SQLAlchemy / any ORM | Django ORM (built-in) |
| Admin panel | None (build your own) | Built-in |
| Auth | Add manually | Built-in |
| API docs | Auto-generated | DRF needed |
| Templates | Not included | Built-in |

## JSON Response Format
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Rahul",
        "marks": 85
    },
    "message": "Student created"
}
```
