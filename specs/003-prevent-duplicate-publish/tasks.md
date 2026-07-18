# Tasks: Prevent Duplicate Publish

**Input**: Design documents from `/specs/003-prevent-duplicate-publish/`

**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

*(No setup tasks required)*

---

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T001 [P1] [US1] Add `get_published_by_batch_and_module` query to `training_session_crud`.

---

## Phase 3: User Story 1 - Prevent Duplicate Publish (Priority: P1) 🎯 MVP

**Goal**: Prevent trainers from publishing multiple sessions for the exact same batch and module combination.

### Implementation for User Story 1

- [x] T002 [US1] Update `POST /sessions/{session_id}/materials/publish` in `trainer.py` to call `get_published_by_batch_and_module`.
- [x] T003 [US1] Raise `ValidationError` if another session is already published.

**Checkpoint**: Backend uniqueness check is live.

---

## Phase 4: Polish & Cross-Cutting Concerns

- [x] T004 Run local validation (e.g. backend startup/tests) to ensure no syntax errors.
