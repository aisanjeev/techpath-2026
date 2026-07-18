# Implementation Plan: Trainer Material Visibility

**Branch**: `[008-trainer-material-visibility]` | **Date**: 2026-07-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/008-trainer-material-visibility/spec.md`

## Summary

When a training module has been presented multiple times, the trainer viewing the presentation logs (sessions) should be able to see the associated published materials (module assets) directly within the report via a new button or link.

## Technical Context

**Language/Version**: Python 3.11, TypeScript (Next.js/React)

**Primary Dependencies**: FastAPI, SQLAlchemy, Next.js, Tailwind CSS, Zustand

**Storage**: PostgreSQL / SQLite (existing `training_sessions` and `training_modules` tables)

**Testing**: pytest (backend)

**Target Platform**: Web (Admin Dashboard for Trainers)

**Project Type**: web-service + web-app

**Performance Goals**: N/A

**Constraints**: N/A

**Scale/Scope**: Minor UI addition in the admin dashboard (trainer logs view) and exposing related assets in the backend API.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No violations. The feature involves adding a button to the frontend (`techpath-admin`) that fetches and displays the existing module assets provided by the backend (`techpath-backend`). All existing architectural layers (Endpoints, Services, CRUD) and state management patterns (Zustand) will be respected.

## Project Structure

### Documentation (this feature)

```text
specs/008-trainer-material-visibility/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
techpath-backend/
├── app/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

techpath-admin/
├── src/
│   ├── components/
│   ├── app/(dashboard)/
│   └── lib/
└── tests/
```

**Structure Decision**: Option 2 (Web application - backend + frontend). This touches both the `techpath-admin` dashboard (for the trainer view) and the `techpath-backend` API (to fetch the published materials for the session's module).
