# Tasks: Toggle Recording

**Input**: Design documents from `/specs/006-toggle-recording/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify project structure in `techpath-admin` and `techpath-backend` for classroom and storage components.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T002 [P] Generate Alembic database migration to add `keep_recording` boolean column (default false) to the training session table.
- [x] T003 [P] Add `keep_recording` column to the corresponding SQLAlchemy model in `techpath-backend/app/models/`.
- [x] T004 Implement `delete_recording` method in `techpath-backend/app/services/storage_service.py` to securely delete `.mp4` objects from the MinIO bucket using the SDK.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Save Class Recording (Priority: P1) 🎯 MVP

**Goal**: Allow a trainer to explicitly request the recording to be kept.

**Independent Test**: Start session, click "Record", end session. Verify transcode is triggered and the video file remains in the bucket.

### Implementation for User Story 1

- [x] T005 [P] [US1] Update `TrainingSessionResponse` and relevant API schemas in `techpath-backend/app/schemas/` to include the `keep_recording` field.
- [x] T006 [P] [US1] Create or update the API endpoint (e.g., `PATCH /sessions/{session_id}/recording`) in `techpath-backend/app/api/v1/endpoints/trainer.py` to allow the trainer to toggle `keep_recording`.
- [x] T007 [P] [US1] Add a "Record" toggle button to the trainer controls in `techpath-admin/src/components/training/PresenterVideoTile.tsx`.
- [x] T008 [US1] Hook up the "Record" toggle to call the backend API and update the local UI state.

**Checkpoint**: At this point, User Story 1 should be fully functional (trainer can toggle the flag and it saves to DB).

---

## Phase 4: User Story 2 - Discard Unwanted Recording (Priority: P1)

**Goal**: Delete the unwanted recording file from MinIO when the session ends.

**Independent Test**: Start session, do NOT click "Record", end session. Verify the video file is deleted from the bucket.

### Implementation for User Story 2

- [x] T009 [P] [US2] Update `end_session` logic in `techpath-backend/app/api/v1/endpoints/trainer.py`.
- [x] T010 [US2] Inside `end_session`, if `keep_recording` is false, call `storage_service.delete_recording(...)` with the session's stream path to discard the media server's background recording.
- [x] T011 [US2] Inside `end_session`, ensure the transcode trigger (and `session_recording_crud.create`) is ONLY called if `keep_recording` is true.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T012 [P] Update `techpath-admin` UI to show a pulsing red dot or active state when `keep_recording` is enabled.
- [x] T013 Run `quickstart.md` validation end-to-end to ensure the deletion logic behaves perfectly.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P1)**: Depends on US1 (relies on the `keep_recording` flag being toggleable, though the default false state can be tested without the UI).

### Parallel Opportunities

- The database migration (T002, T003) and storage service utility (T004) can be built in parallel.
- Frontend UI button (T007) and Backend API endpoint (T006) can be built in parallel.

---

## Implementation Strategy

### Incremental Delivery

1. Complete Setup + Foundational → Database is ready.
2. Complete User Story 1 → Trainer can toggle state.
3. Complete User Story 2 → Backend honors state and deletes files.
4. Polish UI and validate.
