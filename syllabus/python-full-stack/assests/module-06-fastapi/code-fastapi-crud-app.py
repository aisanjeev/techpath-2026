"""
TechPath Institute — FastAPI CRUD Application
===============================================
A complete REST API for managing Students and Courses
with SQLAlchemy database, Pydantic validation, search,
filter, sort, and pagination.

Run this file:
    pip install fastapi uvicorn sqlalchemy aiosqlite
    uvicorn code-fastapi-crud-app:app --reload

Then open:
    http://localhost:8000/docs   — Swagger UI (test all endpoints)
    http://localhost:8000/redoc  — ReDoc (read-only docs)
"""

# ──────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────

from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# ──────────────────────────────────────────────
# DATABASE SETUP
# ──────────────────────────────────────────────

DATABASE_URL = "sqlite+aiosqlite:///./techpath_students.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Dependency: provides a database session for each request."""
    async with async_session() as session:
        yield session


# ──────────────────────────────────────────────
# SQLALCHEMY MODELS (Database Tables)
# ──────────────────────────────────────────────

class CourseDB(Base):
    """Course table — stores available courses at TechPath Institute."""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    duration_months = Column(Integer, nullable=False)
    fee = Column(Float, nullable=False)
    description = Column(String(500), default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship: one course has many students
    students = relationship("StudentDB", back_populates="course")


class StudentDB(Base):
    """Student table — stores enrolled students."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(15), default="")
    city = Column(String(50), default="Bhopal")
    marks = Column(Float, default=0.0)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship: each student belongs to one course
    course = relationship("CourseDB", back_populates="students")


# ──────────────────────────────────────────────
# PYDANTIC SCHEMAS (Request / Response Validation)
# ──────────────────────────────────────────────

# --- Course Schemas ---

class CourseCreate(BaseModel):
    """Schema for creating a new course."""
    name: str = Field(min_length=2, max_length=100, description="Course name")
    duration_months: int = Field(ge=1, le=36, description="Duration in months (1-36)")
    fee: float = Field(ge=0, description="Course fee in INR")
    description: str = Field(default="", max_length=500)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Course name cannot be blank")
        return v.strip()


class CourseUpdate(BaseModel):
    """Schema for updating a course (all fields optional)."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    duration_months: Optional[int] = Field(None, ge=1, le=36)
    fee: Optional[float] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)


class CourseResponse(BaseModel):
    """Schema for course data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    duration_months: int
    fee: float
    description: str
    created_at: datetime


# --- Student Schemas ---

class StudentCreate(BaseModel):
    """Schema for creating a new student."""
    name: str = Field(min_length=2, max_length=100, description="Full name")
    email: str = Field(description="Email address")
    phone: str = Field(default="", max_length=15, description="Phone number")
    city: str = Field(default="Bhopal", max_length=50, description="City")
    marks: float = Field(default=0, ge=0, le=100, description="Marks (0-100)")
    course_id: Optional[int] = Field(None, description="Course ID")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format — must contain @ and a domain")
        return v.lower().strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()


class StudentUpdate(BaseModel):
    """Schema for updating a student (all fields optional)."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=15)
    city: Optional[str] = Field(None, max_length=50)
    marks: Optional[float] = Field(None, ge=0, le=100)
    course_id: Optional[int] = None


class StudentResponse(BaseModel):
    """Schema for student data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str
    city: str
    marks: float
    course_id: Optional[int]
    created_at: datetime


# ──────────────────────────────────────────────
# FASTAPI APP
# ──────────────────────────────────────────────

app = FastAPI(
    title="TechPath Student Management API",
    description="REST API for managing students and courses at TechPath Institute, Bhopal",
    version="1.0.0",
    contact={"name": "TechPath Institute", "email": "info@techpath.biz"},
)


# ──────────────────────────────────────────────
# STARTUP — Create Tables & Seed Sample Data
# ──────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    """Create database tables and insert sample data on first run."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed sample data if tables are empty
    async with async_session() as db:
        result = await db.execute(select(func.count(CourseDB.id)))
        if result.scalar() == 0:
            # Add sample courses
            courses = [
                CourseDB(name="Python Full Stack", duration_months=12, fee=45000.0,
                         description="Complete Python web development with Django and FastAPI"),
                CourseDB(name="ADCA", duration_months=12, fee=25000.0,
                         description="Advanced Diploma in Computer Applications"),
                CourseDB(name="DCA", duration_months=6, fee=15000.0,
                         description="Diploma in Computer Applications"),
                CourseDB(name="Data Science", duration_months=9, fee=55000.0,
                         description="Data analysis, ML, and visualization with Python"),
            ]
            db.add_all(courses)
            await db.flush()

            # Add sample students with Indian names and cities
            students = [
                StudentDB(name="Rahul Sharma", email="rahul@email.com",
                          phone="+919876543210", city="Bhopal", marks=85, course_id=1),
                StudentDB(name="Priya Patel", email="priya@email.com",
                          phone="+919876543211", city="Indore", marks=92, course_id=1),
                StudentDB(name="Amit Kumar", email="amit@email.com",
                          phone="+919876543212", city="Delhi", marks=78, course_id=2),
                StudentDB(name="Sneha Verma", email="sneha@email.com",
                          phone="+919876543213", city="Pune", marks=88, course_id=2),
                StudentDB(name="Vikram Singh", email="vikram@email.com",
                          phone="+919876543214", city="Bhopal", marks=71, course_id=3),
                StudentDB(name="Ananya Mishra", email="ananya@email.com",
                          phone="+919876543215", city="Hyderabad", marks=95, course_id=1),
                StudentDB(name="Karan Joshi", email="karan@email.com",
                          phone="+919876543216", city="Bhopal", marks=65, course_id=3),
                StudentDB(name="Neha Gupta", email="neha@email.com",
                          phone="+919876543217", city="Indore", marks=82, course_id=4),
            ]
            db.add_all(students)
            await db.commit()
            print("Database seeded with sample courses and students!")


# ──────────────────────────────────────────────
# HOME ROUTE
# ──────────────────────────────────────────────

@app.get("/")
async def home():
    """Welcome endpoint with API information."""
    return {
        "success": True,
        "data": {
            "message": "Welcome to TechPath Student Management API!",
            "docs": "/docs",
            "redoc": "/redoc",
            "endpoints": {
                "courses": "/api/courses",
                "students": "/api/students",
            }
        }
    }


# ──────────────────────────────────────────────
# COURSE ENDPOINTS
# ──────────────────────────────────────────────

@app.post("/api/courses", status_code=201)
async def create_course(data: CourseCreate, db: AsyncSession = Depends(get_db)):
    """Create a new course."""
    # Check if course name already exists
    result = await db.execute(select(CourseDB).where(CourseDB.name == data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"Course '{data.name}' already exists")

    course = CourseDB(**data.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return {"success": True, "data": CourseResponse.model_validate(course)}


@app.get("/api/courses")
async def list_courses(
    search: Optional[str] = Query(None, description="Search by course name"),
    db: AsyncSession = Depends(get_db),
):
    """List all courses, optionally filtered by name search."""
    query = select(CourseDB)
    if search:
        query = query.where(CourseDB.name.ilike(f"%{search}%"))
    query = query.order_by(CourseDB.name)

    result = await db.execute(query)
    courses = result.scalars().all()
    return {
        "success": True,
        "total": len(courses),
        "data": [CourseResponse.model_validate(c) for c in courses],
    }


@app.get("/api/courses/{course_id}")
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single course by ID."""
    result = await db.execute(select(CourseDB).where(CourseDB.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"success": True, "data": CourseResponse.model_validate(course)}


@app.put("/api/courses/{course_id}")
async def update_course(
    course_id: int, data: CourseUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a course (partial update — only send fields you want to change)."""
    result = await db.execute(select(CourseDB).where(CourseDB.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)

    await db.commit()
    await db.refresh(course)
    return {"success": True, "data": CourseResponse.model_validate(course)}


@app.delete("/api/courses/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a course by ID."""
    result = await db.execute(select(CourseDB).where(CourseDB.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.delete(course)
    await db.commit()
    return {"success": True, "message": f"Deleted course: {course.name}"}


# ──────────────────────────────────────────────
# STUDENT ENDPOINTS
# ──────────────────────────────────────────────

@app.post("/api/students", status_code=201)
async def create_student(data: StudentCreate, db: AsyncSession = Depends(get_db)):
    """Create a new student."""
    # Check if email already exists
    result = await db.execute(select(StudentDB).where(StudentDB.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"Email '{data.email}' is already registered")

    # Validate course_id if provided
    if data.course_id:
        course_check = await db.execute(
            select(CourseDB).where(CourseDB.id == data.course_id)
        )
        if not course_check.scalar_one_or_none():
            raise HTTPException(status_code=404, detail=f"Course with ID {data.course_id} not found")

    student = StudentDB(**data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return {"success": True, "data": StudentResponse.model_validate(student)}


@app.get("/api/students")
async def list_students(
    search: Optional[str] = Query(None, description="Search by name"),
    city: Optional[str] = Query(None, description="Filter by city"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    sort: str = Query("id", description="Sort by: id, name, marks, city"),
    order: str = Query("asc", description="Sort order: asc or desc"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Records per page (max 100)"),
    db: AsyncSession = Depends(get_db),
):
    """
    List students with search, filter, sort, and pagination.

    Examples:
        /api/students?city=Bhopal
        /api/students?search=rahul&sort=marks&order=desc
        /api/students?course_id=1&skip=0&limit=5
    """
    query = select(StudentDB)

    # Search by name
    if search:
        query = query.where(StudentDB.name.ilike(f"%{search}%"))

    # Filter by city
    if city:
        query = query.where(StudentDB.city.ilike(city))

    # Filter by course
    if course_id:
        query = query.where(StudentDB.course_id == course_id)

    # Get total count before pagination
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Sort
    sort_columns = {
        "id": StudentDB.id,
        "name": StudentDB.name,
        "marks": StudentDB.marks,
        "city": StudentDB.city,
    }
    sort_col = sort_columns.get(sort, StudentDB.id)
    if order == "desc":
        sort_col = sort_col.desc()
    query = query.order_by(sort_col)

    # Pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    students = result.scalars().all()

    return {
        "success": True,
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [StudentResponse.model_validate(s) for s in students],
    }


@app.get("/api/students/{student_id}")
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single student by ID."""
    result = await db.execute(select(StudentDB).where(StudentDB.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"success": True, "data": StudentResponse.model_validate(student)}


@app.put("/api/students/{student_id}")
async def update_student(
    student_id: int, data: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a student (partial update — only send fields you want to change)."""
    result = await db.execute(select(StudentDB).where(StudentDB.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)

    await db.commit()
    await db.refresh(student)
    return {"success": True, "data": StudentResponse.model_validate(student)}


@app.delete("/api/students/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a student by ID."""
    result = await db.execute(select(StudentDB).where(StudentDB.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()
    return {"success": True, "message": f"Deleted student: {student.name}"}


# ──────────────────────────────────────────────
# STATS ENDPOINT
# ──────────────────────────────────────────────

@app.get("/api/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get summary statistics for students and courses."""
    # Student stats
    student_count = await db.execute(select(func.count(StudentDB.id)))
    avg_marks = await db.execute(select(func.avg(StudentDB.marks)))
    max_marks = await db.execute(select(func.max(StudentDB.marks)))
    min_marks = await db.execute(select(func.min(StudentDB.marks)))

    # Course stats
    course_count = await db.execute(select(func.count(CourseDB.id)))

    # City-wise count
    city_query = select(StudentDB.city, func.count(StudentDB.id)).group_by(StudentDB.city)
    city_result = await db.execute(city_query)
    city_counts = {row[0]: row[1] for row in city_result.all()}

    return {
        "success": True,
        "data": {
            "total_students": student_count.scalar() or 0,
            "total_courses": course_count.scalar() or 0,
            "average_marks": round(avg_marks.scalar() or 0, 1),
            "highest_marks": max_marks.scalar() or 0,
            "lowest_marks": min_marks.scalar() or 0,
            "students_by_city": city_counts,
        }
    }


# ──────────────────────────────────────────────
# RUN (if executed directly)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print("Starting TechPath Student Management API...")
    print("Open http://localhost:8000/docs for Swagger UI")
    uvicorn.run("code-fastapi-crud-app:app", host="127.0.0.1", port=8000, reload=True)
