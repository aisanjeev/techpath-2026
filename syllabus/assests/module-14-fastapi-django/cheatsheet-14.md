# Cheat Sheet: FastAPI & Django

**Module 14 — Quick Reference**

---

## HTTP Methods

| Method | Action | Example |
|--------|--------|---------|
| GET | Read | Get students |
| POST | Create | Add student |
| PUT | Full update | Replace student |
| PATCH | Partial update | Change email |
| DELETE | Remove | Delete student |

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |

---

## FastAPI Quick Start

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int

@app.get("/")
def home():
    return {"message": "Hello"}

@app.post("/students")
def create(student: Student):
    return student
```

```bash
uvicorn main:app --reload
# Docs: http://localhost:8000/docs
```

---

## Django Quick Start

```bash
pip install django
django-admin startproject mysite
cd mysite
python manage.py runserver
```

---

## FastAPI vs Django

| | FastAPI | Django |
|-|---------|--------|
| Type | API only | Full-stack |
| Admin | No | Yes |
| ORM | SQLAlchemy | Built-in |
| Templates | No | Yes |
| Speed | Very fast | Fast |
| Best for | APIs | Full websites |
