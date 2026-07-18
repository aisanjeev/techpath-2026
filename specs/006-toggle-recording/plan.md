# Implementation Plan: Toggle Recording

**Branch**: `[006-toggle-recording]` | **Date**: 2026-07-18 | **Spec**: [spec.md](file:///D:/project/techpath/techpath-2026/specs/006-toggle-recording/spec.md)

**Input**: Feature specification from `/specs/006-toggle-recording/spec.md`

## Summary

This feature allows trainers to toggle recording for their live sessions. Using the "Auto-Delete Strategy", the media server continuously records to a MinIO bucket by default. If the trainer leaves recording off (the default) or disables it, the backend automatically deletes the background media file from the storage bucket when the session ends.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript

**Primary Dependencies**: FastAPI, React/Next.js (Admin UI), MinIO SDK (`aioboto3` or `minio` in python backend)

**Storage**: PostgreSQL (via SQLAlchemy), MinIO

**Testing**: Pytest (Backend), Playwright (Frontend)

**Target Platform**: Web Browsers, Backend API

**Project Type**: Web Application (Monorepo)

**Performance Goals**: Deleting the file should not significantly delay the "End Session" response.

**Constraints**: Must securely delete the correct file from the MinIO bucket.

**Scale/Scope**: Impacts all live classroom sessions.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **techpath-backend**: Will add new boolean column to the database model. Migrations required.
- **techpath-admin**: Will add new UI controls.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/006-toggle-recording/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
└── quickstart.md        # Phase 1 output (/speckit-plan command)
```

### Source Code (repository root)

```text
techpath-backend/
├── app/
│   ├── models/
│   │   └── classroom.py     # Add keep_recording column
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── trainer.py   # Update media state and end_session logic
│   └── services/
│       └── storage_service.py   # Add delete_recording method

techpath-admin/
├── src/
│   ├── components/
│   │   └── training/
│   │       └── PresenterVideoTile.tsx # Add Record toggle button
```

**Structure Decision**: The implementation spans the backend database, the `trainer.py` router logic, MinIO storage interactions, and the admin dashboard UI.
