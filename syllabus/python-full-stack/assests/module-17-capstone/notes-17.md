# Module 17: Full-Stack AI Product — Capstone Development

## 1. Capstone Project Overview

The capstone is your graduation project — a **fully working, deployed web application** with an AI feature. This is not a tutorial exercise. You will:

1. **Pick a product idea** and write the full Spec-Kit (Module 16)
2. **Build the backend** with FastAPI or Django + PostgreSQL
3. **Build the frontend** with HTML/CSS/JS or Django templates + HTMX
4. **Add an AI feature** using LangChain/LangGraph (RAG chatbot, AI agent, or AI workflow)
5. **Set up CI/CD** with GitHub Actions
6. **Deploy live** on Azure or Render
7. **Present a demo** with code walkthrough

### Project Ideas (Pick One or Propose Your Own)

| # | Project | AI Feature | Difficulty |
|---|---------|-----------|-----------|
| 1 | Student Attendance Tracker | AI chatbot that answers "What is Rahul's attendance this month?" | Medium |
| 2 | Job Application Tracker | AI resume analyzer — upload resume, get improvement suggestions | Medium |
| 3 | Hostel Mess Menu App | AI meal recommender based on nutrition and preferences | Medium |
| 4 | Local Shop Inventory Manager | AI demand forecasting — predict which items will sell out | Hard |
| 5 | Course Feedback System | AI sentiment analysis on student feedback | Medium |
| 6 | Document Q&A Tool | RAG chatbot — upload PDFs, ask questions about them | Hard |

---

## 2. Backend Development

### FastAPI Project Structure

```
my-capstone/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + lifespan
│   ├── config.py             # Settings from .env
│   ├── database.py           # SQLAlchemy engine + session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   ├── student.py        # Student model
│   │   └── attendance.py     # Attendance model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py           # Pydantic schemas for User
│   │   ├── student.py        # Pydantic schemas for Student
│   │   └── attendance.py     # Pydantic schemas for Attendance
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py           # Login/register endpoints
│   │   ├── students.py       # Student CRUD endpoints
│   │   └── attendance.py     # Attendance endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py     # LangChain/AI logic
│   └── crud/
│       ├── __init__.py
│       └── base.py           # Generic CRUD operations
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test fixtures
│   ├── test_students.py
│   └── test_attendance.py
├── .env                       # Environment variables (DO NOT commit!)
├── .env.example               # Template for env vars (commit this)
├── .gitignore
├── alembic.ini
├── pyproject.toml             # or requirements.txt
└── README.md
```

### Setting Up FastAPI with PostgreSQL

```python
# app/config.py — Load settings from environment variables

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/mydb"
    SECRET_KEY: str = "change-me-in-production"
    OPENAI_API_KEY: str = ""
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
```

```python
# app/database.py — Async database setup

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """Dependency that provides a database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

```python
# app/main.py — FastAPI application

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, students, attendance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    print("Starting up... connecting to database")
    yield
    print("Shutting down...")


app = FastAPI(
    title="SmartAttend API",
    version="1.0.0",
    description="Student Attendance Management for TechPath Institute",
    lifespan=lifespan,
)

# CORS — allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
```

### Pydantic Schemas (Request/Response Validation)

```python
# app/schemas/student.py

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    batch_id: int | None = None
    city: str | None = None


class StudentUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    city: str | None = None
    is_active: bool | None = None


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None
    batch_id: int | None
    city: str | None
    is_active: bool
    created_at: datetime
```

### CRUD Operations

```python
# app/crud/base.py — Generic CRUD class

from typing import TypeVar, Generic, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_list(self, db: AsyncSession, skip: int = 0, limit: int = 20):
        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
```

### API Endpoints

```python
# app/api/students.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.crud.base import CRUDBase
from app.models.student import Student

router = APIRouter()
student_crud = CRUDBase[Student, StudentCreate, StudentUpdate](Student)


@router.get("/", response_model=list[StudentResponse])
async def list_students(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """List all students with pagination."""
    students = await student_crud.get_list(db, skip=skip, limit=limit)
    return students


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single student by ID."""
    student = await student_crud.get(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentResponse, status_code=201)
async def create_student(
    student_in: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new student."""
    student = await student_crud.create(db, student_in)
    return student
```

---

## 3. Frontend Development

### Option A: HTML/CSS/JS with HTMX (Recommended for Speed)

HTMX lets you build dynamic UIs without writing JavaScript:

```html
<!-- templates/attendance.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartAttend — Mark Attendance</title>
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <h1>SmartAttend</h1>
        <p>Welcome, Amit Sir | <a href="/logout">Logout</a></p>
    </header>

    <main>
        <h2>Mark Attendance — PFS-2026-July</h2>
        <p>Date: 25 July 2026</p>

        <!-- HTMX loads student list from API -->
        <div hx-get="/api/v1/students?batch=PFS-2026-July"
             hx-trigger="load"
             hx-target="#student-list">
            Loading students...
        </div>

        <form hx-post="/api/v1/attendance/bulk"
              hx-target="#result"
              hx-swap="innerHTML">
            <table id="student-list">
                <!-- Students loaded here by HTMX -->
            </table>
            <button type="submit">Submit Attendance</button>
        </form>

        <div id="result"></div>
    </main>
</body>
</html>
```

### Option B: Django Templates (If Using Django Backend)

```html
<!-- templates/students/list.html -->
{% extends "base.html" %}

{% block title %}Students — SmartAttend{% endblock %}

{% block content %}
<h2>Students in {{ batch.name }}</h2>

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>City</th>
            <th>Attendance %</th>
        </tr>
    </thead>
    <tbody>
        {% for student in students %}
        <tr>
            <td>{{ student.name }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.city }}</td>
            <td>{{ student.attendance_percentage }}%</td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="4">No students in this batch yet.</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

### Responsive CSS

```css
/* static/style.css — Mobile-first responsive design */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
}

header {
    background: #2563eb;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

th, td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}

th {
    background: #f3f4f6;
    font-weight: 600;
}

button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
}

button:hover {
    background: #1d4ed8;
}

/* Responsive — stack on mobile */
@media (max-width: 768px) {
    header {
        flex-direction: column;
        text-align: center;
    }

    table, thead, tbody, th, td, tr {
        display: block;
    }

    thead { display: none; }

    td {
        padding: 0.5rem;
        text-align: right;
    }

    td::before {
        content: attr(data-label);
        float: left;
        font-weight: 600;
    }
}
```

---

## 4. AI Feature Integration

### RAG Chatbot with LangChain

RAG (Retrieval-Augmented Generation) lets users ask natural language questions about your data:

```python
# app/services/ai_service.py — RAG chatbot for attendance queries

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings


# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=settings.OPENAI_API_KEY,
    temperature=0,
)

# System prompt for the chatbot
SYSTEM_PROMPT = """You are SmartAttend Assistant, a helpful chatbot for TechPath Institute, Bhopal.
You help trainers and students with attendance-related queries.

You have access to the following attendance data:
{context}

Rules:
- Answer only attendance-related questions
- Use the data provided — do not make up numbers
- If you don't have the data, say "I don't have that information"
- Keep responses short and helpful
- Use simple English
- Mention percentages when relevant
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()


async def ask_attendance_bot(question: str, context: str) -> str:
    """
    Ask the attendance chatbot a question.
    
    Args:
        question: User's question in natural language
        context: Formatted attendance data string
    
    Returns:
        AI-generated response
    """
    response = await chain.ainvoke({
        "question": question,
        "context": context,
    })
    return response


def format_attendance_context(students_data: list[dict]) -> str:
    """Format student attendance data into a string for the LLM context."""
    lines = ["Student Attendance Data:"]
    lines.append("-" * 50)
    for s in students_data:
        lines.append(
            f"Name: {s['name']}, "
            f"Batch: {s['batch']}, "
            f"Total Classes: {s['total']}, "
            f"Present: {s['present']}, "
            f"Absent: {s['absent']}, "
            f"Percentage: {s['percentage']}%"
        )
    return "\n".join(lines)
```

### AI Endpoint

```python
# In app/api/chat.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.ai_service import ask_attendance_bot, format_attendance_context
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """Ask the AI chatbot about attendance data."""
    # Fetch attendance data from database
    # (In real app, query the DB here)
    sample_data = [
        {"name": "Rahul Sharma", "batch": "PFS-2026-July", "total": 20, "present": 18, "absent": 2, "percentage": 90},
        {"name": "Priya Patel", "batch": "PFS-2026-July", "total": 20, "present": 15, "absent": 5, "percentage": 75},
        {"name": "Ananya Gupta", "batch": "PFS-2026-July", "total": 20, "present": 12, "absent": 8, "percentage": 60},
    ]

    context = format_attendance_context(sample_data)
    answer = await ask_attendance_bot(request.question, context)
    return ChatResponse(answer=answer)
```

### AI Agent Alternative (LangGraph)

For more complex AI features, use LangGraph to build an agent:

```python
# app/services/ai_agent.py — LangGraph agent that can query the database

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict


class AgentState(TypedDict):
    question: str
    sql_query: str
    query_result: str
    answer: str


def generate_sql(state: AgentState) -> AgentState:
    """Convert natural language question to SQL query."""
    # In production, use text-to-SQL with proper guardrails
    state["sql_query"] = "SELECT * FROM attendances WHERE ..."
    return state


def execute_query(state: AgentState) -> AgentState:
    """Execute the SQL query (read-only) and get results."""
    # Execute against database (read-only connection)
    state["query_result"] = "Rahul: 90%, Priya: 75%, Ananya: 60%"
    return state


def generate_answer(state: AgentState) -> AgentState:
    """Generate a human-readable answer from query results."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke(
        f"Based on this data: {state['query_result']}, "
        f"answer this question: {state['question']}"
    )
    state["answer"] = response.content
    return state


# Build the agent graph
graph = StateGraph(AgentState)
graph.add_node("generate_sql", generate_sql)
graph.add_node("execute_query", execute_query)
graph.add_node("generate_answer", generate_answer)

graph.add_edge(START, "generate_sql")
graph.add_edge("generate_sql", "execute_query")
graph.add_edge("execute_query", "generate_answer")
graph.add_edge("generate_answer", END)

agent = graph.compile()
```

---

## 5. CI/CD with GitHub Actions

### What is CI/CD?

| Term | Meaning | Example |
|------|---------|---------|
| **CI** (Continuous Integration) | Automatically run tests when code is pushed | Push to GitHub → tests run → pass/fail |
| **CD** (Continuous Deployment) | Automatically deploy when tests pass | Tests pass → deploy to Azure/Render |

### GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      
      - name: Run linting
        run: poetry run ruff check app tests
      
      - name: Run type checking
        run: poetry run mypy app
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://testuser:testpass@localhost:5432/testdb
          SECRET_KEY: test-secret-key
        run: poetry run pytest --cov=app --cov-report=term-missing
      
      - name: Check coverage
        run: |
          poetry run pytest --cov=app --cov-fail-under=70

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
          RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID }}
        run: |
          curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            -H "Content-Type: application/json"
```

### Key CI/CD Concepts

| Concept | What It Does |
|---------|-------------|
| `on: push` | Trigger when code is pushed |
| `on: pull_request` | Trigger when a PR is opened |
| `jobs.test` | Define a job that runs tests |
| `services.postgres` | Spin up a PostgreSQL container for tests |
| `needs: test` | Deploy job waits for test job to pass |
| `secrets.RENDER_API_KEY` | Secure secret stored in GitHub Settings |
| `--cov-fail-under=70` | Fail if test coverage drops below 70% |

---

## 6. Documentation

### README.md Structure

Every capstone project needs a professional README:

```markdown
# SmartAttend — Student Attendance Management

> A full-stack web app for managing student attendance at TechPath Institute, Bhopal.
> Built with FastAPI + PostgreSQL + HTMX + LangChain.

## Live Demo
- **App:** https://smartattend.example.com
- **API Docs:** https://smartattend.example.com/docs

## Features
- Trainers mark attendance for their batch in under 2 minutes
- Students view attendance percentage with calendar view
- AI chatbot answers attendance queries in natural language
- Admin downloads Excel reports
- Mobile-responsive design

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | FastAPI 0.110+ |
| Database | PostgreSQL 15 |
| Frontend | HTML/CSS/JS + HTMX |
| AI | LangChain + OpenAI GPT-4o-mini |
| CI/CD | GitHub Actions |
| Hosting | Render (free tier) |

## Setup

### Prerequisites
- Python 3.12+
- PostgreSQL 15+
- OpenAI API key

### Installation
\```bash
git clone https://github.com/yourusername/smartattend.git
cd smartattend
cp .env.example .env
# Edit .env with your database URL and API keys
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
\```

## API Documentation
Visit `/docs` after starting the server for interactive Swagger UI.

## Architecture
[Include architecture diagram here]

## Screenshots
[Include screenshots of key pages]

## Author
- **Your Name** — [GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile)
- Built as capstone project for Python Full Stack course at TechPath Institute, Bhopal
```

---

## 7. Demo Presentation

### Presentation Structure (15-20 minutes)

| Slide | Content | Time |
|-------|---------|------|
| 1 | Title + your name + product name | 30 sec |
| 2 | Problem statement — what pain point you're solving | 1 min |
| 3 | Live demo — show the working app | 5 min |
| 4 | Architecture diagram — how it all connects | 2 min |
| 5 | Code walkthrough — show 2-3 key files | 3 min |
| 6 | AI feature deep dive — show the chatbot/agent in action | 2 min |
| 7 | CI/CD pipeline — show GitHub Actions running | 1 min |
| 8 | Challenges faced and how you solved them | 2 min |
| 9 | Future improvements | 1 min |
| 10 | Q&A | 2-3 min |

### Demo Tips

1. **Prepare seed data** — never demo with empty screens
2. **Have a backup recording** — in case live demo fails
3. **Show the happy path first** — then show error handling
4. **Keep terminal visible** — show server logs during the demo
5. **Practice 3 times** before the actual presentation
