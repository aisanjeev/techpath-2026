# Feature Specification: Live Questions

**Feature Branch**: `[007-live-questions]`

**Created**: 2026-07-18

**Status**: Draft

**Input**: User description: "there is a gap, students are attending class, but they have anydoubt, they can't speak right, then add some feature like live question, but should be easy for students, and also good symbol."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a Live Question (Priority: P1)

As a student attending a live class, I want to click a simple, recognizable icon (e.g., a "?") to type and submit a question without interrupting the trainer's audio/video flow.

**Why this priority**: Students currently have no simple way to raise a doubt if they are muted. This is the core capability that enables interactive Q&A during a session.

**Independent Test**: Can be fully tested by a student joining a live session, clicking the question button, typing text, and submitting. The feature delivers value immediately by bridging the communication gap.

**Acceptance Scenarios**:

1. **Given** a student is in an active live session, **When** they click the "Ask Question" (?) button, **Then** a small modal or input area appears allowing them to type their question.
2. **Given** the student has typed a question, **When** they submit it, **Then** the question is sent to the server and they see a confirmation that their question was submitted.

---

### User Story 2 - Trainer Views and Manages Questions (Priority: P1)

As a trainer presenting a live class, I want to see incoming student questions in a dedicated list and be able to mark them as "Answered" once I have addressed them verbally.

**Why this priority**: If students can ask questions but the trainer can't see them or track which ones were answered, the loop is broken.

**Independent Test**: Can be tested by having a trainer view the Classroom Panel, observing incoming questions from students, and clicking a button to mark a question as answered.

**Acceptance Scenarios**:

1. **Given** a student has submitted a question, **When** the trainer looks at their Classroom Panel, **Then** they see the question with the student's name in a Q&A list.
2. **Given** the trainer has verbally answered the question, **When** they click "Mark Answered", **Then** the question is visually distinct or removed from the active list.

---

### Edge Cases

- What happens when a student submits an empty question or extremely long text?
- How does the system handle rapid, repeated question submissions from the same student (spam)?
- What happens if the student disconnects and reconnects? Do they see their previously asked questions?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a UI button with a clear, universally recognized symbol (like `?`) for students to open the question input.
- **FR-002**: System MUST allow students to submit text-based questions during a live session.
- **FR-003**: System MUST enforce a reasonable character limit on questions to prevent abuse (e.g., 500 characters).
- **FR-004**: System MUST display submitted questions in real-time to the trainer's Classroom Panel via WebSocket.
- **FR-005**: System MUST allow the trainer to mark a question as "Answered".
- **FR-006**: System MUST allow the trainer to toggle whether questions are public (visible to all students) or private (only visible to the trainer).
- **FR-007**: System MUST allow students to upvote public questions, which helps the trainer prioritize them.
- **FR-008**: System MUST save all questions permanently so the trainer can review them post-class.

### Key Entities *(include if feature involves data)*

- **SessionQuestion**: Represents a question asked by a student during a live session. Attributes include the session ID, student ID, the question text, timestamp, and a boolean `is_answered` flag.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can discover and submit a question in under 15 seconds.
- **SC-002**: The trainer receives the incoming question in the UI in under 1 second of submission.
- **SC-003**: 95% of trainers successfully identify and mark questions as answered during the session.

## Assumptions

- Students have a stable WebSocket connection to receive/send live events.
- The UI will be designed to not obstruct the main video or slide presentation area.
- The backend will use the existing `bus` (Classroom Broadcaster) to push question events.
