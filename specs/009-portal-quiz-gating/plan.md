# Implementation Plan: Graded Quiz Attempts and Progress Gating

**Branch**: `009-portal-quiz-gating` | **Date**: 2026-07-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/009-portal-quiz-gating/spec.md`

## Summary

Make quiz lecture assets answerable and gradeable. Three changes, in dependency order:

1. **Stop shipping the answer key to students.** `asset_to_response()` in `app/crud/training.py` currently returns the asset's `config` blob verbatim, so `correct_index` and `explanation` reach students through the portal materials endpoint and the live-classroom asset fetch. Add an audience-aware redaction step at that single serialization point.
2. **Grade on the server.** A new `session_quiz_attempts` table records each submission; a new student-portal endpoint grades against the stored key and returns per-question feedback. The client never sees the key until it has submitted.
3. **Gate on the result.** The portal's existing sequential asset pager consults a progress endpoint and refuses to advance past a quiz without a passing attempt.

Feature 007's live poll flow is untouched. That path already lets a trainer push one quiz question to the room as a real-time poll, and it stays the live mechanism.

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript 5 (admin), JavaScript/JSX (frontend islands)

**Primary Dependencies**: FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Alembic; Astro 5 + React (frontend); Next.js 14 (admin)

**Storage**: SQLite in dev, MySQL in staging/production — `config.is_sqlite` / `config.is_mysql` gate dialect-specific logic. Note: the 007 plan says PostgreSQL; that is wrong and was not corrected there. No Postgres-only constructs may be used here.

**Testing**: pytest with `pytest-asyncio` (backend); Playwright e2e (frontend)

**Target Platform**: Web — student portal (Astro/React island) and trainer dashboard (Next.js)

**Project Type**: Monorepo — FastAPI backend + Next.js admin + Astro frontend

**Performance Goals**: Grading is a single-row insert plus an in-memory comparison against an already-loaded config blob — sub-50ms server-side. The progress lookup for a session's material must be one query, not one per asset.

**Constraints**: Grading must be server-side only; no correct-answer data may reach a student's browser pre-submission. Migration must run on both SQLite and MySQL. Gating must not regress navigation for the large majority of material that contains no quiz.

**Scale/Scope**: Dozens of students per batch, a handful of quizzes per module, a few questions per quiz. Attempt volume is small; no partitioning or archival concerns.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against `.specify/memory/constitution.md`:

| Principle | Gate | Status |
|---|---|---|
| III — Strict layering | Grading logic in `services/`, queries in `crud/`, endpoints thin | **Pass** — grading goes in `app/services/quiz_grading.py`, persistence extends `CRUDBase`, the endpoint only routes and returns |
| III — Async everywhere | All DB access via `AsyncSession` | **Pass** |
| III — SQLAlchemy 2.0 | `select(Model)` + `await db.execute()`, Alembic-versioned schema | **Pass** — new migration on head `b1r2o3a4d5c6` |
| III — Consistent responses | `{success, data, timestamp}` envelope, `APIException` subclasses | **Pass** — `ValidationError` for malformed submissions, `NotFoundError` for unreachable assets, `ForbiddenError` for cross-batch trainer access |
| III — Auth provisioning | Student identity via existing `get_current_student` | **Pass** — no new auth surface |
| I — Zero-JS default | Quiz interactivity is an existing React island, not a new page-wide script | **Pass** — extends `ClassroomAssetView.jsx`, already `client:`-loaded |
| I — Centralized API client | No direct `fetch()` | **Pass** — extends `src/services/studentPortalService.ts` |
| II — Admin patterns | Trainer results via Axios service layer, not direct axios in components | **Pass** — extends `trainer.service.ts`, follows `trainer_reports.py` on the server |

No violations. Complexity Tracking section omitted.

**Post-design re-check (after Phase 1)**: Re-evaluated against the generated data model and contracts. Still passing, with two points worth recording:

- The one new table and one new service module are the minimum the requirements support — no repository layer, no progress table (progress is derived), no asset-versioning system. Each was considered and rejected in [research.md](./research.md).
- The design adds a `ValidationError` path for malformed submissions and a `NotFoundError` path for unreachable sessions, both using existing `app/core/exceptions.py` subclasses handled by the existing middleware. No new error-handling machinery.

One honest caveat, recorded rather than glossed: gating is a **navigation guard, not an access boundary**. Locked assets' payloads are still present in the materials response, so a determined student could reach them by hand. That is acceptable here — the material is already published to a student who attended the session, and the answer key (the thing that genuinely must not leak) is protected server-side independently. If gating ever needs to be a true boundary, the materials endpoint must stop returning locked assets, which is a larger change. See D4.

## Project Structure

### Documentation (this feature)

```text
specs/009-portal-quiz-gating/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── student-quiz.md
│   └── trainer-quiz-results.md
├── checklists/
│   └── requirements.md  # From /speckit-specify
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root)

```text
techpath-backend/
├── app/
│   ├── api/v1/endpoints/
│   │   ├── student_portal.py        # + submit attempt, + progress
│   │   └── trainer_reports.py       # + quiz results for a session
│   ├── models/
│   │   └── training_roster.py       # + SessionQuizAttempt
│   ├── schemas/
│   │   ├── student_portal.py        # + submission/result/progress schemas
│   │   ├── trainer_reports.py       # + quiz results schemas
│   │   └── training.py              # quiz question shape (reference)
│   ├── crud/
│   │   ├── training.py              # asset_to_response gains audience redaction
│   │   └── quiz_attempts.py         # NEW — CRUDBase subclass
│   ├── services/
│   │   └── quiz_grading.py          # NEW — grading + pass/fail + gating decisions
│   ├── core/
│   │   └── config.py                # + QUIZ_PASS_MARK
│   └── db/migrations/versions/
│       └── 20260718_quiz_attempts.py  # NEW — down_revision b1r2o3a4d5c6
└── tests/
    ├── test_quiz_grading.py         # NEW — unit, grading + boundary
    └── test_student_quiz_flow.py    # NEW — integration, redaction + gating

techpath-frontend/
├── src/
│   ├── components/react-components/
│   │   ├── ClassroomAssetView.jsx   # QuizView becomes interactive
│   │   └── StudentPortalApp.jsx     # pager consults gating
│   ├── services/studentPortalService.ts  # + submit/progress calls
│   └── types/studentPortal.ts       # + attempt/progress types

techpath-admin/
├── src/
│   ├── services/trainer.service.ts  # + quiz results call
│   ├── types/classroom.ts           # + quiz results types
│   └── components/training/         # results panel on the session report
```

**Structure Decision**: The feature spans all three tiers and follows the monorepo split already established by 007 — backend owns grading and gating decisions, both frontends are presentation only. The one deliberate addition is `app/services/quiz_grading.py`: the constitution forbids fat controllers, and grading plus the "is this asset unlocked" decision is genuine business logic that both the student-portal endpoint and the trainer-report endpoint need.

## Key Design Decisions

Full rationale in [research.md](./research.md). The load-bearing ones:

- **Redact at `asset_to_response`, not per-endpoint.** That function is documented as the single place deciding what an asset looks like off the wire, precisely so its three callers can't drift. Adding an `audience` parameter keeps that property; redacting in each student-facing endpoint would break it and is how the leak arose in the first place.
- **Attempts are immutable; progress is derived.** A retry inserts a new row rather than updating one. No separate progress table — "unlocked" is computed from the existence of a passing attempt. This makes the audit trail free and keeps the migration to one table.
- **Store the question count the attempt was graded against.** Answers the spec's "trainer edits the quiz after attempts exist" edge case without a full asset-version system: a stored `question_count` that no longer matches the live asset marks the attempt as stale in the trainer's view.
- **Gate forward-only, computed server-side.** The server returns the index of the first unpassed quiz; the client blocks advancement beyond it. Backward navigation is always free.

## Complexity Tracking

No constitution violations. Section intentionally empty.
