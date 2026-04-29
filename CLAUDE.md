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
Public users → Astro frontend (SSR/SSG) → FastAPI backend → SQLite/MySQL
Admin users  → Next.js admin             → FastAPI backend (Firebase-authenticated)
                                         → Azure Blob (file uploads, optional)
                                         → Azure Key Vault (secrets, optional)
                                         → Azure OpenAI (AI features, optional)
```

### Authentication Flow

Auth is Firebase-based across all apps:

1. Users sign in via Firebase client SDK (admin app handles this)
2. Firebase ID token is sent as `Authorization: Bearer <token>` to the backend
3. Backend verifies the token via Firebase Admin SDK (`app/core/firebase_admin.py`)
4. On first login, the backend auto-provisions the user in DB via `get_or_create_from_firebase()`
5. A short-lived JWT (60 min, configurable) is returned for session use

In the admin Axios client (`src/lib/api-client.ts`), a request interceptor fetches a fresh Firebase ID token before every request — no token refresh logic needed client-side.

### Backend Patterns

- **CRUD layer**: `app/crud/base.py` has a generic `CRUDBase[Model, CreateSchema, UpdateSchema]` — extend it for all new entities, don't write raw queries.
- **SQLAlchemy 2.0 queries**: Use `select(Model)` + `await db.execute()`, never `db.session.query()`. Use `await db.flush()` to refresh ORM state within a transaction; commits happen automatically when the `get_db()` dependency exits cleanly.
- **Pydantic v2**: Use `model_dump(exclude_unset=True)` for partial updates; use `ConfigDict(from_attributes=True)` on response schemas that map from ORM models.
- **Dependencies**: `app/api/v1/dependencies.py` — use `get_current_user` (auth required), `get_current_admin_user` (role == "admin"), or `get_optional_user` (auth optional, returns `User | None`).
- **Services layer**: Business logic lives in `app/services/` (AI, storage, email, secrets) — keep it out of CRUD and endpoint handlers.
- **Error handling**: Raise `APIException` subclasses from `app/core/exceptions.py` (`NotFoundError`, `UnauthorizedError`, `ForbiddenError`, `ConflictError`, etc.); error-handler middleware converts them to a consistent JSON shape.
- **Response format**: Always return `{ success, data, timestamp }` or use `MessageResponse` from `app/schemas/common.py`. Lists use `PaginatedResponse` and expose an `X-Total-Count` header; pagination uses `skip` / `limit` query params.
- **Async everywhere**: All DB calls use `AsyncSession`; never mix sync SQLAlchemy.
- **All endpoints** live under `/api/v1/`.
- **Models**: All models include `created_at` / `updated_at` (UTC) via `TimestampMixin`.
- **Multi-DB**: Config auto-detects SQLite vs MySQL from `DATABASE_URL` and adjusts pool/echo settings — `config.is_sqlite` and `config.is_mysql` properties gate DB-specific logic.
- **Static uploads**: In local storage mode, uploaded files are served from `/uploads` (mounted as a static route in the FastAPI lifespan).

### Frontend Patterns

- Pages use Astro components (`.astro`); interactive islands use React (`.tsx`) with `client:load` / `client:idle` directives — default to zero JS.
- Output mode is `server` (Node.js adapter), not static. ISR is configured per-page via the Vercel adapter.
- API calls go through `src/utils/api.ts` helpers (`get`, `post`, `put`, `del`) — don't use `fetch` directly.
- Content (blog, services) comes from local markdown in `src/content/` (Zod-validated at build time via `src/content/config.ts`) or from the backend API. Use Astro's `getCollection()` for build-time content.
- `src/middleware.ts` injects `X-Robots-Tag: noindex, nofollow` on every response unless `PUBLIC_SITE_ENV=production` — prevents staging from being indexed.

### Admin Patterns

- All API calls use the Axios instance in `src/lib/api-client.ts` (injects fresh Firebase ID token, handles 401 → logout redirect).
- Auth state lives in Zustand (`src/store/auth.store.ts`), persisted to localStorage.
- Service layer (`src/services/*.service.ts`) wraps Axios — call services, not axios directly from components.
- Route groups: `(auth)` for login/unauthenticated pages; `(dashboard)` for protected routes with sidebar/topnav layout.
- Forms use React Hook Form + Zod; rich text uses TipTap (`src/components/editors/TipTapEditor.tsx`).
- UI state (sidebar collapse, etc.) is in `src/store/ui.store.ts`.

---

## Environment Setup

Each app needs its own `.env.local`:

**Frontend** (`techpath-frontend/.env.local`):
```
PUBLIC_API_URL=https://staging.api.techpath.biz
VITE_API_BASE_URL=https://staging.api.techpath.biz
SITE_URL=https://dev.techpath.biz
PUBLIC_SITE_ENV=development   # set to "production" to enable robots indexing
```

**Backend** (`techpath-backend/.env.local`, see `.env.example`):
```
DATABASE_URL=sqlite+aiosqlite:///./data/techpath.db
SECRET_KEY=<jwt-signing-key>
STORAGE_TYPE=local                     # or "azure"
FIREBASE_PROJECT_ID=<project-id>
FIREBASE_SERVICE_ACCOUNT_PATH=<path-to-json>   # or FIREBASE_SERVICE_ACCOUNT_B64 in CI
```

**Admin** (`techpath-admin/.env.local`):
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## Deployment

- **Frontend & Admin**: Auto-deploy via Vercel on push to respective branches.
- **Backend**: GitHub Actions (`.github/workflows/deploy-backend.yml`) deploys to VPS via SSH. `develop` → staging (port 8093); `main` → production (port 8092, requires manual approval gate).
- Database migrations must be run manually on the VPS after deploying backend changes (`poetry run alembic upgrade heads` — note plural `heads` to handle multiple migration branches).
