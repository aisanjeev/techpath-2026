# TechPath Backend Setup Guide

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation) (Python package manager)
- (Optional) Docker & Docker Compose for MySQL

## Quick Start (Local Development with SQLite)

The easiest way to get started is using SQLite for local development:

```bash
# 1. Navigate to backend directory
cd techpath-backend

# 2. Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# 3. Install dependencies
poetry install

# 4. Create .env.local file
cp .env.example .env.local

# 5. Create data directories
mkdir -p data/uploads

# 6. Run the application
poetry run uvicorn app.main:app --reload

# Or activate the virtual environment first
poetry shell
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Initial Setup

### Create Admin User

On first run, create an admin user using the setup endpoint:

```bash
curl -X POST http://localhost:8000/api/v1/auth/setup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@techpath.biz",
    "name": "Admin User",
    "password": "SecurePassword123"
  }'
```

### Get Authentication Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@techpath.biz",
    "password": "SecurePassword123"
  }'
```

## Configuration

### Environment Variables

Edit `.env.local` to configure the application:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./data/techpath.db` |
| `SECRET_KEY` | JWT secret key | Change in production! |
| `DEBUG` | Enable debug mode | `true` |
| `STORAGE_TYPE` | `local` or `azure` | `local` |
| `CORS_ORIGINS` | Allowed origins | Frontend URL |

### Using MySQL (Production)

1. Start MySQL with Docker:
```bash
docker-compose up mysql -d
```

2. Update `.env.local`:
```bash
DATABASE_URL=mysql+aiomysql://techpath:techpath123@localhost:3306/techpath
```

3. Run migrations:
```bash
alembic upgrade head
```

### Azure Blob Storage

For production file storage:

```bash
STORAGE_TYPE=azure
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_BLOB_CONTAINER=techpath-uploads
```

### Azure OpenAI

For AI features:

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Running with Docker

```bash
# Start all services (backend, MySQL, Redis)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## API Endpoints Summary

### Authentication
- `POST /api/v1/auth/setup` - Initial admin setup
- `POST /api/v1/auth/login` - Get JWT token
- `POST /api/v1/auth/register` - Create user (admin)
- `GET /api/v1/auth/me` - Current user info

### Services
- `GET /api/v1/services/` - List services
- `GET /api/v1/services/{slug}` - Get service
- `POST /api/v1/services/` - Create service (admin)
- `PUT /api/v1/services/{id}` - Update service (admin)
- `DELETE /api/v1/services/{id}` - Delete service (admin)

### Blog
- `GET /api/v1/blog/posts` - List posts
- `GET /api/v1/blog/posts/{slug}` - Get post
- `POST /api/v1/blog/posts` - Create post (admin)
- `PUT /api/v1/blog/posts/{id}` - Update post (admin)
- `DELETE /api/v1/blog/posts/{id}` - Delete post (admin)
- `GET /api/v1/blog/tags` - List tags

### Contact
- `POST /api/v1/contact/` - Submit contact form
- `POST /api/v1/contact/newsletter` - Subscribe to newsletter
- `GET /api/v1/contact/inquiries` - List inquiries (admin)

### AI
- `POST /api/v1/ai/chat` - Chat with AI assistant
- `POST /api/v1/ai/suggest` - Get service suggestions
- `GET /api/v1/ai/status` - Check AI availability

## Testing

```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app

# Run specific test file
poetry run pytest tests/test_services.py

# Run with verbose output
poetry run pytest -v
```

## Code Quality

```bash
# Format code with Black
poetry run black app tests

# Lint with Ruff
poetry run ruff check app tests

# Fix linting issues automatically
poetry run ruff check --fix app tests

# Type checking with MyPy
poetry run mypy app
```

## Troubleshooting

### Database connection error
- Check DATABASE_URL in .env.local
- Ensure MySQL is running (if using MySQL)
- Check network connectivity

### Import errors
- Activate virtual environment: `poetry shell`
- Run `poetry install`

### Permission errors (uploads)
- Ensure `data/uploads` directory exists and is writable
- Check file permissions

## Poetry Commands Reference

```bash
# Install all dependencies
poetry install

# Install production dependencies only
poetry install --only main

# Add a new dependency
poetry add package-name

# Add a dev dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Run a command in the virtual environment
poetry run <command>

# Activate the virtual environment
poetry shell

# Show installed packages
poetry show

# Export to requirements.txt (if needed)
poetry export -f requirements.txt --output requirements.txt
```

