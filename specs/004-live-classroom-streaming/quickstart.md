# Quickstart: Validating Live Classroom Audio/Video

This is a run/validation guide, not an implementation guide — it maps directly to the acceptance scenarios in [spec.md](./spec.md) and exists to satisfy FR-016/SC-005 ("every step tested before release"). Re-run this checklist after implementation and again before each release that touches the classroom feature.

## Prerequisites

- `techpath-backend` running locally (`poetry run uvicorn app.main:app --reload`) with `LIVE_MEDIA_BASE_URL` and `WATCH_SERVICE_BASE_URL` set in `.env.local` (point at the real `live.techpath.biz` / `watch.techpath.biz` for a true end-to-end check; a local MediaMTX instance is an acceptable substitute for iterating quickly, but the final pre-release pass must hit the real hosts).
- `techpath-admin` running locally (`npm run dev`, port 3000), signed in as a trainer account assigned to at least one batch with a scheduled `TrainingSession`.
- `techpath-frontend` running locally (`npm run dev`, port 4321).
- Two separate browsers or browser profiles (or one desktop + one mobile device) so the "trainer" and "student" roles don't share cookies/localStorage.
- A webcam and microphone available to the trainer machine (or a virtual camera/mic if testing headless).

## Scenario walkthrough (maps to spec.md User Stories 1–3)

### 1. Teacher starts a live session and students watch in real time (P1)

1. As the trainer, open the session's presenter page and click **Start Session**.
   - **Expect**: within 15s (SC-003), the page shows the trainer's own camera preview and the session flips to `live`.
2. As the student, open the classroom page and enter the join code.
   - **Expect**: within 5s of step 1 completing (SC-001), the student's designated video area shows the trainer's live video, and audio is audible through the student device's speakers/headphones.
3. Speak and move on camera as the trainer for at least 60 seconds.
   - **Expect**: audio and video stay in sync for the student throughout (SC-002) — no drift, no stutter beyond brief, self-correcting buffering.
4. Before starting the session (i.e., repeat with a fresh session still `scheduled`), open the student classroom page.
   - **Expect**: a clear "session not started yet" state, not a blank/broken player.

### 2. Teacher controls audio, video, and screen share (P2)

5. With the session live, click **mute** on the trainer side.
   - **Expect**: student stops hearing audio within a couple of seconds; video keeps playing.
6. Click **camera off**.
   - **Expect**: student sees a clear "camera off" placeholder, not a frozen frame.
7. Click **share screen**, select a window/tab.
   - **Expect**: student's video area switches to the shared screen; audio (if unmuted) continues uninterrupted.
8. Click **stop sharing** (both via the app control and via the browser's native "Stop sharing" banner, tested separately).
   - **Expect**: both paths return the student's view to the trainer's webcam automatically.
9. Click **End Session**.
   - **Expect**: broadcast stops for the student, whose screen shows a clear "session ended" state; the trainer's own preview also stops.

### 3. Absent students watch a recorded replay (P3)

10. After ending a session that had live media, poll `GET /trainer/sessions/{id}/recording` (or the presenter page's recording status indicator) until `status` is `ready`.
    - **Expect**: reaches `ready` in a reasonable time (minutes, not hours) for a short test recording.
11. As a student who did **not** join the live session, open the classroom/materials portal after the trainer publishes materials.
    - **Expect**: the replay is discoverable and, once opened, plays back with working video and audio in the same designated area as live viewing (SC-007).
12. Open the classroom/materials page while the recording is still `processing`.
    - **Expect**: a clear "replay processing" state, not an error.

## Edge cases to check explicitly

- **Network fallback (FR-012/SC-006)**: block WebRTC/UDP on the student's network (e.g. via browser devtools throttling/blocking, or an actual restrictive network) and confirm the HLS fallback (`hls.js`) picks up playback within 10s.
- **Unauthorized access (FR-006, SC-004)**: attempt to fetch `GET /classroom/{id}/state` and the trainer's WHIP-URL endpoint without a valid token/session ownership — confirm both are rejected and no media URL is ever returned.
- **Duplicate concurrent session (FR-015)**: attempt to start a second live session for a batch that already has one live — confirm it's rejected or reuses the existing live session rather than producing two simultaneous broadcasts.
- **Trainer reconnect**: kill the trainer's network mid-session for under the reconnect window, then restore it — confirm the same session resumes rather than requiring a brand-new "Start Session".
- **Student joins mid-session**: join partway through a live broadcast — confirm the student immediately sees current live video, not a wait state or a replay from the start.

## Automated coverage this complements

- `pytest` (`techpath-backend/tests/`): stream-path minting/uniqueness/release, trainer-vs-participant URL scoping, media-state persistence + broadcast payloads, recording row lifecycle. Run via `poetry run pytest`.
- Playwright (`techpath-frontend/`): two-context (trainer + student) scenario asserting the `<video>` element reaches `readyState >= HAVE_CURRENT_DATA` and the WHIP/WHEP network calls return `2xx`. Run via `npm run test`.

Neither automated layer can assert "the audio was actually audible and in sync" — that's what the manual walkthrough above is for, and it is the gating check before this feature ships.
