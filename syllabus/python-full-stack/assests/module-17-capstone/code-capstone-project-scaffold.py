"""
=============================================================================
TechPath Capstone Project — FastAPI Application Scaffold
=============================================================================
This is a starter template for your capstone project.
It includes:
  - FastAPI app with CORS and health check
  - Async SQLAlchemy database setup (PostgreSQL or SQLite)
  - Pydantic schemas with validation
  - Generic CRUD operations
  - Sample endpoints for a student management system
  - AI chatbot endpoint (placeholder — connect your LangChain code)

How to use:
  1. Copy this file into your project as app/main.py
  2. Install dependencies: pip install fastapi uvicorn sqlalchemy[asyncio] pydantic
  3. Create a .env file with DATABASE_URL
  4. Run: uvicorn app.main:app --reload
  5. Open http://localhost:8000/docs to see Swagger UI

For PostgreSQL: pip install asyncpg
For SQLite:     pip install aiosqlite
=============================================================================
"""

import os
from datetime import datetime, date
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, select, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, relationship


# =============================================================================
# Configuration
# =============================================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./data/capstone.db"  # Default: SQLite for development
)
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")


# =============================================================================
# Database Setup
# =============================================================================

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Dependency: provides a database session per request."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# =============================================================================
# Models (Database Tables)
# =============================================================================

class Student(Base):
    """Student model — represents a student enrolled at TechPath Institute."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=True)
    batch = Column(String(50), nullable=True)           # e.g., "PFS-2026-July"
    city = Column(String(50), nullable=True)             # e.g., "Bhopal"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship: one student has many attendance records
    attendances = relationship("Attendance", back_populates="student")


class Attendance(Base):
    """Attendance model — one record per student per day."""
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(10), nullable=False)          # "present", "absent", "late"
    marked_by = Column(String(100), nullable=True)       # trainer name
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: each attendance belongs to a student
    student = relationship("Student", back_populates="attendances")


# =============================================================================
# Pydantic Schemas (Request/Response Validation)
# =============================================================================

class StudentCreate(BaseModel):
    """Schema for creating a new student."""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    batch: Optional[str] = None
    city: Optional[str] = None


class StudentUpdate(BaseModel):
    """Schema for updating a student (all fields optional)."""
    name: Optional[str] = None
    phone: Optional[str] = None
    batch: Optional[str] = None
    city: Optional[str] = None
    is_active: Optional[bool] = None


class StudentResponse(BaseModel):
    """Schema for student in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: Optional[str]
    batch: Optional[str]
    city: Optional[str]
    is_active: bool
    created_at: datetime


class AttendanceCreate(BaseModel):
    """Schema for marking attendance."""
    student_id: int
    date: date
    status: str  # "present", "absent", or "late"
    marked_by: Optional[str] = None


class AttendanceResponse(BaseModel):
    """Schema for attendance in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    date: date
    status: str
    marked_by: Optional[str]
    created_at: datetime


class AttendanceReportItem(BaseModel):
    """Schema for attendance report per student."""
    student_id: int
    student_name: str
    total_classes: int
    present: int
    absent: int
    percentage: float


class ChatRequest(BaseModel):
    """Schema for AI chatbot request."""
    question: str


class ChatResponse(BaseModel):
    """Schema for AI chatbot response."""
    answer: str


# =============================================================================
# Application Setup
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup (for development only)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created. Server is ready.")
    print("Open http://localhost:8000/docs for API documentation.")
    yield
    print("Shutting down...")


app = FastAPI(
    title="TechPath Capstone API",
    description="Full-stack AI product — Student Management System for TechPath Institute, Bhopal",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Health Check
# =============================================================================

@app.get("/api/v1/health", tags=["System"])
async def health_check():
    """Check if the server is running."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "message": "TechPath Capstone API is running",
    }


# =============================================================================
# Student Endpoints
# =============================================================================

@app.get("/api/v1/students", response_model=list[StudentResponse], tags=["Students"])
async def list_students(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    batch: Optional[str] = Query(None, description="Filter by batch name"),
    city: Optional[str] = Query(None, description="Filter by city"),
    db: AsyncSession = Depends(get_db),
):
    """
    List all students with optional filters.

    Examples:
      - GET /api/v1/students — all students
      - GET /api/v1/students?batch=PFS-2026-July — filter by batch
      - GET /api/v1/students?city=Bhopal&limit=10 — filter by city, limit to 10
    """
    query = select(Student).where(Student.is_active == True)

    if batch:
        query = query.where(Student.batch == batch)
    if city:
        query = query.where(Student.city == city)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@app.get("/api/v1/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single student by their ID."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/api/v1/students", response_model=StudentResponse, status_code=201, tags=["Students"])
async def create_student(student_in: StudentCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new student.

    Example request body:
    {
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "phone": "9876543210",
        "batch": "PFS-2026-July",
        "city": "Bhopal"
    }
    """
    # Check if email already exists
    existing = await db.execute(select(Student).where(Student.email == student_in.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="A student with this email already exists")

    student = Student(**student_in.model_dump())
    db.add(student)
    await db.flush()
    await db.refresh(student)
    return student


@app.patch("/api/v1/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a student's details (partial update — only send fields you want to change)."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)

    await db.flush()
    await db.refresh(student)
    return student


# =============================================================================
# Attendance Endpoints
# =============================================================================

@app.post("/api/v1/attendance", response_model=AttendanceResponse, status_code=201, tags=["Attendance"])
async def mark_attendance(
    attendance_in: AttendanceCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Mark attendance for a student.

    Example:
    {
        "student_id": 1,
        "date": "2026-07-25",
        "status": "present",
        "marked_by": "Amit Kumar"
    }
    """
    # Validate student exists
    result = await db.execute(select(Student).where(Student.id == attendance_in.student_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Student not found")

    # Validate status
    if attendance_in.status not in ("present", "absent", "late"):
        raise HTTPException(status_code=400, detail="Status must be 'present', 'absent', or 'late'")

    attendance = Attendance(**attendance_in.model_dump())
    db.add(attendance)
    await db.flush()
    await db.refresh(attendance)
    return attendance


@app.get(
    "/api/v1/students/{student_id}/attendance",
    response_model=list[AttendanceResponse],
    tags=["Attendance"],
)
async def get_student_attendance(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get all attendance records for a specific student."""
    # Verify student exists
    result = await db.execute(select(Student).where(Student.id == student_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Student not found")

    result = await db.execute(
        select(Attendance)
        .where(Attendance.student_id == student_id)
        .order_by(Attendance.date.desc())
    )
    return result.scalars().all()


@app.get("/api/v1/reports/attendance", response_model=list[AttendanceReportItem], tags=["Reports"])
async def attendance_report(
    batch: str = Query(..., description="Batch name to generate report for"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get attendance summary report for all students in a batch.

    Returns: name, total classes, present count, absent count, percentage.
    """
    # Get all students in the batch
    result = await db.execute(select(Student).where(Student.batch == batch))
    students = result.scalars().all()

    if not students:
        raise HTTPException(status_code=404, detail=f"No students found in batch '{batch}'")

    report = []
    for student in students:
        # Count attendance records
        total_result = await db.execute(
            select(func.count()).where(Attendance.student_id == student.id)
        )
        total = total_result.scalar() or 0

        present_result = await db.execute(
            select(func.count()).where(
                Attendance.student_id == student.id,
                Attendance.status == "present",
            )
        )
        present = present_result.scalar() or 0

        absent = total - present
        percentage = round((present / total * 100), 1) if total > 0 else 0.0

        report.append(AttendanceReportItem(
            student_id=student.id,
            student_name=student.name,
            total_classes=total,
            present=present,
            absent=absent,
            percentage=percentage,
        ))

    return report


# =============================================================================
# AI Chatbot Endpoint (Placeholder — Connect Your LangChain Code)
# =============================================================================

@app.post("/api/v1/chat", response_model=ChatResponse, tags=["AI Chatbot"])
async def chat_with_ai(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Ask the AI chatbot about attendance data.

    Example questions:
    - "What is Rahul's attendance percentage?"
    - "Which students have less than 75% attendance?"
    - "How many classes did Priya miss this month?"

    TODO: Connect this to your LangChain RAG chain (see ai_service.py in notes).
    """
    # --- PLACEHOLDER: Replace with actual LangChain integration ---
    answer = (
        f"I received your question: '{request.question}'. "
        f"This is a placeholder response. "
        f"Connect LangChain to get real AI-powered answers. "
        f"See app/services/ai_service.py for the implementation."
    )
    return ChatResponse(answer=answer)


# =============================================================================
# Seed Data Endpoint (Development Only)
# =============================================================================

@app.post("/api/v1/seed", tags=["System"])
async def seed_database(db: AsyncSession = Depends(get_db)):
    """
    Populate the database with sample data for development and testing.
    WARNING: Only use in development — do not expose in production!
    """
    # Sample students — Indian names, Indian cities
    sample_students = [
        Student(name="Rahul Sharma", email="rahul@example.com", phone="9876543210", batch="PFS-2026-July", city="Bhopal"),
        Student(name="Priya Patel", email="priya@example.com", phone="9876543211", batch="PFS-2026-July", city="Pune"),
        Student(name="Ananya Gupta", email="ananya@example.com", phone="9876543212", batch="PFS-2026-July", city="Delhi"),
        Student(name="Vikram Singh", email="vikram@example.com", phone="9876543213", batch="PFS-2026-July", city="Jaipur"),
        Student(name="Neha Reddy", email="neha@example.com", phone="9876543214", batch="PFS-2026-Aug", city="Hyderabad"),
        Student(name="Arjun Mehta", email="arjun@example.com", phone="9876543215", batch="PFS-2026-Aug", city="Mumbai"),
    ]

    for student in sample_students:
        # Skip if already exists
        existing = await db.execute(select(Student).where(Student.email == student.email))
        if not existing.scalar_one_or_none():
            db.add(student)

    await db.flush()

    # Sample attendance data
    sample_dates = [
        date(2026, 7, 1), date(2026, 7, 2), date(2026, 7, 3),
        date(2026, 7, 4), date(2026, 7, 7), date(2026, 7, 8),
    ]

    # Rahul: mostly present (good attendance)
    for d in sample_dates:
        status = "absent" if d == date(2026, 7, 3) else "present"
        db.add(Attendance(student_id=1, date=d, status=status, marked_by="Amit Kumar"))

    # Priya: some absences
    for d in sample_dates:
        status = "absent" if d in [date(2026, 7, 2), date(2026, 7, 7)] else "present"
        db.add(Attendance(student_id=2, date=d, status=status, marked_by="Amit Kumar"))

    # Ananya: poor attendance
    for d in sample_dates:
        status = "present" if d in [date(2026, 7, 1), date(2026, 7, 4)] else "absent"
        db.add(Attendance(student_id=3, date=d, status=status, marked_by="Amit Kumar"))

    await db.flush()

    return {
        "message": "Database seeded with sample data",
        "students_added": len(sample_students),
        "attendance_records": len(sample_dates) * 3,
    }


# =============================================================================
# Run the server
# =============================================================================
# Command: uvicorn app.main:app --reload
# Then open: http://localhost:8000/docs
# =============================================================================
