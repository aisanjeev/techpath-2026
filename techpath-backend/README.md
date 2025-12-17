# TechPath Backend API

FastAPI backend for TechPath Professional Services - AI-Powered IT Solutions.

## Features

- **FastAPI** with async/await support
- **SQLAlchemy 2.0** with async sessions (SQLite/MySQL)
- **JWT Authentication** with bcrypt password hashing
- **Azure OpenAI** integration for AI chat and suggestions
- **Azure Blob Storage** / Local filesystem for file uploads
- **Pydantic v2** for data validation
- **Alembic** for database migrations
- **Poetry** for dependency management

## Quick Start

```bash
# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Copy environment file
cp .env.example .env.local

# Create upload directory
mkdir -p data/uploads

# Run the development server
poetry run uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the Swagger UI.

## Project Structure

```
techpath-backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Config, security, exceptions
│   ├── crud/            # Database operations
│   ├── db/              # Database session & migrations
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic (AI, storage, email)
│   ├── middleware/      # Request logging, error handlers
│   └── main.py          # FastAPI app
├── data/                # SQLite DB & uploads (local)
├── docs/                # Documentation
├── tests/               # Test suite
├── pyproject.toml       # Poetry dependencies & tool config
└── Dockerfile           # Container configuration
```

## Configuration

The app uses environment variables. Copy `.env.example` to `.env.local`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection | SQLite (local) |
| `STORAGE_TYPE` | `local` or `azure` | `local` |
| `SECRET_KEY` | JWT secret | Change in production! |
| `AZURE_OPENAI_*` | AI configuration | Optional |

## Commands

```bash
# Development
poetry run uvicorn app.main:app --reload

# Testing
poetry run pytest
poetry run pytest --cov=app

# Code Quality
poetry run black app tests
poetry run ruff check app tests
poetry run mypy app

# Database migrations
poetry run alembic upgrade head
poetry run alembic revision --autogenerate -m "description"
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

See [docs/API.md](docs/API.md) for detailed endpoint documentation.

## License

MIT

