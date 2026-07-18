# Feature Specification: Audio-Only Presentation Mode

**Feature Branch**: `[005-audio-only-presentation]`

**Created**: 2026-07-18

**Status**: Draft

**Input**: User description: "allow feature if trainer wants to go with audio only no video no screen shareing or screen sharing."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Present with Audio Only (Priority: P1)

As a trainer, I want to present using only my microphone without video or screen sharing, so that I can conserve bandwidth, maintain privacy, or present in low-light conditions.

**Why this priority**: Core request from the user. Enables lower-bandwidth sessions and more flexible presentation styles.

**Independent Test**: Can be fully tested by launching a classroom session, turning off the camera, turning off screen sharing, and confirming the microphone is still active and transmitting audio to students.

**Acceptance Scenarios**:

1. **Given** a trainer is in a live session, **When** they toggle their camera off and do not share their screen, **Then** their audio continues to broadcast to the classroom.
2. **Given** a trainer is presenting audio-only, **When** a student joins the classroom, **Then** the student hears the trainer's audio and sees an "Audio Only" or "Camera Off" placeholder instead of a black video feed.

---

### User Story 2 - Toggle Video/Screen Share Mid-Session (Priority: P2)

As a trainer, I want to be able to seamlessly switch between audio-only, video, and screen sharing during a live session, so that I can adapt my presentation style dynamically.

**Why this priority**: Essential for a smooth user experience. Trainers often need to turn off video temporarily while presenting or switch to a screen share.

**Independent Test**: Can be tested by starting a session with video, turning video off (audio only), then starting a screen share, and turning video back on.

**Acceptance Scenarios**:

1. **Given** a trainer is presenting with video, **When** they turn off the camera, **Then** the video feed stops, the audio continues, and students see a placeholder.
2. **Given** a trainer is presenting audio-only, **When** they initiate a screen share, **Then** the screen share replaces the placeholder and audio continues.

### Edge Cases

- What happens when a trainer starts a session with no camera permissions granted? (The system should default to audio-only mode if microphone permission is granted).
- How does the system handle a trainer inadvertently turning off their microphone while in audio-only mode? (The system should clearly warn the trainer that they are completely muted and no longer broadcasting media).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow trainers to toggle their camera on and off during a live session without disconnecting the audio stream.
- **FR-002**: System MUST allow trainers to present with only a microphone active (no camera, no screen share).
- **FR-003**: System MUST display a visual indicator or placeholder (e.g., trainer avatar or "Camera Off" message) to students when the trainer's video and screen share are both inactive.
- **FR-004**: System MUST maintain the media connection state when media tracks (video/screen) are added or removed dynamically.
- **FR-005**: System MUST clearly indicate to the trainer that they are live and broadcasting audio, even when their camera is off.

### Key Entities

- **Classroom Session**: Represents the active live event. Needs state to indicate which media streams (audio, video, screen) are currently active for the trainer.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Trainers can successfully conduct a 30-minute session using only audio without the connection dropping.
- **SC-002**: Toggling video on/off takes less than 2 seconds to reflect on the student's end.
- **SC-003**: Bandwidth usage for audio-only sessions is significantly lower (by at least 70%) compared to video sessions.

## Assumptions

- Users have stable internet connectivity.
- The underlying media streaming infrastructure supports dynamic track addition/removal.
- When a trainer's camera is off, a generic avatar or static text placeholder is sufficient for the student view.
