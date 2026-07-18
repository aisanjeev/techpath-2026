# Tasks: Trainer Material Visibility

**Input**: Design documents from `/specs/008-trainer-material-visibility/`

**Prerequisites**: plan.md, spec.md, data-model.md, contracts/api.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Exact file paths are included in descriptions.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

*No setup tasks needed. Both `techpath-backend` and `techpath-admin` are already initialized.*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

*No new database tables or foundational migrations needed. Existing models (`TrainingSession`, `TrainingModule`, `TrainingModuleAsset`, `LectureAsset`) will be used.*

---

## Phase 3: User Story 1 - Access Published Material from Logs (Priority: P1) 🎯 MVP

**Goal**: Trainers can access the published material associated with sessions directly from the presentation log report.

**Independent Test**: Navigate to a session log in the admin dashboard and verify the "View Published Material" button correctly loads the materials or is appropriately disabled if none exist.

### Implementation for User Story 1

- [x] T001 [US1] Expose backend endpoint to fetch assets for a given session (or module) in `techpath-backend/app/api/endpoints/sessions.py` (or a related controller).
- [x] T002 [US1] Add API client method in `techpath-admin/src/lib/api-client.ts` (or appropriate service file) to call the new/updated endpoint.
- [x] T003 [P] [US1] Create a UI component for the "View Published Material" button/modal in `techpath-admin/src/components/SessionMaterialsModal.tsx`.
- [x] T004 [US1] Integrate the button component into the presentation logs view (e.g., `techpath-admin/src/app/(dashboard)/sessions/page.tsx` or `[id]/page.tsx`).
- [x] T005 [US1] Implement conditional rendering to hide or disable the button (with a tooltip) if the session's module has no associated assets.

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [x] T006 [P] Verify feature using scenarios in `specs/008-trainer-material-visibility/quickstart.md`.
- [x] T007 Code cleanup and ensure Tailwind CSS styles match the existing dashboard design system.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup / Foundational**: N/A
- **User Stories**: US1 can begin immediately.
- **Polish**: Depends on US1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Only story. 

### Parallel Opportunities

- Creating the UI component (T003) can be done in parallel with the backend endpoint creation (T001).

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Implement backend endpoint (T001).
2. Implement frontend API client (T002) and UI components (T003, T004, T005).
3. **STOP and VALIDATE**: Test User Story 1 independently using the quickstart guide.
