# Build a Complete REST API — Step by Step

**Module 14 — FastAPI & Django | Full Project**

---

## Why This Matters

> "I know FastAPI" means nothing. "I built a student management API with 12 endpoints, JWT auth, and a PostgreSQL database — here's the GitHub link" gets you shortlisted. This chapter walks you through building exactly that.

---

## Project: Student Management API

### What We're Building

A complete REST API for managing students, courses, and enrollment — like the backend of a real training institute.

**Endpoints we'll build:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | Register a new user |
| POST | /api/login | Login and get JWT token |
| GET | /api/students | List all students (paginated) |
| POST | /api/students | Add a new student |
| GET | /api/students/{id} | Get one student |
| PUT | /api/students/{id} | Update student |
| DELETE | /api/students/{id} | Delete student |
| GET | /api/courses | List all courses |
| POST | /api/courses | Add a course (admin only) |
| POST | /api/enroll | Enroll student in course |
| GET | /api/students/{id}/courses | Get student's courses |
| GET | /api/stats | Dashboard statistics |

> 🖼️ **IMAGE:** API architecture diagram showing Client (browser/Postman) → FastAPI Server (with routes, Pydantic models, JWT auth) → SQLite Database — with arrows showing request/response flow and the 3 database tables (users, students, courses) shown as small entity boxes
> `fastapi-project-architecture.png`

---

### Step 1: Project Setup

```bash
mkdir student-api
cd student-api
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib
```

### File Structure

```
student-api/
├── main.py              ← Entry point
├── database.py          ← Database connection
├── models.py            ← SQLAlchemy models (tables)
├── schemas.py           ← Pydantic schemas (validation)
├── auth.py              ← JWT authentication
├── requirements.txt     ← Dependencies
└── data/
    └── students.db      ← SQLite database (auto-created)
```

### Step 2: Database Setup (database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./data/students.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 3: Models (models.py)

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(15))
    age = Column(Integer)
    city = Column(String(50))
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    duration_months = Column(Integer)
    fee = Column(Float)
    description = Column(String(500))
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
```

### Step 4: Pydantic Schemas (schemas.py)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --- User Schemas ---
class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Student Schemas ---
class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    phone: Optional[str] = None
    age: Optional[int] = Field(None, ge=15, le=60)
    city: Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = Field(None, ge=15, le=60)
    city: Optional[str] = None
    status: Optional[str] = None

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    age: Optional[int]
    city: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Course Schemas ---
class CourseCreate(BaseModel):
    name: str
    duration_months: int = Field(ge=1, le=24)
    fee: float = Field(gt=0)
    description: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    duration_months: int
    fee: float
    description: Optional[str]

    class Config:
        from_attributes = True

# --- Enrollment ---
class EnrollRequest(BaseModel):
    student_id: int
    course_id: int
```

### Step 5: JWT Auth (auth.py)

```python
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
```

### Step 6: Main Application (main.py)

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User, Student, Course, Enrollment
from schemas import *
from auth import *

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API", version="1.0")

# --- Auth Endpoints ---

@app.post("/api/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    
    token = create_token({"sub": user.email})
    return {"access_token": token}

@app.post("/api/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong email or password")
    
    token = create_token({"sub": user.email})
    return {"access_token": token}

# --- Student Endpoints ---

@app.get("/api/students", response_model=list[StudentResponse])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    city: str = None,
    status: str = "active",
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    query = db.query(Student).filter(Student.status == status)
    if city:
        query = query.filter(Student.city == city)
    return query.offset(skip).limit(limit).all()

@app.post("/api/students", response_model=StudentResponse, status_code=201)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student email already exists")
    
    new_student = Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/api/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/api/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    
    db.commit()
    db.refresh(student)
    return student

@app.delete("/api/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted"}

# --- Course Endpoints ---

@app.get("/api/courses", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.post("/api/courses", response_model=CourseResponse, status_code=201)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# --- Enrollment ---

@app.post("/api/enroll")
def enroll_student(
    data: EnrollRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == data.student_id).first()
    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrollment = Enrollment(student_id=data.student_id, course_id=data.course_id)
    db.add(enrollment)
    db.commit()
    return {"message": f"{student.name} enrolled in {course.name}"}

# --- Stats ---

@app.get("/api/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return {
        "total_students": db.query(Student).count(),
        "active_students": db.query(Student).filter(Student.status == "active").count(),
        "total_courses": db.query(Course).count(),
        "total_enrollments": db.query(Enrollment).count()
    }
```

### Step 7: Run & Test

```bash
uvicorn main:app --reload
```

> 🖼️ **IMAGE:** Browser showing FastAPI's automatic Swagger UI docs at localhost:8000/docs — showing the list of endpoints grouped by tags, with "Try it out" buttons visible, and the green/blue/red HTTP method badges (GET/POST/PUT/DELETE)
> `fastapi-swagger-docs.png`

Open `http://localhost:8000/docs` — FastAPI auto-generates interactive API documentation!

### Testing with the Swagger UI

1. **Register:** POST /api/register with `{"email": "test@test.com", "password": "123456"}`
2. **Copy the token** from the response
3. **Click "Authorize"** button at top → paste the token
4. **Create a course:** POST /api/courses
5. **Add students:** POST /api/students
6. **Enroll:** POST /api/enroll
7. **Check stats:** GET /api/stats

---

## What This Project Proves in an Interview

| Skill | Evidence |
|-------|---------|
| API design | RESTful endpoints, proper HTTP methods |
| Authentication | JWT with password hashing |
| Database | SQLAlchemy ORM, relationships, queries |
| Validation | Pydantic schemas with constraints |
| Error handling | 400, 401, 404 responses |
| Pagination | skip/limit query parameters |
| Filtering | Query parameters for city, status |
| Documentation | Auto-generated Swagger docs |

**Interview line:** "I built a Student Management API from scratch with FastAPI — 12 endpoints including JWT authentication, SQLAlchemy ORM with 4 tables, input validation with Pydantic, and auto-generated Swagger documentation. The code is on my GitHub."
