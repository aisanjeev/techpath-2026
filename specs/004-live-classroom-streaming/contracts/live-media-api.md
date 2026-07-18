# Contracts: Live Classroom Audio/Video

New and modified REST surface (both under `app/api/v1/endpoints/{trainer,classroom}.py`) plus one new realtime event on the existing `ClassroomEvent` bus. Auth/scoping conventions match the rest of `trainer.py` / `classroom.py` exactly — nothing new is introduced (see [research.md](../research.md) Decision 2).

## Trainer-side (Firebase-authenticated, `get_current_trainer_user` + `_assert_owns_batch`)

### `POST /trainer/sessions/{session_id}/start` — modified

Existing endpoint (`app/api/v1/endpoints/trainer.py`). No request shape change. Response (`TrainingSessionResponse`) gains one field:

```jsonc
{
  // ...existing TrainingSessionResponse fields unchanged...
  "media": {
    "whip_url": "https://live.techpath.biz/class-42-8f2a.../whip"  // present only while status == live
  }
}
```

`live_stream_path` is minted in the same branch that currently mints `join_code` (only when transitioning into `live`, never on a restart of an already-live session) — see [data-model.md](../data-model.md).

### `POST /trainer/sessions/{session_id}/end` — unchanged request/response shape

Behavior extends: also clears `live_stream_path`, and if a `live_stream_path` had been set, kicks off the recording pipeline (creates a `SessionRecording` row, calls the external transcode trigger — see below). Still publishes the existing `session_ended` bus event; students' video/audio teardown hangs off that event exactly like every other `session_ended` reaction today.

### `POST /trainer/sessions/{session_id}/media/state` — new

Request:
```jsonc
{ "mic_muted": true, "camera_off": false, "screen_sharing": false }  // all optional, partial update
```

Response: `TrainingSessionResponse` (same shape `get_session` returns, now including the three `media_*` flags). Publishes `media_state_changed` on the bus (payload = the three resulting boolean flags). 403s via the same `_assert_owns_batch` guard as `set_current_slide`; 404s if session doesn't exist; a `ValidationError` if `status != live` (no state to change on a session that isn't presenting).

### `GET /trainer/sessions/{session_id}/recording` — new

Returns the session's `SessionRecording` row if one exists (`{"status": "processing"|"ready"|"failed", "watch_url": str | null}`), or `404` if no recording was ever produced (e.g., session never went live with media). Lets the presenter page show recording status without polling the student-facing endpoint.

## Student/participant-side (classroom-token-authenticated, `get_current_participant`)

### `POST /classroom/join` — unchanged shape

No change — join-code lookup is unaffected by whether the session happens to have live media.

### `GET /classroom/{session_id}/state` — modified

`SessionStateResponse` gains one field, populated only while `status == live` and `live_stream_path` is set:

```jsonc
{
  // ...existing SessionStateResponse fields unchanged...
  "media": {
    "whep_url": "https://live.techpath.biz/class-42-8f2a.../whep",
    "hls_url": "https://live.techpath.biz/class-42-8f2a.../index.m3u8",
    "mic_muted": false,
    "camera_off": false,
    "screen_sharing": false
  }
}
```

Only ever returned to a caller who has already passed `get_current_participant` (i.e., already holds a valid classroom token for a live, non-removed participation) — the same authorization boundary every other field on this response already relies on. `media` is `null` when the trainer hasn't started publishing media for this session (e.g. a chat/poll-only class, or before the trainer's browser finishes the WHIP handshake).

## Realtime: new `ClassroomEvent` type

### `media_state_changed`

```jsonc
{ "type": "media_state_changed", "payload": { "mic_muted": true, "camera_off": false, "screen_sharing": false } }
```

Delivered over the existing WebSocket (`classroom_ws.py`) to both trainer and student connections for a session, via the existing DB-outbox poller (`app/services/classroom/bus.py`) — no new transport. `ClassroomApp.jsx` and `ClassroomPanel.tsx` both already have a `subscribe((event) => ...)` switch for event types (`slide_change`, `timer_started`, etc.); this is one more `case`.

## External services this feature calls (not part of this repo's API surface, but part of its contract obligations)

| Call | Direction | Purpose |
|---|---|---|
| `POST https://live.techpath.biz/{live_stream_path}/whip` | Trainer's browser → MediaMTX, direct | Publish. FastAPI never touches this call; it only hands out the URL. |
| `POST https://live.techpath.biz/{live_stream_path}/whep` | Student's browser → MediaMTX, direct | Playback. Same — FastAPI only hands out the URL. |
| `GET https://live.techpath.biz/{live_stream_path}/index.m3u8` | Student's browser → MediaMTX, direct | HLS fallback (FR-012/SC-006). |
| `POST https://watch.techpath.biz/api/transcode/{live_stream_path}/{recording_filename}` | FastAPI backend → watch service | Triggered from `end_session`; response/webhook flips `SessionRecording.status` to `ready` and sets `watch_url`. |

`LIVE_MEDIA_BASE_URL` and `WATCH_SERVICE_BASE_URL` are added to `app/core/config.py` (same `Field(default=...)` pattern as `AZURE_OPENAI_ENDPOINT` etc.) so these hosts are never hardcoded.
