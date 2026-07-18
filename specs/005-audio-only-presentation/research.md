# Research: Audio-Only Presentation Mode

## Context
The goal is to allow a trainer to present in a live classroom session with only their microphone, turning off their camera and screen sharing. The students should see an "Audio Only" or "Camera Off" placeholder while still hearing the trainer.

## Finding 1: Student Frontend Capability
**Decision**: Reuse the existing `camera_off` state on the student frontend.
**Rationale**: `ClassroomVideoTile.jsx` in `techpath-frontend` already contains logic to render a `Camera off` placeholder overlay when `media.camera_off === true`. It also conditionally sets the `<video>` element to `invisible`. Thus, the student frontend is already 100% capable of handling an audio-only stream presentation if the backend tells it so.
**Alternatives considered**: Building a brand new "AudioTile" component. This was rejected because the existing WHEP peer connection can simply carry an audio-only track without video tracks if renegotiated properly, and the existing UI handles the visual placeholder already.

## Finding 2: Trainer UI Publisher Control
**Decision**: The Admin Dashboard (trainer view) needs explicit controls to disable the camera track in their local `RTCPeerConnection` (WHIP) or mute the video track, and it must notify the backend of this state change.
**Rationale**: The `media_state_changed` event is defined in `classroom.ts`, meaning the backend supports broadcasting this state. The work will primarily be in the `techpath-admin` app where the trainer publishes their stream. When the trainer toggles video off, the app must call the backend API (e.g., `PATCH /api/v1/classroom/sessions/{id}/media`) to update `camera_off=true`, and also disable the video track on the WebRTC connection.

## Finding 3: Media Server Compatibility
**Decision**: Media track toggling must rely on track muting (`track.enabled = false`) or WHIP renegotiation (removing the track).
**Rationale**: Muting the track (`track.enabled = false`) keeps the WHEP connection stable for students (it just sends black frames or stops sending RTP packets for video). The frontend overlay handles the visual aspect. This avoids breaking the WHEP connection entirely.
