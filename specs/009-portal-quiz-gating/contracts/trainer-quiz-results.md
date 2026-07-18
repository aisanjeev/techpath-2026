# Contract: Trainer Quiz Results

Added to `app/api/v1/endpoints/trainer_reports.py`, mounted under the `/trainer` prefix. Guarded by `get_current_trainer_user` plus that module's existing `_assert_owns_batch` (trainer sees own batches; admin sees all).

---

## New: `GET /api/v1/trainer/sessions/{session_id}/quiz-results`

**Response `data`:**

```json
{
  "session_id": 42,
  "quizzes": [
    {
      "asset_id": 102,
      "title": "Networking Fundamentals Check",
      "total_questions": 5,
      "pass_mark": 0.7,
      "attempted_count": 11,
      "passed_count": 8,
      "roster_size": 14,
      "question_stats": [
        { "index": 0, "question": "What does CIDR stand for?", "correct_count": 10, "attempted_count": 11 }
      ],
      "students": [
        {
          "student_id": 5, "name": "…", "email": "…",
          "attempt_count": 2, "best_score": 4, "total_questions": 5,
          "passed": true, "last_attempted_at": "2026-07-18T10:31:04Z", "is_stale": false
        },
        {
          "student_id": 9, "name": "…", "email": "…",
          "attempt_count": 0, "best_score": null, "total_questions": null,
          "passed": false, "last_attempted_at": null, "is_stale": false
        }
      ]
    }
  ]
}
```

**Behaviour notes that are part of the contract, not implementation detail:**

- `students[]` includes **every roster student on the batch**, including those with `attempt_count: 0` (FR-020). The query starts from the roster and left-joins attempts. A trainer's most useful signal is usually who hasn't engaged at all, which an attempts-only query would silently drop.
- `best_score` is the highest score across attempts; `passed` is true if *any* attempt passed. Unlimited retries mean best-of is the meaningful summary.
- `question_stats[].correct_count` counts each student's **best** attempt only, so a student retrying doesn't skew a question's success rate by contributing several times. `attempted_count` is the denominator for that question.
- `is_stale` is true when the student's best attempt was graded against a different question count than the quiz currently has (D5). Partial by design — it does not detect a reworded question at unchanged count.
- `total_questions` at the quiz level is the asset's **current** count; at the student level it is the count their attempt was graded against. These differ exactly when `is_stale` is true.

**Errors:**

| Condition | Status | Exception |
|---|---|---|
| Session not found | 404 | `NotFoundError` |
| Session's batch not assigned to this trainer (and caller isn't admin) | 403 | `ForbiddenError` |

Sessions whose module has no quiz assets return `quizzes: []` rather than an error.

---

## Admin contract

`src/services/trainer.service.ts` gains `getQuizResults(sessionId)`; types go in `src/types/classroom.ts`. Rendered on the existing session report surface alongside attendance and poll history, per constitution principle II — components call the service, never axios directly.
