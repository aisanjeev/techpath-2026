# Phase 1 Data Model: Live Classroom Audio/Video Streaming

Extends the existing schema (`app/models/training_roster.py`, `app/models/classroom.py`) rather than introducing a parallel entity — see [research.md](./research.md) Decision 3.

## `TrainingSession` (existing table `training_sessions`) — new columns

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `live_stream_path` | `String(64)` | yes | `NULL` | Unguessable secret path segment (e.g. `class-{session_id}-{random32}`), minted in `start_session` alongside `join_code`, released (`NULL`) in `end_session`. Unique index. Never rendered directly in any UI — only used server-side to build WHIP/WHEP/HLS URLs before handing those to an already-authorized caller. |
| `media_mic_muted` | `Boolean` | no | `false` | Trainer's last-known mic state, mirrors `current_asset_id`'s "persist so late joiners can bootstrap" pattern. Meaningful only while `status == live`; reset to `false` on next `start_session`. |
| `media_camera_off` | `Boolean` | no | `false` | Same pattern, for camera. |
| `media_screen_sharing` | `Boolean` | no | `false` | Same pattern, for webcam-vs-screen-share source. |

**Validation / state rules**:
- `live_stream_path` is set if and only if a WHIP publish has been authorized for this session (mint at the same moment `join_code` is minted in `start_session`), and is cleared exactly when `join_code` is cleared in `end_session` — same lifecycle, same handler, so they can never drift out of sync.
- `media_mic_muted` / `media_camera_off` / `media_screen_sharing` are only mutable by the endpoint that authenticates the session's trainer (same `_assert_owns_batch` guard as `set_current_slide`/`start_timer`), and only while `status == live`.
- Existing `status` transitions (`scheduled → live → ended`, plus `cancelled`) are unchanged; this feature adds no new status values. "Live" already means "trainer is presenting"; this feature makes that presentation carry audio/video too.

## `SessionRecording` (new table `session_recordings`)

| Column | Type | Nullable | Notes |
|---|---|---|---|
| `id` | `Integer`, PK | no | |
| `session_id` | `Integer`, FK → `training_sessions.id`, `ondelete=CASCADE` | no | One session may have zero (never went live / no recording produced) or one recording row per completed live session. |
| `status` | `String(20)` | no | `processing` \| `ready` \| `failed`. Starts `processing` when `end_session` triggers the transcode call. |
| `recording_path` | `String(255)` | yes | Source file path on the media server (`/mnt/nas/media-streams/{stream_path}/...`), used only to build the transcode request — not itself served to clients. |
| `watch_url` | `String(500)` | yes | Populated once `status == ready`; the URL the student portal links to (`https://watch.techpath.biz/{stream_path}`). |
| `created_at` / `updated_at` | `DateTime(timezone=True)` | no | Via `TimestampMixin`, consistent with every other model in this codebase. |

**Relationships**: `TrainingSession.recording` (one-to-one-ish via `session_id`, no uniqueness constraint enforced at the DB level since a re-presented/re-published module already allows re-recording in principle — CRUD layer takes the most recent row).

**Validation / state rules**:
- A row is created only from `end_session`, only if a `live_stream_path` existed for that session (i.e., media was actually published — a session that only ever used chat/polls with no live media produces no recording row).
- `status` moves `processing → ready` (or `→ failed`) via a follow-up call from the trainer materials-publish flow or a lightweight poll endpoint — exact trigger mechanism is a `tasks.md` implementation detail, not a data-model concern.
- Visible to a student only through the existing `materials_published_at`-gated surface (`student_portal.py` / `list_published_for_student`) — replay availability piggybacks on the publish gate the session already has, per spec Edge Cases ("replay processing" state) and FR-014.

## New `ClassroomEvent` type

No schema change — `ClassroomEvent.event_type` is a free-text column already. This feature adds one new value to the set of strings the bus carries:

- **`media_state_changed`** — payload `{"mic_muted": bool, "camera_off": bool, "screen_sharing": bool}`. Published whenever the trainer's media-state endpoint updates the three `TrainingSession` flags above. Consumed the same way `slide_change`/`code_update`/`timer_started` already are, by both `ClassroomApp.jsx` (student) and `ClassroomPanel.tsx` (trainer's own UI, for consistency across the trainer's own multiple tabs/devices).

## Key entities from `spec.md`, mapped to concrete rows

| Spec entity | Concrete model |
|---|---|
| Class Session | `TrainingSession` (existing) + the new columns above |
| Session Participant | `SessionParticipant` (existing, unchanged — attendance/identity is orthogonal to whether media happens to be flowing) |
| Recording | `SessionRecording` (new, above) |
