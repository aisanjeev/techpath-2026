# Quickstart: Validating Graded Quiz Attempts and Progress Gating

How to prove this feature works end to end once implemented. Scenarios map to the spec's user stories.

## Prerequisites

- Backend deps installed and a dev DB present:
  ```bash
  cd techpath-backend
  poetry install
  poetry run alembic upgrade heads    # plural — the repo has two migration heads
  ```
- Seeded training data including a quiz asset. `scripts/seed_training_demo.py` already creates quiz assets:
  ```bash
  poetry run python scripts/seed_training_demo.py
  ```
- A batch with at least two roster students, a session with published material whose module contains a quiz, and both students marked as having attended.
- `.env.local` may set `QUIZ_PASS_MARK` (defaults to `0.7`).

## Running

```bash
# Backend
cd techpath-backend && poetry run uvicorn app.main:app --reload      # :8000

# Student portal
cd techpath-frontend && npm run dev                                  # :4321  → /portal

# Trainer dashboard
cd techpath-admin && npm run dev                                     # :3000
```

---

## Scenario 1 — Answer key is not sent to students (User Story 1, P1)

The single most important check in the feature.

1. Sign in to `/portal` as a roster student and open a session whose material contains a quiz.
2. In devtools → Network, find the `sessions/{id}/materials` response.
3. Search the raw JSON for `correct_index` and `explanation`.

**Expected**: zero matches. Not `null` values — the keys are absent from every quiz question.

4. Now call the trainer-side asset endpoint as a trainer (or open the CMS quiz editor in the admin app).

**Expected**: `correct_index` and `explanation` present and unchanged. Redaction is student-audience only.

Contract: [student-quiz.md](./contracts/student-quiz.md).

---

## Scenario 2 — Take, grade, and retry a quiz (User Story 2, P1)

1. As the student, page to the quiz. Every question is selectable; selections can be changed.
2. Try to submit with a question unanswered.
   **Expected**: refused, unanswered questions indicated (FR-005).
3. Answer all questions deliberately **wrong** and submit.
   **Expected**: score, fail verdict, per-question right/wrong marks, and the explanation for each — the first time any of that has reached the browser.
4. Choose retry.
   **Expected**: fresh quiz, nothing preselected. The first attempt stays on record.
5. Answer correctly, submit.
   **Expected**: pass verdict.
6. Double-click submit on a further attempt.
   **Expected**: exactly one new attempt recorded — verify via the trainer view in Scenario 4 or by counting rows.

Boundary worth checking explicitly: on a **3-question** quiz, 2 correct must **fail** at the 0.7 pass mark (2/3 = 0.667). This is the case a rounding bug would silently pass.

---

## Scenario 3 — Gating (User Story 3, P2)

1. Find a session whose material has a quiz that is *not* the last item.
2. As a student with no passing attempt, page forward to the quiz and try to advance.
   **Expected**: blocked, with an explanation of why and what to do (FR-019).
3. Page backwards.
   **Expected**: always allowed (FR-015).
4. Submit a passing attempt.
   **Expected**: the next item becomes reachable immediately, no page reload (FR-016).
5. Sign out, sign back in, reopen.
   **Expected**: still passed, still unlocked (FR-017).
6. Open material containing **no** quiz.
   **Expected**: every item reachable, no gating (FR-018, SC-008).

Also confirm a **zero-question** quiz never blocks — it grades as passed by definition.

---

## Scenario 4 — Trainer sees results (User Story 4, P3)

1. Have two students submit attempts, one passing and one not; leave a third roster student with no attempt.
2. Open the session report in the admin app as the batch's trainer.

**Expected**: all three students listed — including the one with **no** attempt, shown as not passed with a zero attempt count. Best score per student, and a per-question success rate that makes a commonly-missed question visible.

3. Sign in as a trainer who does **not** own that batch and request the same session's results.
   **Expected**: `403`.
4. Edit the quiz to add a question, then re-open the report.
   **Expected**: prior attempts still show their original scores, flagged stale. Students who had passed remain passed.

Contract: [trainer-quiz-results.md](./contracts/trainer-quiz-results.md).

---

## Automated checks

```bash
cd techpath-backend
poetry run pytest tests/test_quiz_grading.py tests/test_student_quiz_flow.py -v
poetry run pytest --cov=app          # full suite, confirm no regression
poetry run mypy app && poetry run ruff check app tests && poetry run black --check app tests
```

The grading unit tests must cover the boundary arithmetic (2/3 fails, 7/10 passes, 0/0 passes) and malformed submissions. The integration test asserting no `correct_index` reaches a student endpoint is the regression guard that keeps Scenario 1 true as new student-facing call sites are added.

## Regression check

Feature 007's live poll path must be unaffected: a trainer can still open the Poll tab, launch a question from a quiz asset, watch votes tally live, and close the poll to reveal the correct answer. Nothing in this feature changes it, but the shared quiz config shape means it is worth confirming.
