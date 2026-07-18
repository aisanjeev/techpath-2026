# Feature Specification: Student Speaker Control

**Feature Branch**: `[010-student-speaker-control]`

**Created**: 2026-07-18

**Status**: Draft

**Input**: User description: "read this "C:\Users\Techpath\Documents\MULTI-SPEAKER-GUIDE.md", trainer should have option to enable student to speak. want a good and stable user experience"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Raise Hand and Teacher Approval (Priority: P1)

A student can indicate they want to speak by raising their hand. The trainer can see this request and choose to approve it, allowing the student's microphone to be broadcast to the trainer.

**Why this priority**: This is the core functionality requested by the user, providing controlled two-way audio for doubts without interrupting the main broadcast.

**Independent Test**: Can be fully tested by a trainer and student in the same classroom session. The student raises their hand, the trainer approves, and the student's audio becomes audible to the trainer.

**Acceptance Scenarios**:

1. **Given** a student is in a live classroom, **When** they click "Raise Hand", **Then** the trainer receives a notification that the student wants to speak.
2. **Given** a student has raised their hand, **When** the trainer clicks "Enable Audio" for that student, **Then** the student is notified they can speak and their microphone is activated.
3. **Given** the student's microphone is active, **When** they speak, **Then** the trainer can hear their audio.
4. **Given** the student is speaking, **When** the trainer or student clicks "Mute/Stop", **Then** the student's audio broadcast ends.

---

### User Story 2 - Managing Multiple Doubts (Priority: P2)

The trainer needs a clear and stable UI to manage multiple students who might want to speak at the same time or sequentially.

**Why this priority**: A "good and stable user experience" requires handling more than one concurrent doubt gracefully without overwhelming the trainer or breaking the stream.

**Independent Test**: Can be tested by having multiple mock students raise their hands, and the trainer managing the queue of speakers.

**Acceptance Scenarios**:

1. **Given** multiple students have raised their hands, **When** the trainer views the classroom dashboard, **Then** they see a clear list or queue of students waiting to speak.
2. **Given** one student is currently speaking, **When** the trainer enables audio for a second student, **Then** both students can be heard by the trainer (or they can manage who is actively broadcasting).

### Edge Cases

- What happens when a student loses internet connection while their microphone is live?
- How does the system handle the trainer ignoring or dismissing a raised hand?
- What happens if the student's browser denies microphone permissions after the trainer approves the request?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow students to virtually "raise their hand" during a live session.
- **FR-002**: System MUST notify the trainer in real-time when a student raises their hand.
- **FR-003**: System MUST provide the trainer with a control to "enable" or "approve" a student's request to speak.
- **FR-004**: System MUST activate the student's microphone and publish their audio stream to a unique path when approved by the trainer.
- **FR-005**: System MUST automatically subscribe the trainer's browser to the approved student's audio stream.
- **FR-006**: System MUST provide the trainer with a control to revoke a student's speaking permission (mute them).
- **FR-007**: System MUST provide visual feedback to both the student (e.g., "Mic Live") and the trainer (e.g., "Student X is speaking") while the audio is active.

### Key Entities

- **Classroom Session**: The live event where the broadcast occurs.
- **Doubt Request**: A record indicating a specific student wants to speak at a specific time in a specific session.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Trainers can successfully approve and hear a student's audio within 3 seconds of clicking "Enable Audio".
- **SC-002**: Audio streams from students to trainers maintain less than 500ms latency to ensure natural conversation.
- **SC-003**: 95% of student doubt sessions are completed without stream drops or necessity to refresh the browser.
- **SC-004**: Trainers report high satisfaction (>= 4/5) with the ease of managing student audio requests during a live class.

## Assumptions

- Students have a working microphone and have granted browser permissions to use it.
- The underlying infrastructure uses MediaMTX with unique paths per student as outlined in the multi-speaker guide.
- The classroom uses a real-time signaling mechanism (e.g., WebSockets) to coordinate "Raise Hand" and "Approve" actions between trainer and student.
- The student's audio is only routed to the trainer, not re-broadcasted to all other students (as per the guide's Scenario A).
