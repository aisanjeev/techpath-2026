# Research: Toggle Recording

## Context
The goal is to allow trainers to enable or disable recording of live sessions, saving on-demand video when requested and deleting the recording file to save storage when not requested.

## Finding 1: Recording Strategy
**Decision**: Use "Option A: The Auto-Delete Strategy".
**Rationale**: Recommended by `RECORDING-STRATEGY.md`. MediaMTX records everything by default at the system level. Rather than managing complex start/stop recording states dynamically on the media server (which isn't natively supported), the system keeps Auto-Record ON. If the trainer doesn't want the recording, the backend simply deletes the `.mp4` file from the MinIO storage bucket at the end of the session.
**Alternatives considered**: Option B (Frontend Browser Strategy). This was rejected because it relies on the trainer's browser to upload massive `.webm` files, which is prone to failure and consumes significant trainer upload bandwidth.

## Finding 2: Session End Hook
**Decision**: Execute the deletion logic in the existing `end_session` endpoint.
**Rationale**: When a session ends, the backend currently triggers a transcode. We will intercept this flow: if `keep_recording` is false, we call the MinIO SDK (or `storage_service.py`) to delete the file instead of triggering a transcode.

## Finding 3: Database Updates
**Decision**: Add a `keep_recording` boolean column to the `TrainingSession` model.
**Rationale**: We need to persist the trainer's choice so that when `end_session` is called, the backend knows whether to retain or delete the video. Default should be `True` or `False` depending on product requirements (default to `False` to save space).
