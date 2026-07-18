# Implementation Plan: Student Speaker Control

**Branch**: `[010-student-speaker-control]` | **Date**: 2026-07-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/010-student-speaker-control/spec.md`

## Summary

Implement a two-way audio "push-to-talk" feature allowing students to raise their hands, wait for the trainer's approval, and then broadcast their microphone directly to the trainer using WebRTC (MediaMTX) unique paths, ensuring a stable and uninterrupted main class stream.

## Technical Context

**Language/Version**: TypeScript (React, Next.js, Astro), Python 3.11

**Primary Dependencies**: WebRTC API, MediaMTX (WHEP/WHIP), FastAPI (REST + WebSockets for event delivery)

**Storage**: PostgreSQL (for session state / doubt requests)

**Testing**: Pytest (backend), Jest/React Testing Library (frontend)

**Target Platform**: Web Browsers (Chrome, Firefox, Safari)

**Project Type**: Monorepo with Web Services and Frontend Apps

**Performance Goals**: Audio latency < 500ms, event delivery latency < 1s

**Constraints**: Audio must only go to the trainer, avoiding echo or interruption of main class

**Scale/Scope**: ~10k concurrent users, low bandwidth overhead

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Public Frontend (techpath-frontend)**: Changes isolated to interactive components, maintaining Zero-JS defaults elsewhere.
- **Admin Dashboard (techpath-admin)**: Uses existing Zustand stores and Firebase auth.
- **Backend API (techpath-backend)**: Uses standard REST endpoints for state changes (raise hand, approve), avoiding "fat controllers". Websocket is strictly receive-only for clients, relying on `bus.py`.

## Project Structure

### Documentation (this feature)

```text
specs/010-student-speaker-control/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
techpath-backend/
├── app/
│   ├── api/v1/endpoints/classroom.py  # New REST endpoints for raising hand / approving
│   ├── models/classroom.py            # Updates to track doubt requests
│   └── services/classroom/            # Logic for publishing doubt events

techpath-frontend/
├── src/
│   └── components/Classroom/          # "Raise Hand" button, WebRTC push logic

techpath-admin/
├── src/
│   └── components/Classroom/          # Doubt queue UI, "Enable Audio" button, WebRTC pull logic
```

**Structure Decision**: Utilizing the existing monorepo architecture, spreading the implementation across the 3 main tiers (Admin, Frontend, Backend) interacting via REST APIs and WebSockets.
