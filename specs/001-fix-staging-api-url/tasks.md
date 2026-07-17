# Tasks: Fix Staging API URL

**Input**: Design documents from `/specs/001-fix-staging-api-url/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

*(No setup tasks required for this bug fix)*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

*(No foundational tasks required for this bug fix)*

---

## Phase 3: User Story 1 - Fix Staging API URL (Priority: P1) 🎯 MVP

**Goal**: As a student or prospective customer accessing the platform on staging, I want all frontend interactions to point to the correct staging backend.

**Independent Test**: Build the frontend locally with `PUBLIC_API_URL=https://dummy-staging-api.techpath.biz npm run build` and run `npm run preview`. Verify that network requests to the API go to the dummy staging API instead of localhost.

### Implementation for User Story 1

- [x] T001 [P] [US1] Replace `VITE_API_BASE_URL` with `PUBLIC_API_URL` in `techpath-frontend/src/utils/api.ts`
- [x] T002 [P] [US1] Replace `VITE_API_BASE_URL` with `PUBLIC_API_URL` in `techpath-frontend/src/hooks/useClassroomSocket.ts`
- [x] T003 [P] [US1] Replace `VITE_API_BASE_URL` with `PUBLIC_API_URL` in `techpath-frontend/src/pages/api/contact.ts`
- [x] T004 [P] [US1] Replace `VITE_API_BASE_URL` with `PUBLIC_API_URL` in `techpath-frontend/src/pages/api/inquiry.ts`
- [x] T005 [P] [US1] Replace `VITE_API_BASE_URL` with `PUBLIC_API_URL` in `techpath-frontend/src/pages/api/newsletter.ts`
- [x] T006 [P] [US1] Remove `__API_BASE_URL__` definition from the `vite.define` block in `techpath-frontend/astro.config.mjs`
- [x] T007 [P] [US1] Update type definitions to replace `VITE_API_BASE_URL` with `PUBLIC_API_URL` in `techpath-frontend/src/env.d.ts`

**Checkpoint**: At this point, the API URL fix is fully implemented and should work correctly on the client side.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T008 [P] Update documentation to replace `VITE_API_BASE_URL` with `PUBLIC_API_URL` in `techpath-frontend/docs/DEPLOYMENT.md`
- [x] T009 Run quickstart.md validation to ensure the local build correctly points to the staging API

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: N/A
- **Foundational (Phase 2)**: N/A
- **User Stories (Phase 3)**: Can start immediately.
- **Polish (Final Phase)**: Depends on Phase 3 being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies. Can start immediately.

### Parallel Opportunities

- All tasks in Phase 3 (T001 - T007) are marked [P] as they modify different files and can be executed in parallel.
- Task T008 can also be executed in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch all file edits for User Story 1 together:
Task: "Replace VITE_API_BASE_URL with PUBLIC_API_URL in techpath-frontend/src/utils/api.ts"
Task: "Replace VITE_API_BASE_URL with PUBLIC_API_URL in techpath-frontend/src/hooks/useClassroomSocket.ts"
Task: "Remove __API_BASE_URL__ definition from the vite.define block in techpath-frontend/astro.config.mjs"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1.
2. **STOP and VALIDATE**: Test User Story 1 independently using the Quickstart guide.
3. Complete Polish tasks (documentation).
4. Deploy to staging.
