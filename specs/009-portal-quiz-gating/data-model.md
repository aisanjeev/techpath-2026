# Phase 1 Data Model: Graded Quiz Attempts and Progress Gating

## New table: `session_quiz_attempts`

Lives in `app/models/training_roster.py` as `SessionQuizAttempt(Base, TimestampMixin)` — alongside the roster/session models it references, matching where `TrainingSessionQuestion` sits.

| Column | Type | Null | Notes |
|---|---|---|---|
| `id` | Integer PK, autoincrement | no | |
| `student_id` | Integer FK → `training_students.id` | no | `ondelete="CASCADE"` — attempts die with the student record |
| `session_id` | Integer FK → `training_sessions.id` | no | `ondelete="CASCADE"` — per spec, attempts are retained for the life of the session |
| `asset_id` | Integer FK → `lecture_assets.id` | no | `ondelete="CASCADE"` |
| `attempt_number` | Integer | no | 1-based, assigned server-side; part of the duplicate guard |
| `answers_json` | Text | no | JSON array of selected option indices, one per question, index-aligned to the quiz's `questions` |
| `score` | Integer | no | Count of correct answers |
| `total_questions` | Integer | no | Question count **at grading time** — see Staleness below |
| `passed` | Boolean | no | Frozen verdict at grading time |
| `attempted_at` | DateTime(timezone=True) | no | UTC |
| `created_at` / `updated_at` | DateTime(timezone=True) | no | From `TimestampMixin` |

**Constraints and indexes**

- `UniqueConstraint("student_id", "asset_id", "attempt_number", name="uq_quiz_attempt_number")` — the actual double-submit guard (D6). Follows the `SessionPollVote` precedent of making the DB the guard rather than client state.
- `Index("ix_quiz_attempts_session_asset", "session_id", "asset_id")` — serves the trainer results query.
- `Index("ix_quiz_attempts_student_session", "student_id", "session_id")` — serves the student progress query, which must be **one** query for a whole session's material, not one per asset.

**Rows are immutable.** A retry inserts a new row with the next `attempt_number`. Nothing updates `score`, `passed`, or `answers_json` after insert.

**Migration**: `20260718_quiz_attempts.py`, revision `z1q2u3i4z5a6`, `down_revision = 'b1r2o3a4d5c6'` (`20260718_media_broadcasting.py`, which was the head). Use only dialect-neutral types: `sa.Text` for JSON, `sa.Boolean`, `sa.DateTime(timezone=True)` — no Postgres constructs (see the storage note in plan.md). No `server_default` on the timestamps: `TimestampMixin` supplies them Python-side, and `sa.text('now()')` (used by an earlier migration in this repo) is not valid on SQLite.

> **Correction, found during implementation.** An earlier draft of this document claimed the repo had a second migration head at `t7f8g9h0i1j2`. It does not — `alembic heads` reports a single head. That claim was wrong and has been removed. `alembic upgrade heads` (plural) still works and remains what the deploy runs, but it is not compensating for a branched history here.

> **Downgrade caveat, found by testing.** `downgrade()` must call only `drop_table`. Dropping the indexes explicitly first fails on MySQL: `ix_quiz_attempts_session_asset` leads with `session_id`, so InnoDB uses it to back that column's foreign key and refuses with *"Cannot drop index … needed in a foreign key constraint"*. SQLite tolerates the explicit drops, so this reproduces only on MySQL.

---

## Derived: student progress

Not a table. Computed per request from attempts plus the session's asset list.

For each asset in module order:

```
is_quiz  = asset.asset_type == 'quiz'
passed   = is_quiz AND EXISTS(attempt WHERE student, asset, passed = true)
locked   = index > first_locked_index
```

where `first_locked_index` is the index of the first quiz asset without a passing attempt, or `len(assets)` when there is none. Non-quiz assets never contribute a lock (FR-018).

A quiz with zero questions grades as `0/0 = passed` (D3), so it never blocks — the empty-quiz edge case needs no special handling at this layer.

---

## Staleness

An attempt is presented as stale when `attempt.total_questions != current question count of the asset`.

This is a deliberately partial check. It catches questions being added or removed. It does **not** catch a question being reworded, or its `correct_index` changed, while the count stays the same — such an attempt will appear current. Accepted per D5; the upgrade path is a content hash, which is additive and needs no migration of existing rows.

Stale attempts keep their original score and pass status. A student who passed stays passed.

---

## Existing entities touched

**`LectureAsset`** — no schema change. Its `config_json` holds `{questions: [{question, options[], correct_index, explanation}]}` for quiz assets. What changes is only how it is *serialized*: `asset_to_response()` gains an audience parameter and strips `correct_index` and `explanation` from each question for the student audience (D1).

**`TrainingStudent`**, **`TrainingSession`**, **`TrainingBatch`** — referenced only. Trainer access to results goes through `session.batch.trainer_email` via the existing `_assert_owns_batch` guard in `trainer_reports.py`.

---

## Validation rules

Applied server-side before any row is written:

| Rule | Failure | Source |
|---|---|---|
| Asset exists and is `asset_type == 'quiz'` | `ValidationError` | FR-011 |
| Session is one the student attended and whose material is published | `NotFoundError` | FR-023 |
| `answers` length equals the quiz's question count | `ValidationError`, naming missing indices | FR-005 |
| Every answer is an integer in range for its question's options | `ValidationError` | FR-011 |
| Score computed server-side only; any client-supplied score ignored | — | FR-006 |

`NotFoundError` rather than `ForbiddenError` for the access rule, matching how `get_session_materials` already handles a session the student isn't enrolled in — it avoids confirming the session exists to someone with no right to know.
