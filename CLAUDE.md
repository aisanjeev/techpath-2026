# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TechPath is a monorepo for an IT training SaaS platform with three applications:

- **`techpath-frontend/`** — Public website (Astro 5 + React + Tailwind, deployed to Vercel)
- **`techpath-backend/`** — REST API (FastAPI + SQLAlchemy 2.0, deployed to VPS)
- **`techpath-admin/`** — CMS dashboard (Next.js 14 App Router + TypeScript, deployed to Vercel)

---

## Commands

### Frontend (Astro)
```bash
cd techpath-frontend
npm run dev          # Dev server at port 4321
npm run build        # Type check + build
npm run lint         # ESLint
npm run lint:fix     # Fix lint errors
npm run format       # Prettier
npm run test         # Playwright e2e tests
npm run test:ui      # Playwright UI mode
```

### Backend (FastAPI)
```bash
cd techpath-backend
poetry install                                                    # Install deps
poetry run uvicorn app.main:app --reload                          # Dev server at :8000
poetry run pytest                                                 # All tests
poetry run pytest tests/path/to/test_file.py::test_name          # Single test
poetry run pytest --cov=app                                       # With coverage
poetry run black app tests                                        # Format
poetry run ruff check app tests                                   # Lint
poetry run mypy app                                               # Type check
poetry run alembic upgrade head                                   # Apply migrations
poetry run alembic revision --autogenerate -m "description"       # New migration
```

### Admin (Next.js)
```bash
cd techpath-admin
npm run dev          # Dev server at port 3000
npm run build
npm run lint
```

---

## Architecture

### Data Flow
```
Public users → Astro frontend (SSG/ISR) → FastAPI backend → SQLite/MySQL
Admin users  → Next.js admin             → FastAPI backend (JWT-authenticated)
                                         → Azure Blob (file uploads, optional)
                                         → Azure Key Vault (secrets, optional)
                                         → Azure OpenAI (AI features, optional)
```

### Backend Patterns

- **CRUD layer**: `app/crud/base.py` has a generic `CRUDBase[Model, CreateSchema, UpdateSchema]` — extend it for all new entities, don't write raw queries.
- **Dependencies**: `app/api/v1/dependencies.py` — use `get_current_user` and `get_current_admin_user` for auth-gated endpoints.
- **Error handling**: Raise `APIException`, `NotFoundError`, `UnauthorizedError`, etc. from `app/core/exceptions.py`; middleware handles the HTTP response.
- **Async everywhere**: All DB calls use `AsyncSession`; never mix sync SQLAlchemy.
- **Response format**: Always return `{ success, data, timestamp }` or use `MessageResponse` from `app/schemas/common.py`.
- All endpoints live under `/api/v1/`.

### Frontend Patterns

- Pages use Astro components (`.astro`); interactive islands use React (`.tsx`).
- API calls go through `src/utils/api.ts` helpers (`get`, `post`, `put`, `del`) — don't use `fetch` directly.
- Content (blog, services) can come from either the backend API or local markdown in `src/content/` (Zod-validated via `content/config.ts`).
- ISR is configured per-page via Vercel adapter.

### Admin Patterns

- All API calls use the Axios instance in `src/lib/api-client.ts` (handles JWT injection and 401 redirect).
- Auth state lives in Zustand (`src/store/auth.store.ts`), persisted to localStorage.
- Service layer (`src/services/*.service.ts`) wraps Axios — call services, not axios directly from components.
- Forms use React Hook Form + Zod; rich text uses TipTap (`src/components/editors/TipTapEditor.tsx`).

---

## Environment Setup

Each app needs its own `.env.local`:

**Frontend** (`techpath-frontend/.env.local`):
```
PUBLIC_API_URL=https://staging.api.techpath.biz
VITE_API_BASE_URL=https://staging.api.techpath.biz
SITE_URL=https://dev.techpath.biz
```

**Backend** (`techpath-backend/.env.local`, see `.env.example`):
```
DATABASE_URL=sqlite+aiosqlite:///./data/techpath.db
SECRET_KEY=<jwt-signing-key>
STORAGE_TYPE=local   # or "azure"
```

**Admin** (`techpath-admin/.env.local`):
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## Deployment

- **Frontend & Admin**: Auto-deploy via Vercel on push to respective branches.
- **Backend**: GitHub Actions (`.github/workflows/deploy-backend.yml`) deploys to VPS via SSH. `develop` → staging, `main` → production.
- Database migrations must be run manually on the VPS after deploying backend changes.
