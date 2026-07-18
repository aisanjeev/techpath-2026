# Implementation Plan: Live Classroom Audio/Video Streaming

**Branch**: `develop` | **Date**: 2026-07-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-live-classroom-streaming/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Add real-time teacher audio/video (camera + screen share) to the live classroom feature that already exists in this repo (`TrainingSession` + join-code-based student join flow, `app/services/classroom/*`, `ClassroomApp.jsx` / `ClassroomPanel.tsx`). The transport is browser-native WebRTC WHIP (publish) / WHEP (playback) against the org's already-running self-hosted MediaMTX server at `live.techpath.biz`, exactly as documented in `CLASSROOM-WEBAPP-GUIDE.md`. No new media server, SFU, or backend media library is introduced — FastAPI's only job is to mint an unguessable, session-scoped stream path (mirroring how it already mints `join_code`) and hand the WHIP URL to the trainer and the WHEP/HLS URL to authenticated participants, then broadcast mute/camera/screen-share state changes over the existing `ClassroomEvent` bus. Recording/VOD reuses the existing external `watch.techpath.biz` transcode service.

## Technical Context

**Language/Version**: Python 3.11 (backend, unchanged); TypeScript/Next.js 14 (admin, unchanged); Astro 5 + React/JavaScript (frontend, unchanged)

**Primary Dependencies**: FastAPI, SQLAlchemy 2.0 async, Alembic (backend — all already in place); browser-native `RTCPeerConnection` / `getUserMedia` / `getDisplayMedia` APIs (no new npm/pip package — WHIP/WHEP need no client SDK, per the guide). No `aiortc`/media-processing library is added to the backend: media never flows through FastAPI.

**Storage**: Existing SQLite/MySQL (auto-detected via `DATABASE_URL`). Extends `training_sessions` with live-media columns and adds one new table, `session_recordings`. Actual video/audio bytes live on the MediaMTX host's disk (`/mnt/nas/media-streams/{stream_path}/...`) and are never stored in this repo's database — only referenced by path/URL.

**Testing**: `pytest` for the new backend endpoints/CRUD (auth scoping, stream-path minting/release, state persistence — everything except the media bytes themselves); Playwright for a two-browser-context (trainer + student) scenario against the classroom pages; a manual quickstart checklist (`quickstart.md`) that exercises every acceptance scenario from `spec.md` end-to-end against a real MediaMTX target, since actual audio/video rendering cannot be asserted by an automated test runner. This combination is what satisfies spec FR-016 / SC-005 ("every step must be tested").

**Target Platform**: Web — existing trainer presenter view (`techpath-admin`, desktop) and student classroom view (`techpath-frontend`, desktop + mobile browsers: Chrome, Edge, Safari, Firefox).

**Project Type**: Web application — extends an existing cross-tier feature (backend + admin + frontend) already scoped to this monorepo's three apps.

**Performance Goals**: Student sees live video/audio within 5s of trainer starting (spec SC-001); trainer's session goes live within 15s of clicking "Start Session" (spec SC-003); WHIP/WHEP transport itself runs at MediaMTX's native ~200ms glass-to-glass latency (per the guide), well inside the SC-001 budget once signaling overhead is added.

**Constraints**: MediaMTX itself runs with `authMethod: internal` (no server-side auth) — all access control must happen at the TechPath backend layer, by never handing out a stream path except through an already-authorized request (trainer via `get_current_trainer_user`, student via the existing `get_current_participant` classroom-token dependency). Media does not proxy through FastAPI (direct browser↔MediaMTX WHIP/WHEP), so the multi-worker "no sticky sessions" constraint that `app/services/classroom/bus.py` solves for chat/poll events does not apply to the media path itself — it only applies to broadcasting mute/camera/screen-share *state changes*, which reuses that existing bus.

**Scale/Scope**: Up to ~100 concurrent student viewers per session (spec assumption); one trainer publishing per session; fan-out is MediaMTX's job, not FastAPI's.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **III. Backend API** — New logic lives in `app/services/classroom/media.py` (stream-path minting, MediaMTX/watch-service URL construction), following the existing `app/services/classroom/{bus,identity,roster}.py` pattern. Endpoints stay thin in `trainer.py` / `classroom.py`; DB access goes through `CRUDBase`-extending classes in `app/crud/`. Async/SQLAlchemy 2.0 style preserved. **PASS**.
- **I. Public Frontend** — `ClassroomApp.jsx` is already a fully client-side island (`client:load`, no SSR content), so adding a live `<video>` element and WebRTC logic to it does not introduce new zero-JS violations beyond what's already accepted for this one interactive page. **PASS** (no new deviation).
- **II. Admin Dashboard** — Trainer video controls extend the existing `ClassroomPanel.tsx` / presenter page, reusing the Axios service pattern (`trainer.service.ts`) and no new global state library. **PASS**.
- **Governance** — No new architectural tier, no bypass of the CRUD/service/endpoint layering. No complexity justification needed.

## Project Structure

### Documentation (this feature)

```text
specs/004-live-classroom-streaming/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Web application: this monorepo's existing three-tier layout — extending, not adding, apps

techpath-backend/
├── app/
│   ├── models/
│   │   ├── training_roster.py       # TrainingSession: + live-media columns (Phase 1)
│   │   └── classroom.py             # + SessionRecording model (Phase 1)
│   ├── crud/
│   │   ├── training_roster.py       # + stream-path mint/release on CRUDTrainingSession
│   │   └── classroom.py             # + session_recording_crud
│   ├── services/
│   │   └── classroom/
│   │       ├── bus.py                # unchanged — reused for media_state_changed events
│   │       ├── identity.py           # unchanged — reused token scoping
│   │       └── media.py              # NEW — stream-path minting, MediaMTX/watch URL builders
│   ├── api/v1/endpoints/
│   │   ├── trainer.py                # + publish URL, media state, recording endpoints
│   │   └── classroom.py              # + media block on join/state responses
│   ├── schemas/classroom.py          # + MediaView, MediaStateRequest, RecordingView
│   ├── core/config.py                # + LIVE_MEDIA_BASE_URL, WATCH_SERVICE_BASE_URL settings
│   └── db/migrations/versions/       # + new revision, down_revision = s1t2u3d4e5n6
└── tests/
    ├── unit/                         # media.py URL/path builders
    └── integration/                  # trainer + classroom endpoint auth/state tests

techpath-admin/
└── src/
    ├── components/training/
    │   ├── ClassroomPanel.tsx        # + mic/camera/screen-share controls
    │   └── PresenterVideoTile.tsx    # NEW — trainer local preview + WHIP publish
    ├── services/trainer.service.ts   # + media endpoints
    └── app/(trainer)/trainer/sessions/[id]/present/page.tsx  # wires PresenterVideoTile in

techpath-frontend/
└── src/
    ├── components/react-components/
    │   ├── ClassroomApp.jsx          # + video tile in LiveScreen, WHEP viewer lifecycle
    │   └── ClassroomVideoTile.jsx    # NEW — WHEP/HLS viewer + fallback logic
    └── services/classroomService.ts  # + media field on join/state responses
```

**Structure Decision**: No new applications or top-level directories. This feature extends the existing `TrainingSession`-centered live classroom vertical slice across all three apps, following the file layout the classroom/trainer feature already established (`app/services/classroom/*`, `ClassroomPanel.tsx`, `ClassroomApp.jsx`).

## Complexity Tracking

*No Constitution Check violations — this section is intentionally empty.*
