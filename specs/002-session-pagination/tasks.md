# Tasks: Session Pagination

**Input**: Design documents from `/specs/002-session-pagination/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

*(No setup tasks required for this UI fix)*

---

## Phase 2: Foundational (Blocking Prerequisites)

*(No foundational tasks required for this UI fix)*

---

## Phase 3: User Story 1 - Paginated Session Content (Priority: P1) 🎯 MVP

**Goal**: As a student viewing a session in the portal, I want to navigate through the session content using a paginated "Next/Previous" interface rather than scrolling a long continuous page.

### Implementation for User Story 1

- [x] T001 [P] [US1] Update `StudentPortalApp.jsx` to parse `page` query parameter from the URL.
- [x] T002 [US1] Add `currentPage` state to `StudentPortalApp.jsx` and handle pushState for `session` and `page`.
- [x] T003 [US1] Update `popstate` listener in `StudentPortalApp.jsx` to respect `page`.
- [x] T004 [US1] Update `MaterialsScreen` in `StudentPortalApp.jsx` to show only one asset at a time based on `currentPage`.
- [x] T005 [US1] Add Next and Previous buttons to `MaterialsScreen`.

**Checkpoint**: Pagination works and updates the URL.

---

## Phase 4: Polish & Cross-Cutting Concerns

- [x] T006 Run local build validation to ensure no React errors.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1.
2. **STOP and VALIDATE**: Test User Story 1 independently using the Quickstart guide.
