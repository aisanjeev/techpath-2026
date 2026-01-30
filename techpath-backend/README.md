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

**First-time setup (recommended):** After migrations, seed default training page content so `/training` has hero, FAQs, stories, etc.:

```bash
poetry run alembic upgrade head
python scripts/seed_training_page.py
```

Use `python scripts/seed_training_page.py --force` to overwrite existing content with defaults.

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

## Launch checklist

Before going live (or after a fresh deploy):

1. **Migrations:** `poetry run alembic upgrade head`
2. **Seed training page content:** `python scripts/seed_training_page.py` (idempotent; inserts default hero, FAQs, stories, etc. for `/training` if missing)
3. **Smoke-test:** Open `/api/v1/content/training-page` and `/training` (frontend) to confirm content loads. If the content API is down, the frontend uses a minimal fallback so the page still renders.

The training page content is stored in `app_settings` (key `training_landing_content`). The API returns a built-in default when the key is missing, so the site works even without seeding.

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

See [docs/API.md](docs/API.md) for detailed endpoint documentation.

## Deployment (VPS with GitHub Actions)

The backend uses a **branch-based deployment strategy** with staging and production environments.

### Deployment Strategy

| Branch | Environment | URL | Port |
|--------|-------------|-----|------|
| `develop` | Staging | `staging.api.techpath.biz` | 8093 |
| `main` | Production | `api.techpath.biz` | 8092 |

**Workflow:**
1. Push to `develop` → Auto-deploys to **Staging**
2. Test on staging, verify everything works
3. Merge `develop` into `main` → Deploys to **Production** (with approval)

### GitHub Setup

#### Step 1: Create Environments

Go to **Settings > Environments** and create two environments:

1. **staging**
   - No protection rules needed (auto-deploy)
   
2. **production**
   - Enable "Required reviewers" and add yourself
   - Optionally add wait timer (e.g., 5 minutes)

#### Step 2: Add Repository Secrets

Go to **Settings > Secrets and variables > Actions > Secrets**

| Secret | Description | Example |
|--------|-------------|---------|
| `SSH_HOST` | VPS hostname or IP | `api.techpath.biz` |
| `SSH_PASSWORD` | SSH password | `your-password` |
| `SSH_PORT` | SSH port (optional) | `22` |

#### Step 3: Add Environment Secrets

For each environment (staging & production), add:

| Secret | Description |
|--------|-------------|
| `ENV_FILE` | Full `.env` file contents for that environment |

**Example ENV_FILE for Staging:**
```env
DATABASE_URL=mysql+aiomysql://user:pass@localhost/techpath_staging
SECRET_KEY=staging-secret-key
DEBUG=true
STORAGE_TYPE=local
```

**Example ENV_FILE for Production:**
```env
DATABASE_URL=mysql+aiomysql://user:pass@localhost/techpath_prod
SECRET_KEY=super-secure-production-key-change-me
DEBUG=false
STORAGE_TYPE=azure
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=...
AZURE_OPENAI_API_KEY=your-openai-key
```

### VPS Prerequisites

Run these commands **once** on your VPS server:

```bash
# ===== STAGING USER SETUP =====
sudo useradd -m techpath-staging-api
sudo loginctl enable-linger techpath-staging-api

# As techpath-staging-api user:
sudo su - techpath-staging-api
mkdir -p ~/htdocs/staging.api.techpath.biz
mkdir -p ~/.config/systemd/user
exit

# ===== PRODUCTION USER SETUP =====
sudo useradd -m techpath-api
sudo loginctl enable-linger techpath-api

# As techpath-api user:
sudo su - techpath-api
mkdir -p ~/htdocs/api.techpath.biz
mkdir -p ~/.config/systemd/user
exit
```

### Git Workflow

```bash
# Daily development - work on develop branch
git checkout develop
# ... make changes ...
git add .
git commit -m "feat: add new feature"
git push origin develop
# → Auto-deploys to staging

# When ready for production
git checkout main
git merge develop
git push origin main
# → Go to GitHub Actions, approve the deployment
```

### Manual Deployment

You can also trigger deployments manually from the GitHub Actions tab:
1. Go to **Actions > Deploy Backend to VPS**
2. Click **Run workflow**
3. Select environment (staging or production)
4. Click **Run workflow**

### Service Management

**Staging:**
```bash
# SSH as techpath-staging-api
systemctl --user status techpath-staging-api
journalctl --user -u techpath-staging-api -f
systemctl --user restart techpath-staging-api
```

**Production:**
```bash
# SSH as techpath-api
systemctl --user status techpath-api
journalctl --user -u techpath-api -f
systemctl --user restart techpath-api
```

### Environment Comparison

| Aspect | Staging | Production |
|--------|---------|------------|
| Port | 8093 | 8092 |
| Workers | 1 | 2 |
| Auto-deploy | Yes | Requires approval |
| Database | Test data (can reset) | Real data (precious!) |
| Debug mode | Enabled | Disabled |

## License

MIT

