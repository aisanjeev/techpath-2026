<!--
Sync Impact Report:
- Version change: none → 1.0.0
- List of modified principles:
  - [PRINCIPLE_1_NAME] → Public Frontend (techpath-frontend)
  - [PRINCIPLE_2_NAME] → Admin Dashboard (techpath-admin)
  - [PRINCIPLE_3_NAME] → Backend API (techpath-backend)
  - [PRINCIPLE_4_NAME] → Removed (Merged into tiers)
  - [PRINCIPLE_5_NAME] → Removed (Merged into tiers)
- Added sections: None
- Removed sections: None
- Templates requiring updates: 
  - .specify/templates/plan-template.md (✅ checked, no hardcoded principles found)
  - .specify/templates/spec-template.md (✅ checked, no hardcoded principles found)
  - .specify/templates/tasks-template.md (✅ checked, no hardcoded principles found)
- Follow-up TODOs: None
-->
# TechPath Architecture Constitution

## Core Principles

### I. Public Frontend (techpath-frontend)
**Goal:** Maximize SEO, performance (Core Web Vitals), and lead conversion for the public-facing website.
- **Tech Stack:** Astro 5, React (for islands), Tailwind CSS, TypeScript.
- **Performance First (Zero-JS):** Astro's "Zero JS by default". Pages are rendered as static HTML on the server. JavaScript is only sent to the browser for specific, isolated interactive components (React) using directives like `client:load` or `client:idle`.
- **Rendering Strategy:** Server-Side Rendering (SSR) via a Node.js adapter (Output mode: hybrid or server). High-priority pages are prerendered at build time for speed, dynamic routes rendered on-demand.
- **Content Collections:** Content (blog, services) stored locally as Markdown in `src/content/`, strictly validated at build time using Astro Content Collections and Zod schemas to guarantee data integrity.
- **Centralized API Client:** Direct `fetch()` calls are prohibited. All external data fetching routes through customized helper functions in `src/utils/api.ts`.
- **Styling:** Tailwind CSS with a strict mobile-first approach. Custom styling limited to CSS modules for component-scoped styles when necessary.

### II. Admin Dashboard (techpath-admin)
**Goal:** Provide a rich, highly interactive CMS and dashboard experience for internal staff and administrators.
- **Tech Stack:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Zustand, React Hook Form.
- **Authentication & Token Management:** Auth handled client-side via Firebase SDK. An Axios request interceptor (`src/lib/api-client.ts`) automatically fetches a fresh Firebase ID token before every API request and attaches it as a Bearer token, replacing complex refresh logic.
- **State Management:** Global UI and Authentication state managed by Zustand stores (`src/store/auth.store.ts`, `src/store/ui.store.ts`), persisted to local storage. No complex React Contexts for global state.
- **Strict Routing Groups:** App Router strictly organized into logical groups: `(auth)` for login/unauthenticated views, and `(dashboard)` for protected routes sharing the standard dashboard layout (sidebar, top nav).
- **Forms & Validation:** All forms utilize React Hook Form coupled with Zod for strict client-side validation. Rich text editing is standardized on the TipTap editor.

### III. Backend API (techpath-backend)
**Goal:** Provide a robust, secure, and highly scalable REST API to serve both frontends, isolating all complex business and database logic.
- **Tech Stack:** FastAPI, Python, Async SQLAlchemy 2.0, Pydantic v2.
- **Strict Architectural Layering:** 
  - **Endpoints** (`app/api/`): Strictly for HTTP routing, parameter validation, and returning standardized responses. Avoids "fat controllers".
  - **Services** (`app/services/`): Contains all business logic (e.g., orchestrating LLMs, payments, emails).
  - **CRUD** (`app/crud/`): Contains all database queries, extending a generic `CRUDBase` class to prevent rewriting standard SQL operations.
- **Async Everywhere:** Fully asynchronous (`async def`). Uses `AsyncSession` for database interactions and `asyncio.gather()` for parallel operations to ensure the event loop is never blocked.
- **Database Interactions:** Exclusively uses modern SQLAlchemy 2.0 syntax (e.g., `select(Model) + await db.execute()`). Schema changes strictly version-controlled via Alembic migrations.
- **Consistent API Responses & Errors:** Endpoints always return a standardized JSON structure: `{ success, data, timestamp, message }`. Business logic raises custom exceptions caught by global middleware and safely translated into the standardized JSON error format.
- **Auth Provisioning:** Firebase tokens validated via Firebase Admin SDK. Non-existent users are auto-provisioned before issuing a short-lived JWT session token.

## Application Architecture

The TechPath monorepo is strictly divided into three isolated applications that communicate via well-defined REST API contracts. The backend serves as the single source of truth for business logic and data persistence, while the frontends remain lightweight presentation layers optimized for their specific audiences (public vs. internal admin).

## Development Workflow

Development across all tiers must adhere to their specific architectural boundaries. Cross-tier features must define the API contract first, implement the backend logic via services and CRUD, and then consume the standardized endpoints in the frontends.

## Governance

Constitution supersedes all other practices; Amendments require documentation, approval, and migration plan. All PRs/reviews must verify compliance. Complexity must be justified. Use `CLAUDE.md` and `Astro-FastAPI-Guidelines.md` for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2026-07-17 | **Last Amended**: 2026-07-17
