# Implementation Plan: Audio-Only Presentation Mode

**Branch**: `[005-audio-only-presentation]` | **Date**: 2026-07-18 | **Spec**: [spec.md](file:///D:/project/techpath/techpath-2026/specs/005-audio-only-presentation/spec.md)

**Input**: Feature specification from `/specs/005-audio-only-presentation/spec.md`

## Summary

The audio-only presentation mode allows trainers to disable their camera and screen sharing while continuing to broadcast audio. The technical approach leverages the existing `media_state_changed` websocket events and `camera_off` state on the student frontend (which already correctly renders a placeholder). Implementation will primarily focus on adding controls to the `techpath-admin` app (trainer view) to toggle their local media tracks and update the backend session state.

## Technical Context

**Language/Version**: TypeScript, Python 3.11+

**Primary Dependencies**: React/Next.js (Admin UI), FastAPI (Backend), WebRTC (WHIP/WHEP)

**Storage**: PostgreSQL (via SQLAlchemy)

**Testing**: Playwright (Frontend), Pytest (Backend)

**Target Platform**: Web Browsers (Chrome, Safari, Firefox, Edge)

**Project Type**: Web Application (Monorepo with Admin, Frontend, Backend)

**Performance Goals**: < 2s for UI state updates across connected peers

**Constraints**: Must maintain stable WebRTC connection when toggling tracks

**Scale/Scope**: Impacts all live classroom sessions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **techpath-frontend**: Minimal changes required as it already conditionally renders video and overlays based on the `media.camera_off` state.
- **techpath-admin**: Will add new UI controls. Must adhere to Next.js App Router and Tailwind CSS principles.
- **techpath-backend**: Will add/update API route to toggle media state and broadcast websocket event. Must adhere to FastAPI layering.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/005-audio-only-presentation/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
└── quickstart.md        # Phase 1 output (/speckit-plan command)
```

### Source Code (repository root)

```text
techpath-admin/
├── src/
│   ├── app/
│   │   └── (dashboard)/
│   │       └── training/
│   └── components/
│       └── classroom/       # Trainer media controls

techpath-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── classroom.py # Endpoint to update media state
│   └── services/
│       └── classroom.py     # Websocket broadcast logic
```

**Structure Decision**: The implementation spans the admin dashboard (trainer UI) and the backend (state sync), while the student frontend remains largely untouched as it already supports the `camera_off` state.
