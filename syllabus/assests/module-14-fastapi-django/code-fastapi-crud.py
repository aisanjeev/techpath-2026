"""
FastAPI CRUD API — Module 14 Code Snap
Install: pip install fastapi uvicorn
Run:     uvicorn code-fastapi-crud:app --reload
Docs:    http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Student API", version="1.0.0")

# --- In-Memory Database (replace with SQLite for persistence) ---
students_db = [
    {"id": 1, "name": "Rahul Sharma", "email": "rahul@email.com", "course": "ADCA", "marks": 85, "city": "Bhopal"},
    {"id": 2, "name": "Priya Patel", "email": "priya@email.com", "course": "DCA", "marks": 92, "city": "Indore"},
    {"id": 3, "name": "Amit Kumar", "email": "amit@email.com", "course": "ADCA", "marks": 67, "city": "Delhi"},
]
next_id = 4


# --- Pydantic Models ---
class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str
    course: str = "ADCA"
    marks: int = Field(ge=0, le=100)
    city: str = ""


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = None
    course: Optional[str] = None
    marks: Optional[int] = Field(None, ge=0, le=100)
    city: Optional[str] = None


# --- Helper ---
def find_student(student_id: int):
    for s in students_db:
        if s["id"] == student_id:
            return s
    return None


# --- Endpoints ---

@app.get("/")
def home():
    return {"message": "Student API is running", "docs": "/docs"}


@app.get("/api/students")
def list_students(
    course: Optional[str] = None,
    city: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = "id",
    limit: int = Query(default=10, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
):
    result = students_db.copy()

    if course:
        result = [s for s in result if s["course"].lower() == course.lower()]
    if city:
        result = [s for s in result if s["city"].lower() == city.lower()]
    if search:
        result = [s for s in result if search.lower() in s["name"].lower()]

    if sort in ("name", "marks", "id"):
        result.sort(key=lambda s: s[sort])

    total = len(result)
    result = result[skip:skip + limit]

    return {"success": True, "total": total, "data": result}


@app.get("/api/students/{student_id}")
def get_student(student_id: int):
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"success": True, "data": student}


@app.post("/api/students", status_code=201)
def create_student(student: StudentCreate):
    global next_id

    if any(s["email"] == student.email for s in students_db):
        raise HTTPException(status_code=400, detail="Email already exists")

    new_student = {"id": next_id, **student.model_dump()}
    students_db.append(new_student)
    next_id += 1

    return {"success": True, "data": new_student, "message": "Student created"}


@app.put("/api/students/{student_id}")
def update_student(student_id: int, updates: StudentUpdate):
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = updates.model_dump(exclude_unset=True)
    student.update(update_data)

    return {"success": True, "data": student, "message": "Student updated"}


@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    students_db.remove(student)
    return {"success": True, "message": f"Deleted {student['name']}"}


@app.get("/api/stats")
def get_stats():
    if not students_db:
        return {"success": True, "data": {"total": 0}}

    marks = [s["marks"] for s in students_db]
    courses = {}
    for s in students_db:
        courses[s["course"]] = courses.get(s["course"], 0) + 1

    return {
        "success": True,
        "data": {
            "total_students": len(students_db),
            "average_marks": round(sum(marks) / len(marks), 1),
            "highest_marks": max(marks),
            "lowest_marks": min(marks),
            "courses": courses,
        },
    }
