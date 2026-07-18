# Research: Student Speaker Control

## Realtime Signaling Strategy
- **Decision**: Use existing REST + Event Bus pattern (`classroom_ws.py` + `bus.py`) in `techpath-backend`.
- **Rationale**: The backend constitution mandates that all state changes occur via REST and WebSockets are for delivery only. Raising a hand and approving a student are state changes. They will hit a REST endpoint, be persisted, and then broadcast via the event bus to the participants.
- **Alternatives considered**: True bi-directional WebSockets (rejected due to constitution and scale complexity).

## WebRTC Integration
- **Decision**: Follow Scenario A from the Multi-Speaker Guide using MediaMTX unique paths (`/class-{id}-doubt-{student_id}/whip`).
- **Rationale**: Provides isolation from the main stream and ensures the trainer can selectively subscribe to the student's audio.
- **Alternatives considered**: Mixing audio on the server (rejected due to latency and processing overhead).
