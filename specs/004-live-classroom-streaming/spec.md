# Feature Specification: Live Classroom Audio/Video Streaming

**Feature Branch**: `004-live-classroom-streaming`

**Created**: 2026-07-18

**Status**: Draft

**Input**: User description: "implement this as live audio and video while start session- make sure end user can join the classroom there can see video in right place also listen audio. Reference guide: CLASSROOM-WEBAPP-GUIDE.md. Every step should be tested"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Teacher Starts a Live Session and Students Watch in Real Time (Priority: P1)

A teacher opens their class dashboard and starts a live session. Their camera and microphone activate and their live video/audio begins broadcasting. Enrolled students who have the classroom page open see the teacher's video appear in the designated video area of the page and hear the matching audio, with no manual refresh needed.

**Why this priority**: This is the core value of the feature — without a working live broadcast that students can reliably see and hear, no other capability matters. This is the minimum viable product.

**Independent Test**: Can be fully tested by having a teacher account start a session while a student account has the classroom page open, and confirming the student's video area shows live video and speakers/headphones produce synchronized audio within a few seconds of the teacher going live.

**Acceptance Scenarios**:

1. **Given** a teacher is on their class dashboard and not currently broadcasting, **When** the teacher clicks "Start Session", **Then** the system begins capturing the teacher's camera and microphone and the teacher sees their own live preview.
2. **Given** a teacher has started a live session, **When** an enrolled student opens the classroom page, **Then** the student sees the teacher's live video rendered in the designated classroom video area and hears the corresponding live audio.
3. **Given** a student is watching a live session, **When** the teacher speaks and moves on camera, **Then** the student's audio and video stay in sync with no perceptible drift.
4. **Given** a student opens the classroom page before the teacher has started the session, **When** the page loads, **Then** the student sees a clear "session not started yet" state instead of a broken or blank video player.

---

### User Story 2 - Teacher Controls Audio, Video, and Screen Share During the Session (Priority: P2)

While a session is live, the teacher can mute/unmute their microphone, turn their camera on or off, and switch between webcam and screen-share presentation. Every change is reflected for all watching students within a couple of seconds.

**Why this priority**: Teachers need in-session control to run an effective class (e.g., muting during silence, presenting slides), but the class can still function at a basic level without it, so it ranks below the core broadcast capability.

**Independent Test**: Can be fully tested by starting a live session, toggling mute/camera/screen-share from the teacher's controls, and confirming each state change is reflected on a connected student's view within a couple of seconds.

**Acceptance Scenarios**:

1. **Given** a live session with audio on, **When** the teacher mutes their microphone, **Then** students stop hearing the teacher's audio while the video keeps playing.
2. **Given** a live session with video on, **When** the teacher turns off their camera, **Then** students see a clear "camera off" state instead of a frozen or broken video frame.
3. **Given** a live session using the webcam, **When** the teacher starts screen sharing, **Then** students' video area switches to the shared screen content while audio continues uninterrupted.
4. **Given** the teacher is screen sharing, **When** the teacher stops sharing (via in-browser control or app control), **Then** students' video area automatically switches back to the teacher's webcam.
5. **Given** a live session, **When** the teacher clicks "End Session", **Then** the broadcast stops for all students and each student's video area shows a clear "session ended" state.

---

### User Story 3 - Absent Students Watch a Recorded Replay (Priority: P3)

A student who could not attend the live session opens the classroom page after class and watches a recorded replay of the session, with the same video-in-the-right-place and synchronized-audio experience as the live view.

**Why this priority**: Valuable for accessibility and makeup learning, but it depends on the live session (P1) having happened and is not required for the initial live-class experience to deliver value.

**Independent Test**: Can be fully tested by completing a live session, waiting for the replay to become available, and confirming a student account can open and play it back with working video and audio.

**Acceptance Scenarios**:

1. **Given** a live session has ended, **When** the replay becomes available, **Then** an enrolled student can find and open the replay from the classroom page.
2. **Given** a student opens an available replay, **When** playback starts, **Then** video renders in the same designated video area and audio is audible and in sync.
3. **Given** a session has ended but the replay is still processing, **When** a student opens the classroom page, **Then** the student sees a clear "replay processing" state rather than an error.

---

### Edge Cases

- What happens when a student's network blocks the primary low-latency delivery method? The system must fall back to an alternate playback method so the student can still see and hear the class.
- What happens if the teacher's connection drops mid-session? Students should see a clear "reconnecting" or "session interrupted" state rather than a frozen frame with no explanation, and the teacher's app should attempt to resume the same session if reconnected within a short window.
- How does the system handle a student attempting to access a class they are not enrolled in? Access must be denied and no video/audio delivered.
- How does the system handle a browser/device that does not support live playback? The student must see a clear compatibility message rather than a silent failure.
- What happens when two teachers for the same class both attempt to start a session simultaneously? The system must prevent duplicate concurrent broadcasts for the same class.
- What happens when a student joins partway through a live session? The student must immediately see current live video/audio, not be forced to wait for the next segment or replay from the start.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow an authenticated teacher to start a live session for a class they are assigned to teach.
- **FR-002**: System MUST issue each class session a unique, non-guessable access path so only users who received it from the system can publish or view the broadcast.
- **FR-003**: System MUST capture the teacher's live camera video and microphone audio and transmit them to the classroom in real time once a session starts.
- **FR-004**: System MUST render the live video in the designated video display area of the student's classroom page.
- **FR-005**: System MUST play the live audio in sync with the video so students can hear the class as it happens.
- **FR-006**: System MUST restrict live viewing and publishing to authenticated users enrolled in (or teaching) that specific class.
- **FR-007**: Teacher MUST be able to mute/unmute their microphone during a live session, and the change must be reflected for watching students.
- **FR-008**: Teacher MUST be able to turn their camera on/off during a live session, and the change must be reflected for watching students.
- **FR-009**: Teacher MUST be able to switch the broadcast between webcam and screen-share, and back, during a live session.
- **FR-010**: Teacher MUST be able to end a live session, which stops the broadcast for all currently watching students.
- **FR-011**: System MUST show students a clear status state when: no session is live yet, the session has ended, or the connection is interrupted — rather than a blank or broken player.
- **FR-012**: System MUST provide a fallback playback method for students on networks that block the primary low-latency delivery method.
- **FR-013**: System MUST automatically record each live session for later replay.
- **FR-014**: System MUST make a processed replay available to enrolled students who did not attend the live session.
- **FR-015**: System MUST prevent a class from having more than one active live session running at the same time.
- **FR-016**: Each user-facing capability defined in this specification (starting a session, joining and viewing a live session, hearing audio, teacher controls, ending a session, and replay playback) MUST be verified against its acceptance scenarios before the feature is released.

### Key Entities

- **Class Session**: Represents one live broadcast instance of a class. Key attributes: associated class, teacher, status (not started / live / ended), start time, end time.
- **Session Participant**: Represents a user connected to a class session as either broadcaster (teacher) or viewer (student), including their role and connection status.
- **Recording**: Represents the captured video/audio of a completed class session, including processing status (processing / ready) and availability to enrolled students for replay.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A student who has the classroom page open sees the teacher's live video and hears synchronized audio within 5 seconds of the teacher starting the session.
- **SC-002**: During a live session, audio and video remain synchronized (no perceptible lag) for at least 95% of a typical 45-minute class.
- **SC-003**: A teacher can start a live session, with camera/mic active and visible to students, in under 15 seconds from clicking "Start Session".
- **SC-004**: 100% of unauthorized access attempts (unauthenticated users or users not enrolled in the class) are unable to view or publish to a session during testing.
- **SC-005**: Every acceptance scenario defined in this specification passes verification testing before the feature is considered complete.
- **SC-006**: Students on networks that block the primary delivery method can still watch the class via the fallback method within 10 seconds of joining.
- **SC-007**: At least 90% of students who missed a live session can successfully play back the replay once it is marked available.

## Assumptions

- Teachers and students are already authenticated through the platform's existing login system before reaching the classroom page; this feature does not introduce a new login mechanism.
- "Enrolled students" means users the platform already associates with a given class through existing class/roster data.
- A typical class size (up to ~100 concurrent student viewers per session) is sufficient for initial scope; very large lecture-hall scale is out of scope for v1.
- Recording retention and storage lifecycle follow the platform's existing media storage practices; no new retention policy is introduced by this feature.
- "Every step should be tested" is interpreted as: every acceptance scenario in this specification must be manually or automatically verified end-to-end (teacher publishing, student viewing video in the correct area, student hearing audio, controls, session end, and replay) before this feature ships.
- Mobile browser support follows the same acceptance criteria as desktop browsers; no separate native mobile app is in scope.
