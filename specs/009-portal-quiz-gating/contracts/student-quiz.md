# Contract: Student Quiz Endpoints

All routes are under `/api/v1/student/`, authenticated by `get_current_student`.

**Response shape**: successful responses return the model **directly** — they are *not* wrapped in a `{success, data, timestamp}` envelope. That envelope exists only on error responses, produced by `app/middleware/error_handlers.py`. CLAUDE.md describes the envelope as universal; it isn't, and the bodies below are what the endpoints actually return. Verified against the running app.

---

## Changed: `GET /sessions/{session_id}/materials`

**No signature change.** The behavioural change is that quiz assets in `assets[]` are now redacted.

For an asset with `asset_type == "quiz"`, each entry in `config.questions` is:

```json
{ "question": "What does CIDR stand for?", "options": ["...", "...", "..."] }
```

`correct_index` and `explanation` MUST be absent — not null, absent. Every other asset type is unchanged.

> This is the FR-001 fix. The integration test asserting these two keys never appear in a student response is the regression guard for the whole feature.

---

## New: `GET /sessions/{session_id}/progress`

Tells the portal what is completed and what is locked, in one query.

**Response `data`:**

```json
{
  "session_id": 42,
  "first_locked_index": 3,
  "items": [
    { "asset_id": 101, "index": 0, "is_quiz": false, "passed": null, "locked": false },
    { "asset_id": 102, "index": 1, "is_quiz": true,  "passed": true,  "locked": false,
      "best_score": 4, "total_questions": 5, "attempt_count": 2 },
    { "asset_id": 103, "index": 2, "is_quiz": false, "passed": null, "locked": false },
    { "asset_id": 104, "index": 3, "is_quiz": true,  "passed": false, "locked": false,
      "best_score": 2, "total_questions": 5, "attempt_count": 1 },
    { "asset_id": 105, "index": 4, "is_quiz": false, "passed": null, "locked": true }
  ]
}
```

- `index` is position in module order and matches the portal's pager.
- `passed` is `null` for non-quiz items.
- `first_locked_index` is the index of the first quiz without a passing attempt (`4` would be `len(items)` if all passed). The quiz *at* that index is itself reachable — everything after it is locked.
- `best_score` / `attempt_count` are omitted when the student has no attempt on that quiz.

**Errors**: `404` if the session isn't one the student attended with published material.

---

## New: `POST /sessions/{session_id}/assets/{asset_id}/quiz-attempts`

Submits and grades an attempt.

**Request:**

```json
{ "answers": [2, 0, 1, 3, 0] }
```

Index-aligned to `config.questions`. One selected option index per question. No score field — a client-supplied score is ignored if sent (FR-006).

**Response `data`** (`201`):

```json
{
  "attempt_id": 77,
  "attempt_number": 2,
  "score": 4,
  "total_questions": 5,
  "percentage": 80.0,
  "passed": true,
  "pass_mark": 0.7,
  "attempted_at": "2026-07-18T10:31:04Z",
  "unlocked_next": true,
  "questions": [
    {
      "index": 0,
      "your_answer": 2,
      "correct_index": 2,
      "is_correct": true,
      "explanation": "CIDR is Classless Inter-Domain Routing."
    }
  ]
}
```

This response is the **only** place a student ever receives `correct_index` and `explanation`, and only for their own just-submitted attempt (FR-003).

`unlocked_next` lets the portal reveal the next item without refetching progress (FR-016).

**Errors:**

| Condition | Status | Exception |
|---|---|---|
| Session not attended / not published | 404 | `NotFoundError` |
| Asset not found in that session's material | 404 | `NotFoundError` |
| Asset is not a quiz | 422 | `ValidationError` |
| `answers` length ≠ question count | 422 | `ValidationError`, body names the missing indices |
| An answer out of range for its question | 422 | `ValidationError` |
| Duplicate concurrent submit | 201 | Returns the single recorded attempt; the unique constraint collapses the race (D6) |

---

## Frontend contract

`src/services/studentPortalService.ts` gains `getProgress(sessionId)` and `submitQuizAttempt(sessionId, assetId, answers)`. Per constitution principle I, no direct `fetch()` — these go through the existing helpers.

`ClassroomAssetView.jsx`'s `QuizView` becomes stateful: one selection per question, submit disabled until all are answered and while a request is in flight, then renders the returned per-question feedback with a retry affordance. It must tolerate a quiz whose `config.questions` lack `correct_index` — which, after this change, is always the case pre-submission.
