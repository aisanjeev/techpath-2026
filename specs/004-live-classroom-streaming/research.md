# Phase 0 Research: Live Classroom Audio/Video Streaming

All Technical Context items were resolvable from the existing codebase and the provided reference guide (`C:\Users\Techpath\Documents\CLASSROOM-WEBAPP-GUIDE.md`) — no `[NEEDS CLARIFICATION]` markers remained after the codebase survey below, so this phase records decisions and rejected alternatives rather than open questions.

## Decision 1: Transport — WHIP/WHEP against the existing self-hosted MediaMTX server

**Decision**: Use WebRTC WHIP (browser → server publish) and WHEP (server → browser playback) against the org's already-running `live.techpath.biz` MediaMTX instance, using only browser-native `RTCPeerConnection`/`getUserMedia`/`getDisplayMedia` — no client SDK, no new backend media dependency.

**Rationale**:
- The org already operates this server (`CLASSROOM-WEBAPP-GUIDE.md`); building or buying a second media pipeline (e.g. a hosted SFU provider) would duplicate infrastructure that's already paid for and already reachable from both `techpath-admin` and `techpath-frontend`.
- Confirmed via codebase survey: `techpath-backend/pyproject.toml` has no `aiortc`, `av`, or any media-processing package — media has never flowed through FastAPI, and WHIP/WHEP's browser-to-media-server-direct model keeps it that way. FastAPI stays a signaling/authorization layer only.
- ~200ms glass-to-glass latency easily satisfies spec SC-001 (5s) and the "no perceptible lag" requirement in SC-002.

**Alternatives considered**:
- *Third-party hosted video (Twilio Video, Daily, LiveKit Cloud)*: rejected — recurring per-minute cost for infrastructure the org already self-hosts for free, and would require a second identity/authorization bridge alongside the one this feature already needs to build for MediaMTX.
- *Proxy media through FastAPI*: rejected — would reintroduce exactly the multi-worker "a socket only lives on one process" problem that `app/services/classroom/bus.py`'s docstring explains at length and solved via a DB-outbox poller. WHIP/WHEP's browser↔MediaMTX-direct model sidesteps that problem entirely for media, so only lightweight state events (mute/camera/screen-share) need the existing bus.
- *Low-latency HLS as the primary path*: rejected as primary (1-2s latency vs WHEP's ~200ms hurts the live Q&A feel implied by spec User Story 1), but **kept as the required fallback** (FR-012 / SC-006) for networks that block WebRTC/UDP — the guide already documents this exact fallback via `hls.js`.

## Decision 2: Authorization — reuse the join-code-scoped access pattern, not MediaMTX-side auth

**Decision**: MediaMTX stays `authMethod: internal` (open) as already configured; TechPath's backend is the sole gate, by never exposing a stream path to a caller it hasn't already authorized. The path itself is a new unguessable secret (like `join_code`, but not shown on-screen/spoken aloud, so it can be longer and higher-entropy) minted once per session-goes-live and released when the session ends.

**Rationale**: This is not a new pattern — it is exactly what `training_session_crud.generate_join_code()` / `get_by_join_code()` (`app/crud/training_roster.py`) and the classroom token machinery (`app/services/classroom/identity.py`) already do for chat/poll access. Reusing it means:
- The trainer-only WHIP URL is only ever returned from an endpoint gated by `get_current_trainer_user` + `_assert_owns_batch` (same as every other trainer route in `trainer.py`).
- The student-only WHEP/HLS URL is only ever returned from the existing `get_current_participant`-gated surface (`classroom.py`), i.e. folded into the response of `join_classroom`/`identify`/`get_state`, which a caller can only reach after proving a valid join code (+ optional roster email match).
- No second credential system, no MediaMTX webhook/API-key integration to build or operate.

**Alternatives considered**:
- *Turn on MediaMTX's built-in auth (JWT/webhook)*: rejected for v1 — the guide explicitly recommends leaving it open and doing access control application-side, and adding it would mean maintaining two authorization systems in sync for no additional security (the random-path strategy already makes the stream URL unguessable to anyone who wasn't handed it by an authorized backend response).

## Decision 3: Where live-media state lives — extend `TrainingSession`, don't invent a parallel entity

**Decision**: Add live-media columns directly to `training_sessions` (stream path, mic/camera/screen-share flags) and one new small table, `session_recordings`, rather than a separate "ClassSession"/"LiveSession" entity.

**Rationale**: `TrainingSession`'s own docstring says it exists precisely for this: *"...so the live-classroom work has something to hang attendance, polls and progress off without a migration on a hot table."* The session already carries `status` (scheduled/live/ended), `started_at`/`ended_at`, and `join_code` with exactly the lifecycle (mint-on-start, release-on-end) the new stream path needs. `current_asset_id` and `timer_started_at`/`timer_duration_seconds` are the established precedent for "persist derived live state on the session row so a reconnecting/late-joining client can bootstrap it via `GET /classroom/{id}/state` instead of replaying an event log" — the new mic/camera/screen-share flags follow that same pattern.

**Alternatives considered**:
- *New `LiveClassSession` table 1:1 with `TrainingSession`*: rejected — it would duplicate the batch/module/trainer FK wiring and the start/end lifecycle `TrainingSession` already owns, for no isolation benefit (nothing about live-media state needs a different lifecycle than the session itself).

## Decision 4: Recording / VOD — reuse the existing external transcode/watch service, don't rebuild it

**Decision**: On `end_session`, call the already-existing external `watch.techpath.biz` transcode API (documented in the guide) from a new `app/services/classroom/media.py` function, and persist a `SessionRecording` row (`status: processing → ready`) so the student portal can poll/display it. No new video-processing code is written in this repo.

**Rationale**: MediaMTX already auto-records every WHIP publish to `/mnt/nas/media-streams/{stream_path}/...` with zero backend trigger; the only integration work is (a) knowing the recording's eventual path/filename convention to pass to the transcode trigger, and (b) tracking processing status so FR-014/SC-007 ("replay available to absent students") has something to poll. This is a thin service call + one table, consistent with how `app/services/email.py` and `app/services/ai/*` already wrap other external calls behind `app/services/`.

**Alternatives considered**:
- *Backend actively watches the filesystem for new recordings*: rejected — needless coupling to the media server's disk layout when the guide already documents a clean HTTP trigger for the same job.

## Decision 5: Testing strategy for a feature pytest can't observe end-to-end

**Decision**: Three layers, matching spec FR-016/SC-005's "every step tested" requirement without pretending an automated suite can assert "the pixels moved and the speaker made sound":
1. `pytest` integration tests for everything that *is* deterministic and server-side: stream-path minting/uniqueness/release, authorization scoping (trainer-only vs participant-only URL exposure, rejection for non-enrolled/unauthenticated callers), media-state persistence and broadcast, recording row lifecycle.
2. Playwright, two browser contexts (trainer + student) driving the real pages, asserting the DOM/video-element wiring reaches a `playing` state and that WHIP/WHEP network calls succeed — this is the existing `techpath-frontend` e2e tool (`npm run test`), extended rather than introducing a new one.
3. A manual `quickstart.md` checklist mapped 1:1 to every acceptance scenario in `spec.md`, run against the real `live.techpath.biz` target before shipping — audio/video fidelity and cross-browser/network-fallback behavior ultimately need a human watching a screen and listening, which is exactly what the spec's Independent Test descriptions call for.

**Rationale**: This mirrors how the existing classroom feature is tested today (no WebSocket-frame-level pytest assertions found in the survey; behavior is verified through endpoint auth/state tests plus the working UI) and keeps the automated suite honest about what it can and can't prove.
