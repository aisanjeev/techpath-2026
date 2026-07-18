# Tasks: Student Speaker Control

**Input**: Design documents from `/specs/010-student-speaker-control/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify MediaMTX local configuration supports WHEP and WHIP unique paths in `docker-compose.yml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Create DoubtRequest model entity in `techpath-backend/app/models/classroom.py`
- [x] T003 Generate Alembic migration for DoubtRequest table in `techpath-backend/alembic/versions/`
- [x] T004 Add DOUBT_REQUESTED, DOUBT_APPROVED, DOUBT_REJECTED, DOUBT_COMPLETED events to `techpath-backend/app/models/classroom.py`
- [x] T005 Implement DoubtRequest CRUD operations in `techpath-backend/app/crud/classroom.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Raise Hand and Teacher Approval (Priority: P1) 🎯 MVP

**Goal**: A student can indicate they want to speak by raising their hand, and the trainer can approve it to allow the student's microphone to be broadcast to the trainer via WebRTC.

**Independent Test**: Student clicks raise hand, trainer sees notification, clicks approve, student's audio is captured and heard by trainer.

### Implementation for User Story 1

- [x] T006 [P] [US1] Create REST endpoint for 'Raise Hand' (POST /doubts) in `techpath-backend/app/api/v1/endpoints/classroom.py`
- [x] T007 [P] [US1] Create REST endpoint for 'Approve' (POST /doubts/{id}/approve) in `techpath-backend/app/api/v1/endpoints/classroom.py`
- [x] T008 [P] [US1] Create REST endpoint for 'Stop Audio' (POST /doubts/{id}/stop) in `techpath-backend/app/api/v1/endpoints/classroom.py`
- [x] T009 [P] [US1] Create WebRTC push helper function (WHIP) in `techpath-frontend/src/utils/webrtc.ts`
- [x] T010 [US1] Implement 'Raise Hand' button and microphone capture in `techpath-frontend/src/components/Classroom/StudentControls.tsx`
- [x] T011 [US1] Wire student WebSocket event listener to trigger WebRTC publish in `techpath-frontend/src/components/Classroom/ClassroomView.tsx`
- [x] T012 [P] [US1] Create WebRTC pull helper function (WHEP) in `techpath-admin/src/utils/webrtc.ts`
- [x] T013 [US1] Add 'Enable Audio' button to trainer UI in `techpath-admin/src/components/Classroom/TrainerControls.tsx`
- [x] T014 [US1] Wire trainer WebSocket event listener to trigger WebRTC subscribe in `techpath-admin/src/components/Classroom/ClassroomDashboard.tsx`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Managing Multiple Doubts (Priority: P2)

**Goal**: The trainer needs a clear and stable UI to manage multiple students who might want to speak at the same time or sequentially.

**Independent Test**: Multiple mock students raise hands, and the trainer manages the queue of speakers on the dashboard.

### Implementation for User Story 2

- [x] T015 [P] [US2] Update Zustand store to track pending doubts list in `techpath-admin/src/store/classroom.store.ts`
- [x] T016 [US2] Create 'Doubt Queue' UI component for trainer in `techpath-admin/src/components/Classroom/DoubtQueue.tsx`
- [x] T017 [US2] Implement active speaker tracking to mute/replace older audio in `techpath-admin/src/components/Classroom/AudioMixer.tsx`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T018 [P] Add visual feedback for 'Mic Live' state in `techpath-frontend/src/components/Classroom/MicrophoneStatus.tsx`
- [x] T019 [P] Handle browser permission denial edge cases in frontend and admin
- [x] T020 Run quickstart.md validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Depends on UI elements introduced in US1, should be implemented after US1.

### Parallel Opportunities

- All REST endpoints in Phase 3 can be built in parallel.
- Frontend and Admin WebRTC helpers can be built in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch REST Endpoints together:
Task: T006 Create REST endpoint for 'Raise Hand'
Task: T007 Create REST endpoint for 'Approve'
Task: T008 Create REST endpoint for 'Stop Audio'

# Build UI helpers together:
Task: T009 Create WebRTC push helper function (WHIP)
Task: T012 Create WebRTC pull helper function (WHEP)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo MVP
