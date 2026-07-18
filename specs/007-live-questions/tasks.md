# Tasks: Live Questions

**Input**: Design documents from `/specs/007-live-questions/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify project structure per implementation plan (Monorepo with FastAPI, Next.js, Astro)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Update `TrainingSession` model with `questions_are_public` flag in `techpath-backend/app/models/training_roster.py` (or session model location)
- [x] T003 [P] Create `TrainingSessionQuestion` model in `techpath-backend/app/models/training_roster.py` (or new model file)
- [x] T004 Generate Alembic migration for the new tables and columns in `techpath-backend`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask a Live Question (Priority: P1) 🎯 MVP

**Goal**: Student sees a "?" button, types their doubt, and submits. It shows up for the trainer.

**Independent Test**: Can be fully tested by a student joining a live session, clicking the question button, typing text, and submitting.

### Implementation for User Story 1

- [x] T005 [P] [US1] Create Pydantic schemas for Question creation and responses in `techpath-backend/app/schemas/training_roster.py` (or new schema file)
- [x] T006 [US1] Implement CRUD operations for Questions in `techpath-backend/app/crud/crud_question.py`
- [x] T007 [P] [US1] Update `ClassroomBroadcaster` in `techpath-backend/app/services/classroom/bus.py` to broadcast `question_asked` and `question_upvoted` events
- [x] T008 [US1] Implement POST endpoint `/api/v1/student/sessions/{session_id}/questions` in `techpath-backend/app/api/v1/endpoints/student.py`
- [x] T009 [US1] Implement POST endpoint `/api/v1/student/sessions/{session_id}/questions/{question_id}/upvote` in `techpath-backend/app/api/v1/endpoints/student.py`
- [x] T010 [US1] Build "Ask Question" (❓) React component UI in `techpath-frontend/src/components/`
- [x] T011 [US1] Integrate "Ask Question" UI with WebSockets to receive new questions and display them, and connect API submission in `techpath-frontend`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Trainer Views and Manages Questions (Priority: P1)

**Goal**: Trainer sees incoming questions in their dashboard, can mark them as "Answered", and toggle public visibility.

**Independent Test**: Can be tested by having a trainer view the Classroom Panel, observing incoming questions, and interacting with them.

### Implementation for User Story 2

- [x] T012 [P] [US2] Implement GET endpoints for trainer and student to list questions in `techpath-backend/app/api/v1/endpoints/trainer.py` and `student.py`
- [x] T013 [P] [US2] Implement POST endpoint `/api/v1/trainer/sessions/{session_id}/questions/{question_id}/answer` in `trainer.py`
- [x] T014 [P] [US2] Implement PATCH endpoint `/api/v1/trainer/sessions/{session_id}/settings` for `questions_are_public` toggle in `trainer.py` (if not already existing)
- [x] T015 [US2] Update `ClassroomBroadcaster` in `techpath-backend/app/services/classroom/bus.py` to broadcast `question_answered` and `questions_visibility_changed` events
- [x] T016 [P] [US2] Add Zustand state for Questions in `techpath-admin/src/store/classroom.store.ts` (or equivalent store)
- [x] T017 [US2] Build `ClassroomPanel` Q&A tab UI in `techpath-admin/src/components/training/` to list questions
- [x] T018 [US2] Integrate "Mark Answered" and "Public Questions" toggle into Trainer UI in `techpath-admin`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T019 [P] Validate UI handles empty question lists and extremely long question text gracefully in both `techpath-admin` and `techpath-frontend`
- [x] T020 Run quickstart.md validation end-to-end to ensure real-time WebSockets and API behave correctly under load.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch schema and UI tasks together:
Task: "Create Pydantic schemas for Question creation and responses"
Task: "Build 'Ask Question' React component UI"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories
