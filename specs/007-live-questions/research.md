# Phase 0: Outline & Research

## Decision 1: Backend Implementation for Real-Time Q&A

**Decision**: Use the existing `bus` (Classroom Broadcaster) in FastAPI for real-time WebSocket communication to push new questions to the trainer, and standard REST POST endpoints for students to submit questions.

**Rationale**: `techpath-backend` already has a real-time messaging system built via WebSockets (`app/services/classroom/bus.py`). Reusing this avoids introducing new infrastructure like Redis PubSub or third-party services (Pusher). The HTTP POST endpoint handles validation and persistence before broadcasting, keeping the WebSocket strictly for downstream notification.

**Alternatives considered**: 
- Having students send questions directly over WebSocket (more complex error handling and authentication for upstream messages).
- Polling via REST (poor performance and latency).

---

## Decision 2: Data Persistence & Prioritization

**Decision**: Store questions in a new PostgreSQL table `training_session_questions` using Async SQLAlchemy 2.0. Include fields for `upvotes` (integer) and `is_answered` (boolean). Include `is_public` (boolean) to handle the trainer toggle requirement.

**Rationale**: The user requirements explicitly state that questions must be permanently saved, upvotable if public, and toggleable (public/private). A relational database table linked to `training_sessions` perfectly models this. 

**Alternatives considered**:
- Ephemeral in-memory storage (rejected due to permanence requirement).
- NoSQL document store (rejected as it violates the project's PostgreSQL architecture).

---

## Decision 3: Frontend Trainer UI (techpath-admin)

**Decision**: Integrate the Q&A list into the existing `ClassroomPanel` component using Zustand for state management and the existing WebSocket subscription logic for real-time updates.

**Rationale**: The `ClassroomPanel` is already the hub for the trainer's live interactions (polls, chat, etc.). Adding a "Q&A" tab or section here provides a unified experience.

**Alternatives considered**:
- A separate window/popup (too obtrusive).

---

## Decision 4: Student UI (techpath-frontend)

**Decision**: Add an "Ask Question" (❓) floating action button or sidebar panel to the student's live classroom view (React Island in Astro). This panel will show public questions with an upvote button, or just a simple input if questions are private.

**Rationale**: The user requested a "good symbol" (like a question mark) and an "easy for students" interface. A non-obtrusive UI that doesn't block the video stream is ideal.
