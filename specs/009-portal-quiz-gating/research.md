# Phase 0 Research: Graded Quiz Attempts and Progress Gating

All Technical Context unknowns are resolved. No `NEEDS CLARIFICATION` markers remain.

---

## D1. Where to strip the answer key

**Decision**: Add an `audience` parameter to `asset_to_response()` in `app/crud/training.py`, defaulting to the trainer/admin view. Student-facing callers pass the student audience and get quiz `config.questions[*]` with `correct_index` and `explanation` removed.

**Rationale**: That function's own docstring states it exists so its three callers — the admin module endpoint, the trainer's slide broadcast, and the student classroom fetch — "can't quietly drift apart". Redaction belongs at exactly that choke point. The current leak is what drift looks like: the function was written for the trainer case and student surfaces inherited it unexamined.

> **Third leak found during implementation.** The spec listed two student-facing call sites (portal materials, classroom state). There is a **third**: `set_slide` in `app/api/v1/endpoints/trainer.py` serializes the asset and then `bus.publish`es it to every connected student as a `slide_change` event. It is trainer-authenticated, so an audit by *caller role* passes it — but the payload is student-destined, so it leaked the answer key to the whole class the moment a trainer put a quiz slide on screen. This was arguably the worst of the three, being live and during class.
>
> The rule is therefore: **redaction follows the audience of the payload, not the role of the caller.** All three now pass `audience="student"`; the six admin-CMS call sites in `training.py` and the trainer's own module fetch in `trainer.py` correctly keep the default.

Defaulting to the *unredacted* trainer view is deliberate despite the usual "secure by default" instinct. There are ten call sites, eight of them trainer/admin. A student-safe default would silently strip answers from the CMS editor and the presenter view — a loud, immediately-noticed breakage, but it would also mean every trainer call site needs an explicit opt-out, and a *missed* one degrades trainer UX rather than leaking data. Since the redaction is enforced by an integration test that asserts on the student endpoints specifically (T-tests in tasks), the risk of a missed student call site is covered by the test rather than by the default.

**Alternatives considered**:
- *Redact in each student-facing endpoint* — rejected: two call sites today, more later, and each is a fresh chance to forget. This is precisely the failure mode being fixed.
- *Separate `StudentLectureAssetResponse` schema* — rejected for now: it duplicates ten-plus fields to vary one, and every future asset field would need adding twice. Worth revisiting if student/trainer asset views diverge further than this one blob.
- *Strip at the model layer / never load the key* — rejected: the grader needs the key on the same request path.

---

## D2. Attempt persistence shape

**Decision**: One new table, `session_quiz_attempts`. Immutable rows: `(student_id, session_id, asset_id, answers_json, score, total_questions, passed, attempted_at)`. A retry inserts a new row. No progress table.

**Rationale**: "Has this student passed this quiz" is `EXISTS(... AND passed = true)` — cheap and always consistent with the attempt history. A separate progress table would be derived state needing to be kept in sync, with a real risk of the two disagreeing. Storing the attempt history for free also satisfies the trainer-visibility story and gives per-question analytics with no extra writes.

`answers_json` as a JSON array of selected option indices keeps the schema dialect-neutral across SQLite and MySQL — the codebase already stores `options_json`, `config_json`, and `tags_json` as `Text`, so this follows the established convention rather than reaching for a native JSON column that behaves differently on each backend.

**Alternatives considered**:
- *One row per answer* — rejected: correct normalization, but turns a submission into N inserts and every read into a join, for data that is only ever read as a whole attempt.
- *Update a single row per (student, quiz)* — rejected: destroys the retry history the trainer story needs, and the spec explicitly calls attempts immutable.

---

## D3. Pass mark and the boundary case

**Decision**: `QUIZ_PASS_MARK: float = Field(default=0.7)` in `app/core/config.py`. An attempt passes when `correct / total >= QUIZ_PASS_MARK`, compared as a fraction — never as a rounded percentage.

**Rationale**: The spec's edge case (3 questions, 70% pass mark) is the whole reason to pin this down. 2/3 = 0.667, which is below 0.7 and must fail. Rounding to a whole percent first gives 67% — still a fail — but rounding *up* anywhere in the chain would give 70% and silently pass. Comparing the raw fraction has no such failure mode. A zero-question quiz is defined as passed (`0/0`), which is what makes FR-018 and the empty-quiz edge case fall out for free rather than needing a special case at the gating layer.

Platform-wide setting rather than per-quiz, per the spec's assumption. The attempt row stores `score` and `total_questions` rather than a boolean-only verdict, so a later per-quiz pass mark can regrade historical attempts without a migration.

**Alternatives considered**:
- *Integer percentage setting* — rejected: invites exactly the rounding ambiguity above.

> **Revised during implementation.** This decision originally deferred a per-quiz pass mark as a future addition. That was wrong: `QuizAssetIn` in `app/schemas/training.py` **already** has `pass_mark_percent: int = Field(default=60, ge=0, le=100)`, so quizzes authored through the CMS may already carry their own mark, and ignoring it would silently override what an author set.
>
> Implemented behaviour: `pass_mark_for(config)` uses the asset's `pass_mark_percent` when present and in range, falling back to `settings.QUIZ_PASS_MARK`. Note the unit change — the stored field is a **percentage** (0-100) and the setting is a **fraction** (0-1); the conversion happens in one place, because mixing them makes every quiz either free or impossible. Non-numeric, boolean, and out-of-range values fall back rather than throwing, since this runs against already-authored content.

---

## D4. How gating is computed and enforced

**Decision**: The progress endpoint returns, per asset in the session's material, `{asset_id, is_quiz, passed, locked}` plus a `first_locked_index`. The client blocks forward navigation past `first_locked_index`. Backward navigation is never restricted.

**Rationale**: Server-computed because the client cannot be trusted with it and because the client does not have the pass mark. Returned as a list rather than a single index so the portal can render per-item completion state — a real LMS shows you the map, not just the wall.

Enforcement is a navigation guard, not an access-control boundary, and the plan should be honest about that: a determined student could still request a later asset's data directly. That is acceptable because the material is already published to them and they attended the session — gating here is a pedagogical sequencing tool, not a secrecy mechanism. The thing that genuinely must not leak, the answer key, is protected server-side by D1 regardless of navigation. If gating ever needs to be a real boundary, the materials endpoint would have to stop returning locked assets' payloads, which is a larger change and is not what was asked for.

**Alternatives considered**:
- *Withhold locked assets from the materials response* — rejected for now: makes gating airtight but complicates the pager, breaks the "Page N of M" count, and adds a round trip per unlock. Noted above as the upgrade path.
- *Client-side gating from attempt data alone* — rejected: client would need the pass mark and could be edited trivially.

---

## D5. Stale attempts after a quiz is edited

**Decision**: Store `total_questions` on the attempt. When it differs from the live asset's current question count, the trainer's results view marks that attempt stale. Scores are never retroactively regraded.

**Rationale**: The spec requires attempts keep their awarded score and be identifiable as taken against an earlier version. Full asset versioning would answer this properly but is far beyond scope. Question count is a cheap, no-migration-later proxy that catches the common edits — adding or removing questions. It does *not* catch a reworded question or a changed correct answer at the same count, and the data model documents that limitation rather than implying the check is complete.

A student who passed against an older version stays passed. Invalidating passes on edit would let a trainer fixing a typo silently re-lock material for students who had already moved on.

**Alternatives considered**:
- *Content hash of the questions blob* — stronger, catches reworded questions; rejected as the extra column and hashing discipline aren't justified before anyone has asked to detect that case. The upgrade is additive.
- *Full asset versioning* — correct long-term answer, disproportionate here.

---

## D6. Duplicate submission handling

**Decision**: A unique constraint on `(student_id, asset_id, attempt_number)` where `attempt_number` is assigned server-side from the count of existing attempts. The client also disables submit while a request is in flight.

**Rationale**: The spec requires a double-clicked submit to record one attempt. Client-side disabling alone is not sufficient — two tabs, or a retried request, defeat it. The DB constraint is the actual guard, matching how `SessionPollVote` already uses a unique constraint as the double-vote guard rather than trusting client state. That precedent is worth following for consistency.

**Alternatives considered**:
- *Idempotency key from the client* — rejected: more moving parts, and the natural key here is already sufficient.
- *Time-window dedupe (ignore submissions within N seconds)* — rejected: arbitrary, and would wrongly reject a genuinely fast legitimate retry.

---

## D7. Trainer results surface

**Decision**: New route on `app/api/v1/endpoints/trainer_reports.py`, following its existing `/sessions/{id}/polls/history` shape and reusing its `_assert_owns_batch` guard.

**Rationale**: That module already exists for exactly this — read-only reports over a session, with batch-ownership access control and an admin-sees-all carve-out. Its docstring notes it was split from `trainer.py` so reporting features could land without touching that file. Quiz results are the same kind of thing.

Results include roster students with **no** attempt, per FR-020 — the pedagogically useful signal is usually who hasn't engaged, which a query over attempts alone would omit. That means starting from the batch roster and left-joining attempts, not the reverse.

**Alternatives considered**:
- *Extend the poll-history endpoint* — rejected: different entity, different shape, and conflating them makes both harder to evolve.
- *New standalone module* — rejected: `trainer_reports.py` is the right home and is not yet large.

---

## D8. Testing approach

**Decision**: Unit tests for the grading service covering the boundary arithmetic (2/3 fails at 0.7, 7/10 passes, 0/0 passes) and malformed submissions. Integration tests asserting the student materials response contains no `correct_index` or `explanation` for a quiz, that the trainer response still does, and that gating blocks then unblocks.

**Rationale**: The redaction assertion is the single most valuable test in the feature — it is the regression guard that makes D1's unredacted default safe, and it fails loudly if a future student-facing call site forgets to pass the audience. The boundary cases are where a plausible implementation is most likely to be quietly wrong.
