# Tasks: Audio-Only Presentation Mode

**Input**: Design documents from `/specs/005-audio-only-presentation/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify project structure in `techpath-admin` and `techpath-backend` for classroom components.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

*(No foundational tasks required as `media_state_changed` websocket events and `ClassroomMediaState` models already exist in the backend, and `camera_off` handling exists in the frontend.)*

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Present with Audio Only (Priority: P1) 🎯 MVP

**Goal**: Allow a trainer to present using only their microphone without video or screen sharing.

**Independent Test**: Launch a classroom session from the admin panel, turn off the camera, and confirm the microphone is active and transmitting to students (student sees "Camera Off").

### Implementation for User Story 1

- [x] T002 [P] [US1] Implement `PATCH /api/v1/classroom/{session_id}/media` endpoint in `techpath-backend/app/api/v1/classroom.py` to accept media state updates.
- [x] T003 [US1] Update `techpath-backend/app/services/classroom.py` to broadcast `media_state_changed` event to the session when the media state is updated via the API.
- [x] T004 [P] [US1] Add a "Turn Off Camera" toggle button to the trainer controls in the admin app (e.g., `techpath-admin/src/app/(dashboard)/training/[id]/_components/TrainerControls.tsx`).
- [x] T005 [US1] Implement local media track management in the admin app to mute/disable the video track on the `RTCPeerConnection` when the camera is turned off.
- [x] T006 [US1] Connect the "Turn Off Camera" button to call the new backend API endpoint to update `camera_off=true`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Toggle Video/Screen Share Mid-Session (Priority: P2)

**Goal**: Seamlessly switch between audio-only, video, and screen sharing during a live session.

**Independent Test**: Start session with video, turn off (audio only), then start a screen share, and turn video back on.

### Implementation for User Story 2

- [x] T007 [P] [US2] Enhance the trainer controls in the admin app to handle turning the camera back on (unmuting/enabling the video track).
- [x] T008 [US2] Connect the "Turn On Camera" action to call the backend API endpoint to update `camera_off=false`.
- [x] T009 [US2] Update screen share toggling logic to correctly interact with the `media_state_changed` event and update the backend state appropriately (`screen_sharing=true/false`).

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T010 [P] Add appropriate icons (e.g., Lucide React `CameraOff`) and tooltips to the trainer controls in `techpath-admin`.
- [x] T011 Run `quickstart.md` validation end-to-end.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **User Stories (Phase 3+)**: Can start immediately after Setup.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup.
- **User Story 2 (P2)**: Depends on US1 (requires the base toggle logic).

### Parallel Opportunities

- The backend API endpoint (T002) and frontend button UI (T004) can be developed in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1 (Backend API + Frontend UI)
3. **STOP and VALIDATE**: Test User Story 1 independently using quickstart instructions.
4. Deliver MVP.

### Incremental Delivery

1. Deliver MVP (US1).
2. Complete Phase 4: User Story 2 to allow toggling back and forth.
3. Polish UI.
