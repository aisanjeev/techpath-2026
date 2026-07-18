---

description: "Task list for Graded Quiz Attempts and Progress Gating"
---

# Tasks: Graded Quiz Attempts and Progress Gating

**Input**: Design documents from `/specs/009-portal-quiz-gating/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/)

**Tests**: Test tasks ARE included. Research decision D8 makes them load-bearing rather than optional — the integration test asserting the answer key never reaches a student endpoint is what makes the unredacted default in D1 safe, and the grading boundary tests cover the arithmetic most likely to be quietly wrong.

**Organization**: Grouped by user story so each is independently implementable and testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Exact file paths included in every task

## Path Conventions

Monorepo, three apps (see plan.md "Source Code"):

- Backend: `techpath-backend/app/...`, tests in `techpath-backend/tests/`
- Student portal: `techpath-frontend/src/...`
- Trainer dashboard: `techpath-admin/src/...`

---

## Phase 1: Setup

**Purpose**: Configuration groundwork. Small — this feature adds to an existing, running system.

- [X] T001 Add `QUIZ_PASS_MARK: float = Field(default=0.7)` to the Settings class in `techpath-backend/app/core/config.py`, following the existing `ROSTER_SYNC_PAGE_SIZE` pattern
- [X] T002 [P] Document `QUIZ_PASS_MARK` in `techpath-backend/.env.example` with a note that it is a fraction (0.7), not a percentage (70)

---

## Phase 2: Foundational (Attempt Persistence)

**Purpose**: The attempt storage and grading layer that User Stories 2, 3, and 4 all build on.

**⚠️ Blocks US2, US3, US4 — but NOT US1.** User Story 1 is the answer-key redaction and touches none of this. It can be implemented and shipped before or alongside this phase. See Dependencies below; the template's usual "foundational blocks everything" does not hold here and forcing that order would needlessly delay a live data-exposure fix.

- [X] T003 Create `SessionQuizAttempt(Base, TimestampMixin)` in `techpath-backend/app/models/training_roster.py` per [data-model.md](./data-model.md) — columns, both indexes, and the `uq_quiz_attempt_number` unique constraint on `(student_id, asset_id, attempt_number)`
- [X] T004 Create Alembic migration `techpath-backend/app/db/migrations/versions/20260718_quiz_attempts.py` with `down_revision = 'b1r2o3a4d5c6'`, using only dialect-neutral types (`sa.Text` for `answers_json`, `sa.Boolean`, `sa.DateTime(timezone=True)`) so it applies on both SQLite and MySQL
- [X] T005 Verify the migration applies and rolls back cleanly on SQLite: `cd techpath-backend && poetry run alembic upgrade heads && poetry run alembic downgrade -1 && poetry run alembic upgrade heads` (note `heads` plural — the repo has a second head at `t7f8g9h0i1j2`)
- [X] T006 [P] Create `techpath-backend/app/crud/quiz_attempts.py` with a `CRUDBase` subclass exposing: create an attempt, list attempts for `(student, asset)`, next attempt number for `(student, asset)`, best attempt per student for a set of assets, and passing-asset ids for `(student, session)` in a single query
- [X] T007 [P] Create `techpath-backend/app/services/quiz_grading.py` with pure grading logic: compare submitted answers to `correct_index`, compute `score`/`total_questions`, and decide `passed` as `score / total >= QUIZ_PASS_MARK` compared as a **fraction, never a rounded percentage** (D3). A zero-question quiz returns passed.

**Checkpoint**: Attempts can be stored and graded. US2, US3, US4 unblocked.

---

## Phase 3: User Story 1 — Answer Key Is Never Given to Students (Priority: P1) 🎯 MVP

**Goal**: `correct_index` and `explanation` stop reaching students on every student-facing surface, while trainers and admins keep seeing them.

**Independent Test**: Open a session's materials as a student and inspect the raw response — neither key appears on any quiz question. Request the same asset as a trainer — both are present.

**Why this ships first**: It is a live exposure on already-published material and depends on nothing else in the feature.

### Tests for User Story 1

- [X] T008 [P] [US1] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: `GET /student-portal/sessions/{id}/materials` for a session with a quiz asset returns questions where `correct_index` and `explanation` are **absent** (assert key absence, not null values)
- [X] T009 [P] [US1] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: the trainer/admin asset response for the same asset still contains `correct_index` and `explanation` unchanged

### Implementation for User Story 1

- [X] T010 [US1] Add an `audience` parameter to `asset_to_response()` in `techpath-backend/app/crud/training.py`, defaulting to the trainer/admin view; when the student audience is passed, strip `correct_index` and `explanation` from each entry of `config["questions"]` for `asset_type == "quiz"`. Deep-copy the config before stripping so the mutation cannot leak into a cached or shared dict.
- [X] T011 [US1] Pass the student audience at the materials call site in `techpath-backend/app/api/v1/endpoints/student_portal.py` (line ~98)
- [X] T012 [US1] Pass the student audience at the live-classroom call site in `techpath-backend/app/api/v1/endpoints/classroom.py` (line ~205)
- [X] T013 [US1] Confirm the remaining `asset_to_response` call sites in `techpath-backend/app/api/v1/endpoints/trainer.py` and `techpath-backend/app/api/v1/endpoints/training.py` are left on the default trainer audience, and note in the function docstring that any new student-facing caller must opt in
- [X] T014 [US1] Update `QuizView` in `techpath-frontend/src/components/react-components/ClassroomAssetView.jsx` so it no longer assumes `correct_index` exists — it must render correctly from questions and options alone

**Checkpoint**: US1 complete and independently shippable. The answer key no longer leaves the server for students.

---

## Phase 4: User Story 2 — Student Takes and Submits a Graded Quiz (Priority: P1)

**Goal**: A student selects an answer per question, submits, and gets a server-computed score with per-question feedback and explanations. Unlimited retries.

**Independent Test**: Open a quiz in the portal, answer all questions, submit, see score and per-question feedback. Retry and get a second independent result.

**Depends on**: Phase 2. Builds on US1's redaction but is testable on its own.

### Tests for User Story 2

- [X] T015 [P] [US2] Unit tests in `techpath-backend/tests/test_quiz_grading.py` for the grading boundary: 2/3 **fails** at a 0.7 pass mark (0.667 — the case a rounding bug silently passes), 7/10 passes, 3/3 passes, 0/0 passes
- [X] T016 [P] [US2] Unit tests in `techpath-backend/tests/test_quiz_grading.py` for malformed submissions: wrong answer count, an option index out of range, a non-integer answer
- [X] T017 [P] [US2] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: submitting an attempt returns score, `passed`, and per-question `correct_index`/`explanation` — the only place a student receives them
- [X] T018 [P] [US2] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: two identical concurrent submissions record exactly one attempt (the unique constraint collapses the race)
- [X] T019 [P] [US2] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: a student cannot submit against a session they did not attend or whose material is unpublished (404)

### Implementation for User Story 2

- [X] T020 [P] [US2] Add submission and result schemas to `techpath-backend/app/schemas/student_portal.py` per [contracts/student-quiz.md](./contracts/student-quiz.md) — request carries `answers` only; any client-sent score is ignored
- [X] T021 [US2] Implement `POST /sessions/{session_id}/assets/{asset_id}/quiz-attempts` in `techpath-backend/app/api/v1/endpoints/student_portal.py`: validate access via `get_enrolled_published`, validate the asset is a quiz, validate answers, grade via the service, persist, and return per-question feedback
- [X] T022 [US2] Add validation error paths in the same endpoint using `ValidationError`/`NotFoundError` from `techpath-backend/app/core/exceptions.py` — answer-count mismatch names the missing question indices (FR-005)
- [X] T023 [P] [US2] Add `submitQuizAttempt(sessionId, assetId, answers)` to `techpath-frontend/src/services/studentPortalService.ts` using the existing API helpers (no direct `fetch`)
- [X] T024 [P] [US2] Add attempt and result types to `techpath-frontend/src/types/studentPortal.ts`
- [X] T025 [US2] Make `QuizView` interactive in `techpath-frontend/src/components/react-components/ClassroomAssetView.jsx`: one selection per question, freely changeable, submit disabled until all answered and while in flight
- [X] T026 [US2] Add the result view to the same component: score, pass/fail, per-question correct/incorrect with explanations, and a retry action that clears selections without preselecting prior answers

**Checkpoint**: Students can take and be scored on quizzes. Combined with US1, this is the functional-quiz MVP.

---

## Phase 5: User Story 3 — Quiz Gates Progress Through Material (Priority: P2)

**Goal**: A student cannot page past a quiz until they pass it; the portal shows what is completed and what is locked.

**Independent Test**: Reach a quiz mid-material with no passing attempt, try to advance — blocked. Pass it — the next item becomes reachable without reload.

**Depends on**: Phase 2 and US2 (needs attempts to exist).

### Tests for User Story 3

- [X] T027 [P] [US3] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: the progress endpoint reports `first_locked_index` at the first unpassed quiz, and marks later items locked
- [X] T028 [P] [US3] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: after a passing submission the previously locked next item is no longer locked; material with no quiz reports nothing locked; a zero-question quiz never locks

### Implementation for User Story 3

- [X] T029 [P] [US3] Add progress schemas to `techpath-backend/app/schemas/student_portal.py` per [contracts/student-quiz.md](./contracts/student-quiz.md)
- [X] T030 [US3] Implement `GET /sessions/{session_id}/progress` in `techpath-backend/app/api/v1/endpoints/student_portal.py` — resolve passing-asset ids in **one** query via the T006 CRUD method, not one per asset
- [X] T031 [US3] Add the `unlocked_next` field to the submit response in the same file so the portal can reveal the next item without refetching (FR-016)
- [X] T032 [P] [US3] Add `getProgress(sessionId)` to `techpath-frontend/src/services/studentPortalService.ts` and progress types to `techpath-frontend/src/types/studentPortal.ts`
- [X] T033 [US3] Fetch progress on load in `techpath-frontend/src/components/react-components/StudentPortalApp.jsx` and disable the Next control past `first_locked_index`; leave Previous unrestricted at all times (FR-015)
- [X] T034 [US3] Show per-item completion state and an explanation of why a locked item is locked in `techpath-frontend/src/components/react-components/StudentPortalApp.jsx` (FR-019)
- [X] T035 [US3] Unlock the next item in-place on a passing submission in `StudentPortalApp.jsx`, driven by `unlocked_next` — no page reload

**Checkpoint**: Portal behaves like a sequenced LMS. Note this is a navigation guard, not an access boundary (see plan.md post-design note).

---

## Phase 6: User Story 4 — Trainer Sees Who Passed (Priority: P3)

**Goal**: A trainer sees, per quiz in a session, every roster student's best score and pass status — including non-attempters — plus per-question success rates.

**Independent Test**: With two students attempted and one not, open the session report as their trainer and see all three. Request as a non-owning trainer and get 403.

**Depends on**: Phase 2 and US2 (needs attempt data).

### Tests for User Story 4

- [X] T036 [P] [US4] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: results include roster students with zero attempts, and `best_score`/`passed` reflect the best of multiple attempts
- [X] T037 [P] [US4] Integration test in `techpath-backend/tests/test_student_quiz_flow.py`: a trainer who does not own the batch gets 403; an admin gets results

### Implementation for User Story 4

- [X] T038 [P] [US4] Add quiz-results schemas to `techpath-backend/app/schemas/trainer_reports.py` per [contracts/trainer-quiz-results.md](./contracts/trainer-quiz-results.md)
- [X] T039 [US4] Implement `GET /sessions/{session_id}/quiz-results` in `techpath-backend/app/api/v1/endpoints/trainer_reports.py`, reusing that module's `_assert_owns_batch` guard. Query **from the batch roster left-joined to attempts** so students with no attempt appear (FR-020)
- [X] T040 [US4] Compute `question_stats` in the same endpoint from each student's **best** attempt only, so retries don't skew a question's success rate
- [X] T041 [US4] Set `is_stale` per student by comparing the attempt's `total_questions` to the asset's current question count (D5); do not regrade
- [X] T042 [P] [US4] Add `getQuizResults(sessionId)` to `techpath-admin/src/services/trainer.service.ts` and result types to `techpath-admin/src/types/classroom.ts`
- [X] T043 [US4] Add a "Quiz results" section to `techpath-admin/src/app/(trainer)/trainer/sessions/[id]/report/page.tsx`, following the existing Attendance and Poll history sections — fetch alongside them in the same `Promise.allSettled` block, and surface stale attempts visibly

**Checkpoint**: All four stories independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T044 [P] Run backend quality gates: `cd techpath-backend && poetry run black app tests && poetry run ruff check app tests && poetry run mypy app`
- [X] T045 [P] Run frontend and admin lint: `cd techpath-frontend && npm run lint` and `cd techpath-admin && npm run lint`
- [X] T046 Run the full backend suite and confirm no regression: `cd techpath-backend && poetry run pytest --cov=app`
- [X] T047 Regression-check feature 007's live poll path per [quickstart.md](./quickstart.md): trainer launches a question from a quiz asset, votes tally live, closing reveals the correct answer
- [X] T048 Walk all four scenarios in [quickstart.md](./quickstart.md) end to end against a running dev stack
- [X] T049 [P] Update `CLAUDE.md` with the quiz-attempt model and the `asset_to_response` audience rule, so the next contributor doesn't reintroduce the leak

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: no dependencies
- **Phase 2 (Foundational)**: after Setup. Blocks US2, US3, US4 — **not US1**
- **Phase 3 (US1)**: after Setup only. Independent of Phase 2 and of every other story
- **Phase 4 (US2)**: after Phase 2
- **Phase 5 (US3)**: after Phase 2 and US2
- **Phase 6 (US4)**: after Phase 2 and US2
- **Phase 7 (Polish)**: after the stories being shipped

### User Story Dependencies

- **US1 (P1)**: fully independent. Can ship on its own, first — and should, since it closes a live exposure
- **US2 (P1)**: needs Phase 2. Does not need US1 to function, though shipping US1 first is strongly preferred so the client is never trusted with the key
- **US3 (P2)**: needs US2 — gating is meaningless without attempts
- **US4 (P3)**: needs US2 — reads attempt data. Independent of US3

### Within Each Story

- Tests before implementation
- Models → CRUD → services → endpoints → frontend
- Backend contract settled before the frontend consuming it

### Parallel Opportunities

- T001/T002 in Setup
- T006 and T007 in Phase 2 (different new files)
- **US1 (Phase 3) can run fully in parallel with Phase 2** — different files, no shared state
- All test tasks marked [P] within a story
- Once Phase 2 and US2 land, US3 and US4 are independent of each other and can run in parallel
- Within US2: T023/T024 (frontend service and types) parallel with T020 (backend schemas)

---

## Parallel Example: User Story 1 alongside Foundational

```bash
# Developer A — close the exposure (Phase 3):
Task: "Add audience parameter to asset_to_response in techpath-backend/app/crud/training.py"
Task: "Integration test asserting no correct_index in student materials response"

# Developer B — build persistence (Phase 2), concurrently:
Task: "Create SessionQuizAttempt model in techpath-backend/app/models/training_roster.py"
Task: "Create Alembic migration 20260718_quiz_attempts.py"
```

---

## Implementation Strategy

### MVP First

1. Phase 1 (Setup) — two small tasks
2. **Phase 3 (US1) — ship this alone if nothing else.** It closes a live answer-key exposure and needs no schema change
3. Phase 2 (Foundational) + Phase 4 (US2) — quizzes become genuinely functional
4. **STOP and VALIDATE**: quickstart Scenarios 1 and 2
5. Deploy — at this point the user's core complaint ("looks not functional") is resolved

### Incremental Delivery

1. US1 → deploy (security fix, standalone)
2. Foundational + US2 → deploy (working graded quiz)
3. US3 → deploy (gating — "proceed further")
4. US4 → deploy (trainer visibility)

### Deployment Note

The migration must be applied manually on the VPS after deploying the backend — `poetry run alembic upgrade heads` (plural, per CLAUDE.md). US1 alone requires no migration, which is another reason it ships cleanly first.

---

## Notes

- `[P]` = different files, no dependencies on incomplete tasks
- Grading compares fractions, never rounded percentages — see T015
- The redaction test (T008) is the regression guard for the whole feature; do not weaken it to assert `null` instead of key absence
- Commit after each task or logical group

---

## Implementation Notes (post-completion)

Recorded because they contradict what the plan assumed. Anyone reading the design docs alone would be misled.

1. **A third answer-key leak existed.** The spec listed two student-facing call sites; `set_slide` in `trainer.py` was a third — trainer-authenticated but broadcasting the asset to every student. The rule is that redaction follows the **audience of the payload**, not the caller's role. See D1 in research.md.
2. **Per-quiz pass marks already existed.** `QuizAssetIn.pass_mark_percent` (default 60) was already in the authoring schema. The implementation honours it over the global `QUIZ_PASS_MARK`, converting percentage → fraction. See D3.
3. **The student-portal prefix is `/student`, not `/student-portal`.** The contracts have been corrected.
4. **Successful responses are not enveloped.** `{success, data, timestamp}` is error-only, from `middleware/error_handlers.py`. CLAUDE.md describes it as universal; it is not.
5. **There is only one migration head.** The claim of a second head at `t7f8g9h0i1j2` was wrong.
6. **The migration's `downgrade()` must only `drop_table`.** Explicit `drop_index` first fails on MySQL because the composite index backs a foreign key. Caught by T005.
7. **T044's `black app tests` reformats 137 files.** The repo has never been black-formatted, so running it as written produces an enormous unrelated diff. Only the new files were formatted; everything else was reverted. Ruff (1854 baseline errors) and mypy (180 baseline) are likewise not clean — only genuine issues in new code were fixed, bringing mypy to 163.

### Verification status

Verified: all 49 quiz tests pass against the real ASGI app; full suite 207 passed / 3 failed (the 3 are pre-existing `test_recordings.py` failures, confirmed identical on clean `HEAD`); migration applies and rolls back on MySQL; new routes and schemas present in the live OpenAPI spec; all three endpoints reject unauthenticated access; frontend builds and the portal loads with no console errors.

**Not verified:** the student quiz UI past the Google sign-in gate, and the trainer's quiz-results panel. Both need real authentication, which cannot be performed here. Their behaviour is covered by integration tests, but nobody has looked at them on screen — walk quickstart.md Scenarios 2–4 manually before shipping.
