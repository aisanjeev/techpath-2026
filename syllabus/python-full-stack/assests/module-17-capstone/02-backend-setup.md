# Backend Setup: FastAPI + PostgreSQL + Redis + AI

**Module 17 — Full-Stack AI Product: Capstone Development | Topic 2**

---

## Choosing Your Backend Framework

For your capstone, you have two solid choices: FastAPI and Django. Both are production-ready Python frameworks, but they serve different needs.

| Feature | FastAPI | Django |
|---------|---------|--------|
| Speed | Very fast (async by default) | Fast (sync by default, async optional) |
| Learning curve | Moderate (you need to set up things yourself) | Easier (batteries included) |
| API development | Built for APIs (auto Swagger docs) | Needs Django REST Framework add-on |
| Admin panel | No built-in admin | Built-in admin panel |
| Database ORM | SQLAlchemy (you wire it up) | Django ORM (built-in) |
| Best for | API-first projects, microservices | Full web apps with admin needs |
| AI integration | Excellent (async works great with AI APIs) | Good (but sync can be a bottleneck) |

**Recommendation**: If your capstone is API-first (frontend is separate), go with FastAPI. If you want a quick admin panel and server-rendered templates, go with Django.

This topic focuses on FastAPI since it aligns with what you have learned in earlier modules.

---

## Project Scaffolding

A clean project structure is like a well-organized kitchen — you know exactly where everything is, and you can cook faster.

### Recommended FastAPI Project Structure

```
my-capstone/
|-- app/
|   |-- __init__.py
|   |-- main.py              # FastAPI app entry point
|   |-- config.py            # Settings and environment variables
|   |-- database.py          # Database connection setup
|   |-- models/
|   |   |-- __init__.py
|   |   |-- user.py          # User model
|   |   |-- item.py          # Your domain models
|   |-- schemas/
|   |   |-- __init__.py
|   |   |-- user.py          # Pydantic schemas for validation
|   |   |-- item.py
|   |-- api/
|   |   |-- __init__.py
|   |   |-- v1/
|   |       |-- __init__.py
|   |       |-- router.py    # Main router combining all routes
|   |       |-- users.py     # User endpoints
|   |       |-- items.py     # Domain endpoints
|   |-- crud/
|   |   |-- __init__.py
|   |   |-- base.py          # Generic CRUD operations
|   |   |-- user.py
|   |-- services/
|   |   |-- __init__.py
|   |   |-- ai_service.py    # AI/LLM integration
|   |   |-- email_service.py
|   |-- core/
|       |-- __init__.py
|       |-- security.py      # Auth helpers
|       |-- exceptions.py    # Custom exceptions
|-- alembic/                  # Database migrations
|-- tests/
|   |-- __init__.py
|   |-- test_users.py
|   |-- test_items.py
|-- .env
|-- .gitignore
|-- pyproject.toml
|-- README.md
```

### Initializing the Project

```bash
# Create project directory
mkdir my-capstone && cd my-capstone

# Initialize with Poetry (recommended)
poetry init --name my-capstone --python "^3.11"

# Install core dependencies
poetry add fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg alembic
poetry add pydantic-settings python-dotenv

# Install dev dependencies
poetry add --group dev pytest pytest-asyncio httpx black ruff mypy

# Create the folder structure
mkdir -p app/{models,schemas,api/v1,crud,services,core}
mkdir -p tests alembic
```

---

## PostgreSQL Setup

PostgreSQL is the database of choice for production applications. Think of it as upgrading from a notebook (SQLite) to a proper filing cabinet system (PostgreSQL) — it handles multiple users, large datasets, and complex queries with ease.

### Installing PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install postgresql postgresql-contrib

# Verify it is running
sudo systemctl status postgresql

# Create a database for your project
sudo -u postgres psql
```

```sql
-- Inside PostgreSQL shell
CREATE USER capstone_user WITH PASSWORD 'secure_password_123';
CREATE DATABASE capstone_db OWNER capstone_user;
GRANT ALL PRIVILEGES ON DATABASE capstone_db TO capstone_user;
\q
```

### Database Connection in FastAPI

Create `app/database.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=5,
    max_overflow=10,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


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

### Configuration with Pydantic Settings

Create `app/config.py`:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "My Capstone"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://capstone_user:secure_password_123@localhost:5432/capstone_db"
    SECRET_KEY: str = "change-this-to-a-random-string"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
```

---

## Redis Setup for Caching and Queues

Redis is an in-memory data store. Think of it as a sticky note on your desk — it holds frequently needed information so you do not have to dig through your filing cabinet (database) every time.

### Why Use Redis?

| Use Case | Without Redis | With Redis |
|----------|--------------|------------|
| User session data | Query DB every request | Read from memory (instant) |
| API rate limiting | Complex DB logic | Simple counter with expiry |
| AI response caching | Call AI API every time (slow + costly) | Cache responses for same queries |
| Background task queue | Not possible | Use Redis as message broker |

### Installing and Connecting Redis

```bash
# Install Redis
sudo apt install redis-server
sudo systemctl start redis

# Test it
redis-cli ping  # Should return PONG
```

```bash
# Install Python Redis library
poetry add redis
```

### Using Redis in FastAPI

```python
import redis.asyncio as redis
from app.config import settings

# Create Redis connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_cached_response(key: str) -> str | None:
    """Get a cached value from Redis."""
    return await redis_client.get(key)


async def set_cached_response(key: str, value: str, expire_seconds: int = 3600):
    """Cache a value in Redis with expiry."""
    await redis_client.set(key, value, ex=expire_seconds)


# Example: Cache AI responses
async def get_ai_summary(document_id: str, text: str) -> str:
    cache_key = f"summary:{document_id}"

    # Check cache first
    cached = await get_cached_response(cache_key)
    if cached:
        return cached

    # If not cached, call AI and cache the result
    summary = await call_ai_api(text)
    await set_cached_response(cache_key, summary, expire_seconds=86400)  # 24 hours
    return summary
```

---

## Integrating AI (OpenAI / Azure OpenAI)

Adding AI to your capstone is what makes it stand out. Here is how to set it up properly.

### Installing the OpenAI SDK

```bash
poetry add openai
```

### AI Service Setup

Create `app/services/ai_service.py`:

```python
from openai import AsyncOpenAI
from app.config import settings


client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_summary(text: str) -> str:
    """Generate a summary of the given text using GPT."""
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text concisely.",
            },
            {
                "role": "user",
                "content": f"Summarize the following text in 3-4 bullet points:\n\n{text}",
            },
        ],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content


async def answer_question(context: str, question: str) -> str:
    """Answer a question based on provided context (basic RAG)."""
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the question based ONLY on the provided context. "
                    "If the answer is not in the context, say 'I do not have "
                    "enough information to answer this question.'"
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
        max_tokens=300,
        temperature=0.2,
    )
    return response.choices[0].message.content
```

### Creating an AI Endpoint

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.ai_service import generate_summary, answer_question
from pydantic import BaseModel


router = APIRouter(prefix="/ai", tags=["AI"])


class SummaryRequest(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    summary: str


class QuestionRequest(BaseModel):
    context: str
    question: str


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    summary = await generate_summary(request.text)
    return SummaryResponse(summary=summary)


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    answer = await answer_question(request.context, request.question)
    return {"answer": answer}
```

---

## Environment Setup

### The .env File

Create a `.env` file in your project root (never commit this to Git):

```
APP_NAME=My Capstone Project
DEBUG=true
DATABASE_URL=postgresql+asyncpg://capstone_user:secure_password_123@localhost:5432/capstone_db
SECRET_KEY=your-random-secret-key-here
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-openai-key-here
```

### The .gitignore File

```
# Environment
.env
.env.local

# Python
__pycache__/
*.pyc
.mypy_cache/
.pytest_cache/

# IDE
.vscode/
.idea/

# Virtual environment
.venv/
```

---

## Putting It All Together: main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to services
    print(f"Starting {settings.APP_NAME}...")
    yield
    # Shutdown: clean up
    print("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

# Allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}
```

### Running the Server

```bash
# Start the development server
poetry run uvicorn app.main:app --reload --port 8000

# Visit http://localhost:8000/docs to see Swagger UI
# Visit http://localhost:8000/health to check server status
```

---

## Common Mistakes and How to Avoid Them

| Mistake | Why It Happens | Solution |
|---------|---------------|----------|
| Committing `.env` to Git | Forgetting `.gitignore` | Add `.env` to `.gitignore` before first commit |
| Using sync database calls | Copy-pasting old code | Always use `async/await` with `AsyncSession` |
| No error handling on AI calls | Assuming API always works | Wrap AI calls in try/except, return fallback |
| Hardcoding database URL | Quick testing | Always use environment variables via `settings` |
| Not setting up migrations | "I will do it later" | Run `alembic init alembic` on Day 1 |

---

*TechPath Institute — Full-Stack AI Product: Capstone Development*
