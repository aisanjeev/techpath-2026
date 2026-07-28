# Full CRUD with PostgreSQL & SQLAlchemy

**Module 06 — FastAPI: Modern API Development | Topic 4**

---

## The Full Stack

In this topic, we connect all the layers:

```
Client Request → FastAPI Endpoint → Pydantic Schema → CRUD Function → SQLAlchemy → PostgreSQL
                                                                                      ↓
Client Response ← FastAPI Endpoint ← Pydantic Schema ← CRUD Function ← SQLAlchemy ← PostgreSQL
```

---

## Database Setup

### database.py — Connection Configuration

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./techpath.db"
# Production: "postgresql+asyncpg://user:pass@localhost:5432/techpath_db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### models.py — Database Models

```python
# app/models/student.py
from sqlalchemy import String, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(50), default="Bhopal")
    fee_paid: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}')>"
```

### schemas.py — Pydantic Schemas

```python
# app/schemas/student.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    city: str = "Bhopal"
    fee_paid: float = Field(ge=0, default=0.0)

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    fee_paid: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    city: str
    fee_paid: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

---

## CRUD Functions

```python
# app/crud/student.py
from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

# CREATE
async def create_student(db: AsyncSession, data: StudentCreate) -> Student:
    student = Student(**data.model_dump())
    db.add(student)
    await db.flush()          # Get the auto-generated id
    await db.refresh(student) # Refresh to load all fields
    return student

# READ ONE
async def get_student(db: AsyncSession, student_id: int) -> Student | None:
    return await db.get(Student, student_id)

# READ ONE BY EMAIL
async def get_student_by_email(db: AsyncSession, email: str) -> Student | None:
    stmt = select(Student).where(Student.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# READ MANY (with pagination and filtering)
async def get_students(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    city: str | None = None,
    is_active: bool | None = None,
    search: str | None = None
) -> tuple[list[Student], int]:
    # Build the query
    stmt = select(Student)

    # Apply filters
    if city:
        stmt = stmt.where(Student.city == city)
    if is_active is not None:
        stmt = stmt.where(Student.is_active == is_active)
    if search:
        stmt = stmt.where(Student.name.ilike(f"%{search}%"))

    # Count total (before pagination)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar()

    # Apply pagination
    stmt = stmt.order_by(Student.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    students = result.scalars().all()

    return students, total

# UPDATE
async def update_student(
    db: AsyncSession, student_id: int, data: StudentUpdate
) -> Student | None:
    student = await db.get(Student, student_id)
    if not student:
        return None

    # Only update fields that were actually sent
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)

    await db.flush()
    await db.refresh(student)
    return student

# DELETE
async def delete_student(db: AsyncSession, student_id: int) -> bool:
    student = await db.get(Student, student_id)
    if not student:
        return False
    await db.delete(student)
    await db.flush()
    return True
```

---

## API Endpoints

```python
# app/api/v1/endpoints/students.py
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.crud.student import (
    create_student, get_student, get_student_by_email,
    get_students, update_student, delete_student
)
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])

# CREATE
@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student_endpoint(
    data: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check if email already exists
    existing = await get_student_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists"
        )
    student = await create_student(db, data)
    return student

# READ MANY
@router.get("/", response_model=list[StudentResponse])
async def list_students(
    response: Response,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    city: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None
):
    students, total = await get_students(db, skip, limit, city, is_active, search)
    response.headers["X-Total-Count"] = str(total)
    return students

# READ ONE
@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_endpoint(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    student = await get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    return student

# UPDATE
@router.patch("/{student_id}", response_model=StudentResponse)
async def update_student_endpoint(
    student_id: int,
    data: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    student = await update_student(db, student_id, data)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    return student

# DELETE
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_endpoint(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await delete_student(db, student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    return None
```

---

## Response Format

A consistent response format makes your API predictable:

```python
# app/schemas/common.py
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class APIResponse(BaseModel):
    success: bool
    data: Any
    timestamp: datetime = datetime.utcnow()

class MessageResponse(BaseModel):
    success: bool = True
    message: str
    timestamp: datetime = datetime.utcnow()

class PaginatedResponse(BaseModel):
    success: bool = True
    data: list[Any]
    total: int
    skip: int
    limit: int
    timestamp: datetime = datetime.utcnow()
```

---

## Error Handling

```python
# app/core/exceptions.py
from fastapi import HTTPException, status

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ConflictError(HTTPException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
```

**Usage:**
```python
from app.core.exceptions import NotFoundError, ConflictError

@router.get("/{student_id}")
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if not student:
        raise NotFoundError(f"Student {student_id} not found")
    return student
```

---

## Testing the API

```bash
# Using curl
# Create
curl -X POST http://localhost:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Rahul Sharma", "email": "rahul@email.com", "city": "Bhopal"}'

# Read all
curl http://localhost:8000/api/v1/students?city=Bhopal&limit=5

# Read one
curl http://localhost:8000/api/v1/students/1

# Update
curl -X PATCH http://localhost:8000/api/v1/students/1 \
  -H "Content-Type: application/json" \
  -d '{"city": "Indore", "fee_paid": 20000}'

# Delete
curl -X DELETE http://localhost:8000/api/v1/students/1
```

Or use the interactive Swagger UI at `http://localhost:8000/docs`.

---

## Summary

| Layer | File | Responsibility |
|-------|------|---------------|
| Database | `database.py` | Connection, session management |
| Models | `models/student.py` | Table structure (SQLAlchemy) |
| Schemas | `schemas/student.py` | Validation (Pydantic) |
| CRUD | `crud/student.py` | Database operations |
| Endpoints | `endpoints/students.py` | HTTP interface |

---

*TechPath Institute — Python Full Stack Development*
