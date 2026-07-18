---

description: "Task list for Live Classroom Audio/Video Streaming"
---

# Tasks: Live Classroom Audio/Video Streaming

**Input**: Design documents from `/specs/004-live-classroom-streaming/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/live-media-api.md](./contracts/live-media-api.md), [quickstart.md](./quickstart.md)

**Tests**: Included. The spec's own FR-016/SC-005 ("every step must be tested before release") and the user's original request ("everystep should be tested") make this an explicit requirement, not an optional add-on — see `research.md` Decision 5 for the three-layer strategy (pytest, Playwright, manual quickstart) these tasks implement.

**Organization**: Tasks are grouped by user story (P1/P2/P3 from `spec.md`) so each can be implemented, tested, and demoed independently. This extends the existing live-classroom vertical slice (`TrainingSession`, `app/services/classroom/*`, `ClassroomApp.jsx`, `ClassroomPanel.tsx`) rather than adding new apps or directories — see `plan.md` Project Structure.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Maps the task to US1, US2, or US3
- Every task includes an exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Configuration and constants every later phase needs.

- [X] T001 Add `LIVE_MEDIA_BASE_URL` and `WATCH_SERVICE_BASE_URL` settings (`Field(default="")`, same pattern as `AZURE_OPENAI_ENDPOINT`) plus an `is_live_media_configured` property to `techpath-backend/app/core/config.py`; document both in `techpath-backend/.env.example`
- [X] T002 [P] Add a `RecordingStatus` enum (`PROCESSING`, `READY`, `FAILED`) to `techpath-backend/app/core/constants.py`, following the existing `PollStatus`/`SessionStatus` enum style

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The stream-path lifecycle and URL-building service every user story's media flow depends on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 Add nullable `live_stream_path: Mapped[Optional[str]]` (`String(64)`, unique index) column to `TrainingSession` in `techpath-backend/app/models/training_roster.py`, next to the existing `join_code` column, with a docstring note cross-referencing it (mint/release lifecycle mirrors `join_code`)
- [X] T004 Create the Alembic migration adding `live_stream_path` to `training_sessions` (`down_revision = 's1t2u3d4e5n6'`) in `techpath-backend/app/db/migrations/versions/`, with matching `upgrade()`/`downgrade()`
- [X] T005 [P] Create `techpath-backend/app/services/classroom/media.py` with `mint_live_stream_path(session_id: int) -> str` (high-entropy, e.g. `class-{session_id}-{secrets.token_urlsafe(16)}`) and URL builders `whip_url(path)`, `whep_url(path)`, `hls_url(path)` that read `settings.LIVE_MEDIA_BASE_URL` — module docstring follows the style of `app/services/classroom/identity.py`
- [X] T006 [P] Add `MediaView` schema (`whip_url: Optional[str]`, `whep_url: Optional[str]`, `hls_url: Optional[str]`, `mic_muted: bool`, `camera_off: bool`, `screen_sharing: bool`) to `techpath-backend/app/schemas/classroom.py`
- [X] T007 Add `mint_live_media(db, session)` / `release_live_media(session)` helper methods to `CRUDTrainingSession` in `techpath-backend/app/crud/training_roster.py`, calling `media.mint_live_stream_path` and clearing the column respectively (not yet wired into any endpoint — that's US1/US2)

**Checkpoint**: Foundation ready — US1 can now be implemented and independently tested.

---

## Phase 3: User Story 1 - Teacher Starts a Live Session and Students Watch in Real Time (Priority: P1) 🎯 MVP

**Goal**: Trainer clicks "Start Session" → camera/mic go live → enrolled student sees the video in the classroom page's designated area and hears synced audio.

**Independent Test**: Start a session as a trainer in one browser, join as a student in another, confirm the student's video area shows live video with audible, synced audio within a few seconds — matches `spec.md` User Story 1 acceptance scenarios and `quickstart.md` Scenario 1.

### Tests for User Story 1

- [X] T008 [P] [US1] Integration test: `POST /trainer/sessions/{id}/start` mints `live_stream_path` and returns `media.whip_url` only to the owning trainer (403 for a different trainer, per existing `_assert_owns_batch` pattern) in `techpath-backend/tests/test_trainer_media.py`
- [X] T009 [P] [US1] Integration test: `GET /classroom/{id}/state` returns `media.whep_url`/`media.hls_url` only to a caller holding a valid classroom token for a *live* session, and `media: null` when the session isn't live or has no `live_stream_path` yet, in `techpath-backend/tests/test_classroom_media.py`
- [X] T010 [P] [US1] Playwright test: student context's video tile leaves its placeholder and completes WHEP signaling against a mocked media endpoint, in `techpath-frontend/tests/classroom-live-media.spec.ts` (also added `techpath-frontend/playwright.config.ts` — this repo had `npm run test` wired but no Playwright config/tests yet). Trainer-side (admin, separate app) covered by `tsc --noEmit` only — see file header comment.

### Implementation for User Story 1

- [X] T011 [US1] Wire `mint_live_media`/`release_live_media` (T007) into `start_session`/`end_session` in `techpath-backend/app/api/v1/endpoints/trainer.py`; extend `_session_out` to include `media: MediaView` (whip_url populated only for this trainer-facing response, only while live)
- [X] T012 [US1] Add `media: Optional[MediaView]` to `SessionStateResponse` in `techpath-backend/app/schemas/classroom.py` and populate it (whep_url/hls_url, no whip_url) inside `get_state` in `techpath-backend/app/api/v1/endpoints/classroom.py`
- [X] T013 [P] [US1] Create `PresenterVideoTile.tsx` in `techpath-admin/src/components/training/PresenterVideoTile.tsx` — `getUserMedia` capture, local preview `<video>`, `RTCPeerConnection` + WHIP POST to `whip_url` (port the `ClassroomBroadcaster` class from `CLASSROOM-WEBAPP-GUIDE.md` into TypeScript). Local mute/camera-off controls included now; broadcasting that state to students is US2 (T025).
- [X] T014 [US1] Wire `PresenterVideoTile` into `techpath-admin/src/app/(trainer)/trainer/sessions/[id]/present/page.tsx` as a floating picture-in-picture tile over the slide area, shown while `isLive`
- [X] T015 [P] [US1] Create `ClassroomVideoTile.jsx` in `techpath-frontend/src/components/react-components/ClassroomVideoTile.jsx` — WHEP viewer (`RTCPeerConnection` + POST to `whep_url`, `ontrack` → `<video>`), with explicit "not live yet" / "connecting" / "error" placeholder states (port the `ClassroomViewer` class from the guide)
- [X] T016 [US1] Render `ClassroomVideoTile` in the designated video area of `LiveScreen` in `techpath-frontend/src/components/react-components/ClassroomApp.jsx` (always visible above the slide/code tab content), passing `liveState.media`; teardown happens for free on unmount when `session_ended` flips the app out of the `live` stage
- [X] T017 [US1] Add `media`/`MediaView` fields to the TypeScript types in `techpath-frontend/src/types/classroom.ts` and `techpath-admin/src/types/training.ts` (both `startSession`/`endSession` and `getState` already return the full response object, so no service-layer change was needed beyond the type)
- [ ] T018 [US1] Run `quickstart.md` Scenario 1 (steps 1–4) manually against a live `LIVE_MEDIA_BASE_URL` target; record pass/fail for each acceptance scenario in the PR/checklist — **not run**: this environment has no real MediaMTX host, camera/mic hardware, or Firebase-authenticated trainer/student browser sessions available. Requires a human with the real `live.techpath.biz` target before this feature ships (see FR-016/SC-005).

**Checkpoint**: User Story 1 is fully functional and independently testable — this is the MVP.

---

## Phase 4: User Story 2 - Teacher Controls Audio, Video, and Screen Share During the Session (Priority: P2)

**Goal**: Trainer can mute/unmute, toggle camera, and switch to/from screen share mid-session, with every change reflected on student screens within a couple of seconds.

**Independent Test**: With a session already live (US1), toggle mute/camera/screen-share from the trainer's controls and confirm each state change reaches a connected student's view — matches `spec.md` User Story 2 and `quickstart.md` Scenario 2.

### Tests for User Story 2

- [X] T019 [US2] Integration test: `POST /trainer/sessions/{id}/media/state` persists the three flags, publishes a `media_state_changed` event via the bus, rejects a non-owning trainer (403) and a non-live session (422/ValidationError) in `techpath-backend/tests/test_trainer_media.py`

### Implementation for User Story 2

- [X] T020 Add `media_mic_muted`, `media_camera_off`, `media_screen_sharing` (`Boolean`, `default=False`) columns to `TrainingSession` in `techpath-backend/app/models/training_roster.py`
- [X] T021 Create the Alembic migration adding those three columns (`down_revision` = the revision created in T004) in `techpath-backend/app/db/migrations/versions/`
- [X] T022 [P] [US2] Add `MediaStateRequest` schema (`mic_muted`, `camera_off`, `screen_sharing`, all `Optional[bool]`) to `techpath-backend/app/schemas/classroom.py`
- [X] T023 [US2] Implement `POST /trainer/sessions/{session_id}/media/state` in `techpath-backend/app/api/v1/endpoints/trainer.py`: partial-update the three flags (`exclude_unset`), `bus.publish(..., "media_state_changed", {...})`, return `TrainingSessionResponse` (depends on T020–T022)
- [X] T024 [US2] Include `mic_muted`/`camera_off`/`screen_sharing` in the `MediaView` populated by `get_state` in `techpath-backend/app/api/v1/endpoints/classroom.py`
- [X] T025 [P] [US2] Add mute/camera-off/screen-share controls to `PresenterVideoTile.tsx` (`techpath-admin`): `toggleAudio()`, `toggleVideo()`, `startScreenShare()`/`stopScreenShare()` (`getDisplayMedia` + `replaceTrack`, auto-revert on the track's native `onended`), each calling the new `/media/state` endpoint via a new `trainerService.setMediaState()`
- [X] T026 [P] [US2] Handle the `media_state_changed` event in `ClassroomApp.jsx`'s WS subscribe switch (`techpath-frontend`) — merges onto `liveState.media`, which `ClassroomVideoTile` already renders (camera-off placeholder, muted badge); added the event to both apps' `ClassroomEvent` union types
- [X] T027 [US2] "End Session" only exists on the session detail page (`[id]/page.tsx`), not the present page — navigating there unmounts `PresenterVideoTile`, whose own `useEffect(() => stop, [])` cleanup already stops local tracks and closes the peer connection. No additional wiring needed; verified the cleanup path exists.
- [ ] T028 [US2] Run `quickstart.md` Scenario 2 (steps 5–9) manually, including both the in-app "stop sharing" control and the browser's native "Stop sharing" banner; record pass/fail — **not run**, same reason as T018 (no real MediaMTX/camera hardware/trainer+student sessions in this environment)

**Checkpoint**: User Stories 1 and 2 both work independently — full live presenting experience.

---

## Phase 5: User Story 3 - Absent Students Watch a Recorded Replay (Priority: P3)

**Goal**: After a live session ends, its recording is transcoded and becomes available for enrolled students who missed it to watch on the existing materials portal.

**Independent Test**: Complete a live session (US1), wait for the replay to process, confirm a student account can find and play it back — matches `spec.md` User Story 3 and `quickstart.md` Scenario 3.

### Tests for User Story 3

- [X] T029 [US3] Integration test: a `SessionRecording` row is created only when `end_session` is called on a session that had a `live_stream_path`; `GET .../recording` is gated the same way `materials_published_at` already gates student access, in `techpath-backend/tests/test_recordings.py`

### Implementation for User Story 3

- [X] T030 Add `SessionRecording` model (`id`, `session_id` FK→`training_sessions.id` `ondelete=CASCADE`, `status`, `recording_path`, `watch_url`, `TimestampMixin`) to `techpath-backend/app/models/classroom.py`
- [X] T031 Create the Alembic migration adding the `session_recordings` table (`down_revision` = the revision created in T021) in `techpath-backend/app/db/migrations/versions/`
- [X] T032 [P] [US3] Add `session_recording_crud` (extends `CRUDBase`, plus `get_by_session(db, session_id)`) to `techpath-backend/app/crud/classroom.py`
- [X] T033 [P] [US3] Add `trigger_transcode(stream_path)` and `watch_url(stream_path)` to `techpath-backend/app/services/classroom/media.py`. Note: `watch_url` is deterministic (per the guide's URL scheme) so it's computed and stored immediately rather than waiting on the trigger response — `status` is the real "is it actually ready" gate. Also note: MediaMTX names the recording file itself from record-start time, which this backend never learns, so the trigger passes only `stream_path`, not an exact filename — the watch service is expected to resolve "the recording for this path" itself.
- [X] T034 [US3] In `end_session` (`techpath-backend/app/api/v1/endpoints/trainer.py`), when the session had a `live_stream_path`, create a `SessionRecording` (`status=processing`) and schedule `trigger_transcode` via FastAPI `BackgroundTasks` (existing pattern from `contact.py`) so ending the session doesn't block on an external call (depends on T030–T033)
- [X] T035 [US3] Implement `GET /trainer/sessions/{session_id}/recording` in `techpath-backend/app/api/v1/endpoints/trainer.py` (404 if no row exists)
- [X] T036 [US3] Extend `techpath-backend/app/api/v1/endpoints/student_portal.py`'s `get_session_materials` to include a `recording: RecordingView | None` field alongside published assets, gated the same way `materials_published_at` already gates access
- [X] T037 [P] [US3] Add replay UI (`RecordingCard`: processing/ready states, link to `watch_url`; `failed`/absent render nothing) to `techpath-frontend/src/components/react-components/StudentPortalApp.jsx`
- [ ] T038 [US3] Run `quickstart.md` Scenario 3 (steps 10–12) manually; record pass/fail — **not run**, same reason as T018/T028

**Known gap, flagged rather than silently glossed over**: nothing in this codebase or `CLASSROOM-WEBAPP-GUIDE.md` defines how the watch/transcode service reports completion back to this backend (no webhook, no documented status-check API). `trigger_transcode` fires the kickoff and the recording row is created, but nothing currently flips `status` from `processing` to `ready` — that requires either a webhook endpoint here or a scheduled poll job against the watch service, neither of which is specified. The states themselves (processing/ready/failed) and every gate around them are correctly implemented and tested; only the missing "how does `ready` actually get set" piece needs a follow-up decision.

**Checkpoint**: All three user stories independently functional — feature is complete end-to-end.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases from `spec.md` and the remaining `quickstart.md` checks that span multiple stories.

- [X] T039 [P] Implement HLS fallback (`hls.js`, `lowLatencyMode: true`, plus native Safari HLS) in `ClassroomVideoTile.jsx` for networks that block WebRTC (FR-012/SC-006) — only engaged if WHEP never once reaches `playing`; added a Playwright test (`falls back to HLS when WHEP is unreachable`) proving the fallback actually triggers
- [X] T040 [P] Two-sided reconnect handling: (a) backend — `start_session` already reuses the existing `live_stream_path`/`join_code` on a live→live restart (T011/T007), so a trainer whose browser drops and reconnects gets the same publish URL back; (b) frontend — `ClassroomVideoTile.jsx` now watches `RTCPeerConnection.connectionState` and shows a distinct "Reconnecting…" state with a fixed-delay auto-retry if an already-`playing` WHEP connection fails/disconnects
- [X] T041 [P] Add a duplicate-concurrent-session guard to `start_session` in `techpath-backend/app/api/v1/endpoints/trainer.py` (new `CRUDTrainingSession.get_other_live_session`; rejects with `ValidationError` if another session for the same batch is already `live`, per FR-015)
- [X] T042 Add unauthorized-access tests covering both the trainer media endpoints and `GET /classroom/{id}/state`'s `media` field for unauthenticated/non-enrolled callers (FR-006/SC-004) in `techpath-backend/tests/test_media_authorization.py` — cross-session token rejection, no-credentials rejection, kicked-participant token rejection, non-owning-trainer rejection for whip_url/media-state/end-session, plus one "the boundary isn't over-tightened" sanity check
- [ ] T043 Run the full `quickstart.md` edge-case checklist (network fallback, unauthorized access, duplicate session, trainer reconnect, mid-session join) end-to-end against the real `live.techpath.biz`/`watch.techpath.biz` hosts — **not run**, same reason as T018/T028/T038 (no real MediaMTX/watch service reachable from this environment). Everything checkable without those hosts (duplicate-session rejection, unauthorized access, HLS fallback wiring, reconnect state machine) is covered by the automated tests instead.
- [X] T044 [P] Documented `LIVE_MEDIA_BASE_URL` / `WATCH_SERVICE_BASE_URL` in `techpath-backend/.env.example` (done in Phase 1/T001) and `techpath-backend/app/core/config.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories (US1 needs `live_stream_path` + `media.py` to exist)
- **User Story 1 (Phase 3)**: Depends on Foundational only — this is the MVP
- **User Story 2 (Phase 4)**: Depends on Foundational; T020/T021 (its own migration) must land before T023; in practice built after US1 since it extends the same presenter/viewer components US1 creates, but does not require US1's tests to pass first
- **User Story 3 (Phase 5)**: Depends on Foundational only for the schema pattern; T034 hooks into `end_session`, which US1 already touches (T011) — implement after US1 to avoid a merge conflict in the same function, not because of a hard data dependency
- **Polish (Phase 6)**: Depends on US1 + US2 (T039/T040 touch the same viewer/presenter components) and US1's `start_session` changes (T041)

### Within Each User Story

- Migration (model → alembic revision) before the CRUD/service code that uses the new columns
- Backend endpoint before the frontend component that calls it
- Trainer-side (`techpath-admin`) and student-side (`techpath-frontend`) component tasks are parallel-safe with each other (different apps, different files)
- Manual quickstart task last, once everything else in the phase is done

### Parallel Opportunities

- T001 and T002 (Setup) in parallel
- T005 and T006 (Foundational) in parallel once T003/T004 land
- T008, T009, T010 (US1 tests) in parallel
- T013 and T015 (US1: admin vs frontend components) in parallel
- T022, T025, T026 (US2: schema, admin controls, frontend handling) largely parallel once T020/T021 land
- T032 and T033 (US3: CRUD vs service) in parallel
- T039, T040, T041, T044 (Polish) in parallel — different files

---

## Parallel Example: User Story 1

```bash
# Tests together:
Task: "Integration test for whip_url trainer scoping in techpath-backend/tests/test_trainer_media.py"
Task: "Integration test for whep_url/hls_url participant scoping in techpath-backend/tests/test_classroom_media.py"
Task: "Playwright student-side WHEP wiring test in techpath-frontend/tests/classroom-live-media.spec.ts"

# Components together (different apps):
Task: "Create PresenterVideoTile.tsx in techpath-admin/src/components/training/PresenterVideoTile.tsx"
Task: "Create ClassroomVideoTile.jsx in techpath-frontend/src/components/react-components/ClassroomVideoTile.jsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (blocks everything)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: run `quickstart.md` Scenario 1 end-to-end against a real MediaMTX target
5. Demo: a trainer can go live and a student can see/hear them — the core value from `spec.md`

### Incremental Delivery

1. Setup + Foundational → foundation ready
2. User Story 1 → validate → demo (MVP: live audio/video works)
3. User Story 2 → validate → demo (trainer has in-session controls)
4. User Story 3 → validate → demo (absent students can catch up)
5. Polish → validate full `quickstart.md` edge-case checklist → ship

### Parallel Team Strategy

Once Foundational is done, US1 (both apps' video components) can be split between a backend developer (T008–T012) and two frontend developers (T013–T014 admin, T015–T017 frontend) working in parallel, since the contract in `contracts/live-media-api.md` is agreed upfront.

---

## Notes

- [P] tasks touch different files with no unmet dependencies
- Every task lists an exact file path — no task should require guessing where code goes
- Commit after each task or logical group, per this repo's normal workflow
- Migrations are deliberately split one-per-story (T004, T021, T031) rather than one big migration, so each story's schema change ships and can be reverted independently
- Story phases are ordered P1 → P2 → P3 for delivery, but T020/T021 (US2's migration) and T030/T031 (US3's migration) have no *data* dependency on US1/US2 code — only the shared `end_session`/`start_session` functions create a practical (not architectural) ordering reason to build them in sequence
