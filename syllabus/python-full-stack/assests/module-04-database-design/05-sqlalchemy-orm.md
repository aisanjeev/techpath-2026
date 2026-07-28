# SQLAlchemy ORM — Python Meets the Database

**Module 04 — Database Design, SQL & NoSQL | Topic 5**

---

## What is an ORM?

An ORM (Object-Relational Mapper) lets you work with database tables as Python classes and rows as Python objects. Instead of writing raw SQL, you write Python code.

**Without ORM (raw SQL):**
```python
cursor.execute("INSERT INTO students (name, email) VALUES ('Rahul', 'rahul@email.com')")
```

**With ORM (SQLAlchemy):**
```python
student = Student(name="Rahul", email="rahul@email.com")
session.add(student)
```

Both do the same thing, but the ORM version is:
- Type-safe (IDE auto-complete works)
- Database-agnostic (switch from SQLite to MySQL without changing code)
- Less error-prone (no raw SQL strings to mess up)

---

## SQLAlchemy 2.0 — The Modern Way

SQLAlchemy 2.0 is the current standard. It uses `select()` statements and `Mapped` type hints. The older 1.x style (`session.query()`) is deprecated.

### Installation

```bash
pip install sqlalchemy
pip install aiosqlite        # For async SQLite
pip install pymysql           # For MySQL
pip install aiomysql          # For async MySQL
```

---

## Setting Up the Database Connection

### Sync Connection (Simple)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Connection string
DATABASE_URL = "sqlite:///./techpath.db"
# For MySQL: "mysql+pymysql://user:pass@localhost:3306/techpath_db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL

# Create session factory
SessionLocal = sessionmaker(bind=engine)
```

### Async Connection (Production)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./techpath.db"
# For MySQL: "mysql+aiomysql://user:pass@localhost:3306/techpath_db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

---

## Defining Models (Tables as Python Classes)

### Base Class (SQLAlchemy 2.0 Style)

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text
from datetime import datetime

class Base(DeclarativeBase):
    pass
```

### Student Model

```python
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(50), default="Bhopal")
    fee_paid: Mapped[float] = mapped_column(default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', city='{self.city}')>"
```

### Course Model

```python
class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    duration_weeks: Mapped[int] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
```

### Enrollment Model (Junction Table)

```python
class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    enrolled_on: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
```

### Creating All Tables

```python
# Sync
Base.metadata.create_all(engine)

# Async
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

---

## Relationships — Connecting Models

Relationships let you navigate between related objects in Python.

```python
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    # Relationship: One student has many enrollments
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    # Relationship: One course has many enrollments
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
```

**Using relationships:**
```python
# Access a student's courses
student = session.get(Student, 1)
for enrollment in student.enrollments:
    print(enrollment.course.title)
```

---

## CRUD Operations

### Create (Insert)

```python
from sqlalchemy import select

# Sync
with SessionLocal() as session:
    student = Student(name="Rahul Sharma", email="rahul@email.com", city="Bhopal")
    session.add(student)
    session.commit()
    session.refresh(student)  # Get the auto-generated id
    print(student.id)  # 1

# Async
async with AsyncSessionLocal() as session:
    student = Student(name="Priya Patel", email="priya@email.com", city="Pune")
    session.add(student)
    await session.commit()
    await session.refresh(student)
```

**Insert multiple rows:**
```python
students = [
    Student(name="Amit Kumar", email="amit@email.com", city="Delhi"),
    Student(name="Sneha Gupta", email="sneha@email.com", city="Pune"),
    Student(name="Ananya Singh", email="ananya@email.com", city="Bhopal"),
]
session.add_all(students)
session.commit()
```

### Read (Select)

```python
# Get by primary key
student = session.get(Student, 1)

# Select all
stmt = select(Student)
result = session.execute(stmt)
students = result.scalars().all()

# Select with filter
stmt = select(Student).where(Student.city == "Bhopal")
students = session.execute(stmt).scalars().all()

# Select with multiple conditions
stmt = select(Student).where(
    Student.city == "Bhopal",
    Student.is_active == True
)

# Select with ordering
stmt = select(Student).order_by(Student.name)

# Select with limit and offset (pagination)
stmt = select(Student).order_by(Student.id).limit(10).offset(0)

# Select one row (error if more than one)
stmt = select(Student).where(Student.email == "rahul@email.com")
student = session.execute(stmt).scalar_one_or_none()

# Count
from sqlalchemy import func
stmt = select(func.count()).select_from(Student)
total = session.execute(stmt).scalar()
```

### Update

```python
# Method 1: Get and modify
student = session.get(Student, 1)
student.city = "Indore"
student.fee_paid = 20000.0
session.commit()

# Method 2: Bulk update
from sqlalchemy import update
stmt = update(Student).where(Student.city == "Bhopal").values(is_active=False)
session.execute(stmt)
session.commit()
```

### Delete

```python
# Method 1: Get and delete
student = session.get(Student, 5)
session.delete(student)
session.commit()

# Method 2: Bulk delete
from sqlalchemy import delete
stmt = delete(Student).where(Student.is_active == False)
session.execute(stmt)
session.commit()
```

---

## Joins in SQLAlchemy

```python
# Inner join
stmt = (
    select(Student.name, Course.title)
    .join(Enrollment, Student.id == Enrollment.student_id)
    .join(Course, Enrollment.course_id == Course.id)
)

# Left join
stmt = (
    select(Student.name, Course.title)
    .outerjoin(Enrollment, Student.id == Enrollment.student_id)
    .outerjoin(Course, Enrollment.course_id == Course.id)
)

# With GROUP BY
from sqlalchemy import func
stmt = (
    select(Student.city, func.count(Student.id).label("count"))
    .group_by(Student.city)
    .having(func.count(Student.id) > 2)
)
```

---

## Sessions and Transactions

### The Session Pattern

```python
# FastAPI dependency pattern
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()    # Auto-commit if no error
        except Exception:
            await session.rollback()  # Auto-rollback on error
            raise
```

### Flush vs Commit

| Operation | What It Does |
|-----------|-------------|
| `session.flush()` | Sends SQL to the database but does NOT finalize (can still rollback) |
| `session.commit()` | Finalizes all changes permanently |
| `session.rollback()` | Undoes all changes since the last commit |
| `session.refresh(obj)` | Reloads the object from the database |

**When to flush:** After creating an object, flush to get its auto-generated `id` without committing the full transaction.

```python
student = Student(name="Vikram", email="vikram@email.com")
session.add(student)
await session.flush()       # id is now assigned
print(student.id)           # 6
# ... do more work ...
await session.commit()      # NOW it is permanent
```

---

## Alembic — Database Migrations

Alembic tracks changes to your models and generates migration scripts to update the database schema.

### Setup

```bash
pip install alembic
alembic init migrations
```

### Configuration

Edit `alembic.ini`:
```ini
sqlalchemy.url = sqlite:///./techpath.db
```

Edit `migrations/env.py`:
```python
from app.models import Base
target_metadata = Base.metadata
```

### Creating and Running Migrations

```bash
# Generate a migration from model changes
alembic revision --autogenerate -m "create students table"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# See current migration status
alembic current

# See migration history
alembic history
```

### What a Migration File Looks Like

```python
# migrations/versions/abc123_create_students_table.py
def upgrade():
    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(150), unique=True, nullable=False),
        sa.Column('city', sa.String(50), server_default='Bhopal'),
    )

def downgrade():
    op.drop_table('students')
```

### Common Alembic Commands

| Command | What It Does |
|---------|-------------|
| `alembic revision --autogenerate -m "msg"` | Generate migration from model changes |
| `alembic upgrade head` | Apply all migrations |
| `alembic upgrade +1` | Apply next migration |
| `alembic downgrade -1` | Rollback one migration |
| `alembic current` | Show current version |
| `alembic history` | Show all migrations |
| `alembic heads` | Show latest version(s) |

---

## Complete Example: FastAPI + SQLAlchemy

```python
# models.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    enrollments = relationship("Enrollment", back_populates="student")

# crud.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_student(db: AsyncSession, name: str, email: str):
    student = Student(name=name, email=email)
    db.add(student)
    await db.flush()
    return student

async def get_students(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Student).order_by(Student.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_student_by_email(db: AsyncSession, email: str):
    stmt = select(Student).where(Student.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| ORM | Maps Python classes to database tables |
| Mapped columns | Define columns with type hints |
| Relationships | Navigate between related objects |
| select() | SQLAlchemy 2.0 way to query |
| flush() | Send SQL without committing |
| commit() | Finalize all changes permanently |
| Alembic | Track and apply schema changes |

---

*TechPath Institute — Python Full Stack Development*
