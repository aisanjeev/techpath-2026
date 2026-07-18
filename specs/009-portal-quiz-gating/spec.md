# Feature Specification: Graded Quiz Attempts and Progress Gating

**Feature Branch**: `[009-portal-quiz-gating]`

**Created**: 2026-07-18

**Status**: Draft

**Input**: User description: "if any assets has quiz and while showing to trainer session and on students, currently looks not functional, it should be that students can test live like polls, submit like this and real time trainer can see result from roaster, also while giving material, once user will check from portal, that time also quiz should be function to proceed further. like real lms panel"

## Context

Quiz lecture assets already exist in the content library, and trainers can already push a single quiz question into the live classroom as a real-time poll (delivered in feature 007). What does not exist is any way for a student to *answer* a quiz as a quiz — during class or afterwards in the portal — and nothing records whether a student has understood the material.

Today a quiz asset renders as a static, unclickable list of questions on the student side, while the answer key for every question is sent to the student's browser along with it. This feature makes quizzes answerable, grades them on the server, and uses the result to gate a student's progression through published material.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Answer Key Is Never Given to Students (Priority: P1)

A student opens any quiz — in the live classroom or in the portal — and receives only the questions and the answer options. The correct answer and its explanation are not present anywhere in what their browser receives until they have submitted an attempt.

**Why this priority**: Every other story in this feature is meaningless while the answer key ships to the client — a graded quiz whose answers can be read from the browser measures nothing. This is also a live data-exposure problem on already-published material, so it has value the moment it ships, independent of grading.

**Independent Test**: Sign in as a student, open a session's materials containing a quiz, and inspect the raw response the browser receives. No correct-answer marker or explanation appears for any question. Repeat as a trainer and confirm both are still present.

**Acceptance Scenarios**:

1. **Given** a published quiz asset with correct answers and explanations, **When** a student requests that session's materials, **Then** each question carries its text and options but no correct-answer indicator and no explanation.
2. **Given** the same asset, **When** a trainer or admin requests it for presenting or editing, **Then** the correct answers and explanations are present and unchanged.
3. **Given** a student viewing an asset during a live session, **When** the trainer displays a quiz slide, **Then** the student's copy of that asset also excludes the answer key.

---

### User Story 2 - Student Takes and Submits a Graded Quiz (Priority: P1)

A student working through published material reaches a quiz. They select an answer for each question and submit. The system grades the submission and immediately shows them their score, which questions they got right and wrong, and the explanation for each. If they did not reach the pass mark they can retake the quiz as many times as they need.

**Why this priority**: This is the core of the request — the quiz becoming functional rather than decorative. Together with Story 1 it forms the minimum viable feature: a quiz a student can actually take and be scored on.

**Independent Test**: As a student, open a quiz in the portal, answer every question, submit, and confirm a score and per-question feedback appear. Retake it and confirm a second, independent result is produced.

**Acceptance Scenarios**:

1. **Given** a quiz with unanswered questions, **When** the student attempts to submit, **Then** submission is refused and the unanswered questions are indicated.
2. **Given** a fully answered quiz, **When** the student submits, **Then** a score, a pass/fail outcome, and per-question correct/incorrect feedback with explanations are returned.
3. **Given** a student who scored below the pass mark, **When** they choose to retry, **Then** the quiz is presented fresh with no answers preselected and their previous attempt remains on record.
4. **Given** a student who has already passed, **When** they reopen the quiz, **Then** their best result is shown along with the option to take it again.
5. **Given** a submission containing an answer for a question that does not exist on the quiz, **When** it is submitted, **Then** the submission is rejected rather than partially graded.

---

### User Story 3 - Quiz Gates Progress Through Material (Priority: P2)

A student moving page by page through a session's published material cannot advance past a quiz until they have passed it. The material list shows them which items they have completed and which remain locked, so they always know where they stand.

**Why this priority**: This is what makes the portal behave like a real LMS rather than a document viewer. It depends on Story 2 existing, so it follows it — but Story 2 is genuinely useful on its own even ungated.

**Independent Test**: As a student, open material containing a quiz partway through, attempt to advance past the quiz without passing it, and confirm advancement is blocked. Pass the quiz and confirm the next item becomes reachable.

**Acceptance Scenarios**:

1. **Given** a student on a quiz page with no passing attempt, **When** they try to move to the next item, **Then** advancement is blocked and the reason is explained.
2. **Given** the same student, **When** they submit a passing attempt, **Then** the next item becomes immediately reachable without reloading.
3. **Given** a student on a quiz page, **When** they move backwards to an earlier item, **Then** they are always allowed to — gating restricts forward progress only.
4. **Given** a student returning in a new visit after passing a quiz, **Then** that quiz remains passed and everything they had unlocked is still unlocked.
5. **Given** material with no quiz in it, **When** a student pages through it, **Then** nothing is gated and every item is reachable.

---

### User Story 4 - Trainer Sees Who Passed (Priority: P3)

A trainer looks at a session's report and sees, for each quiz in the material, how their students performed — who has passed, who has attempted without passing, who has not attempted at all, and the score distribution across questions so they can spot a concept the group as a whole missed.

**Why this priority**: Valuable for the trainer but not required for a student to be able to take a quiz. It reads data the earlier stories produce, so it is naturally last.

**Independent Test**: With at least two students having submitted attempts, open the session report as their trainer and confirm each student's status and score appear, and that a student from another trainer's batch does not.

**Acceptance Scenarios**:

1. **Given** several students have attempted a quiz, **When** their trainer opens the session report, **Then** each roster student appears with their best score and pass status, including those who never attempted.
2. **Given** a session belonging to a different trainer's batch, **When** a trainer requests its quiz results, **Then** access is refused.
3. **Given** a quiz where most students missed the same question, **When** the trainer views the results, **Then** the per-question success rate makes that visible.

---

### Edge Cases

- A trainer edits a quiz's questions after students have already submitted attempts — existing attempts keep the score they were awarded at the time and are not retroactively regraded, and are marked as having been taken against an earlier version of the quiz.
- A quiz asset contains zero questions — it is treated as having nothing to pass and never blocks progress.
- A student submits the same attempt twice in quick succession (double-clicked submit) — only one attempt is recorded.
- A quiz appears in material for a session the student did not attend, or that has not been published — the student cannot see or attempt it at all.
- Two questions where the pass mark falls between whole questions (e.g. 3 questions at a 70% pass mark) — the threshold is applied so that the student must meet or exceed it, not merely approach it.
- A student loses connectivity mid-quiz before submitting — their in-progress selections are not preserved and they start the attempt over; no partial attempt is recorded.
- Material is republished with a new asset added before a quiz the student had already passed — the passed quiz stays passed.

## Requirements *(mandatory)*

### Functional Requirements

**Answer key protection**

- **FR-001**: System MUST exclude the correct-answer indicator and the explanation from every quiz question sent to a student, on every student-facing surface.
- **FR-002**: System MUST continue to provide correct answers and explanations to trainers and administrators for presenting, reviewing, and editing.
- **FR-003**: System MUST reveal a question's correct answer and explanation to a student only in the response to that student's own submitted attempt.

**Taking a quiz**

- **FR-004**: Students MUST be able to select exactly one option per question and change that selection freely before submitting.
- **FR-005**: System MUST refuse a submission that does not answer every question, identifying which are missing.
- **FR-006**: System MUST grade every submission on the server against the stored answer key; a client-supplied score MUST never be trusted.
- **FR-007**: System MUST return, for each question, whether the student's answer was correct, which option was correct, and the explanation.
- **FR-008**: System MUST record every submitted attempt with the student, the quiz, the session, the submitted answers, the resulting score, the pass outcome, and the time of submission.
- **FR-009**: Students MUST be able to reattempt a quiz an unlimited number of times, with each attempt recorded separately.
- **FR-010**: System MUST treat an attempt as passing when the proportion of correct answers meets or exceeds the pass mark, which defaults to 70% and MUST be configurable without a code change.
- **FR-011**: System MUST reject a submission referencing a question or option that does not exist on the quiz.
- **FR-012**: System MUST ensure a duplicate submission of the same attempt records only one attempt.

**Progress and gating**

- **FR-013**: System MUST tell the portal, for a session's material, which items the student has completed and which are locked.
- **FR-014**: System MUST prevent a student from advancing past a quiz item until they have a passing attempt on it.
- **FR-015**: System MUST allow backward navigation to any previously reachable item at all times.
- **FR-016**: System MUST unlock the following item immediately upon a passing submission, without the student reloading.
- **FR-017**: System MUST persist unlocked progress across visits and devices for the same student.
- **FR-018**: System MUST treat non-quiz items as never blocking progress.
- **FR-019**: System MUST explain to the student why a locked item is locked and what to do about it.

**Trainer visibility**

- **FR-020**: Trainers MUST be able to see, per quiz in a session, each roster student's best score and pass status, including students with no attempt.
- **FR-021**: Trainers MUST be able to see the per-question success rate across the group for a quiz.
- **FR-022**: System MUST restrict quiz results to trainers who own the batch the session belongs to.

**Access control**

- **FR-023**: System MUST permit a student to view or attempt a quiz only for a session they attended and whose material has been published.

### Key Entities

- **Quiz Attempt**: One student's submission of one quiz on one session — the answers they gave, the score awarded, whether it passed, and when. Immutable once recorded; a retry creates a new one.
- **Quiz Asset**: An existing lecture asset holding a set of questions, each with options, one correct option, and an optional explanation. Unchanged by this feature apart from how it is exposed.
- **Student Progress**: The derived view of which material items a given student has completed and which remain locked for a session. Determined by their attempts rather than stored independently.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: No correct answer or explanation is present in any data a student's browser receives before they submit, verified across both the live classroom and the portal.
- **SC-002**: A student can complete and submit a five-question quiz in under two minutes, seeing their score immediately on submission.
- **SC-003**: 100% of submissions are scored on the server; no submission's score can be altered from the client.
- **SC-004**: A student who has not passed a quiz cannot reach any material item beyond it, in 100% of attempts.
- **SC-005**: A student who passes a quiz sees the next item become available without any manual refresh.
- **SC-006**: A trainer can determine, for any quiz in their session, which students have passed and which question the group most often got wrong, within 30 seconds of opening the report.
- **SC-007**: Students returning in a later visit find their previously passed quizzes still passed, in 100% of cases.
- **SC-008**: Existing material without quizzes remains navigable exactly as before, with no new restrictions.

## Assumptions

- The existing live-poll flow delivered in feature 007 stays as it is; a trainer pushing a single quiz question to the room as a real-time poll remains the live mechanism, and this feature does not replace it. The graded-quiz path added here is complementary and works both in class and afterwards.
- Quiz questions are single-select with exactly one correct option, matching how quiz assets are authored today. Multi-select, free-text, and partial credit are out of scope.
- Question order and option order are presented as authored; randomisation is out of scope.
- Quizzes are untimed. A per-quiz time limit is out of scope.
- The pass mark is a single platform-wide setting rather than per-quiz or per-batch. Per-quiz pass marks are a plausible later addition and the recorded attempt data supports adding them without migration.
- Gating applies to the portal's sequential material view. It does not restrict a student during a live session, where the trainer controls what is on screen.
- Students are identified by the existing portal sign-in; attempts belong to a roster student, and guests who joined a live session by code without being on a roster cannot accumulate graded attempts.
- Attempts are retained for the life of the session record and removed with it.
- The trainer-facing results view follows the existing session report surface that already reports poll results, rather than introducing a separate destination.
- The admin content editor for authoring quizzes is unchanged, as is the trainer presenter's own view of a quiz slide — the latter still showing the answer key to the trainer is tracked separately.
