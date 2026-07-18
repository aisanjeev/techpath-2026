"""Realtime delivery for the live classroom.

Production runs ``--workers 2`` (see deploy-backend.yml). A WebSocket connection is
pinned to whichever worker process accepted it — there is no way around that with plain
uvicorn workers — so an in-memory broadcaster only ever reaches sockets on its own
worker. A trainer on worker A and a student on worker B would silently never see each
other's events, roughly half the time, at random.

The fix is a durable outbox (``ClassroomEvent``) plus a small poller in every worker:
each publish appends a row; each worker's poll loop reads rows newer than the last one
it saw for every session it has local sockets for, and fans them out locally. Correct
under any worker count, with the database that is already there — no Redis to provision.
If this ever needs push-level latency instead of the ~500ms poll tick, swap the body of
``_poll_loop`` for a LISTEN/NOTIFY or Redis pub/sub consumer; nothing above this module
would change, since callers only ever see ``publish()`` and the connection manager.
"""
import asyncio
import json
import logging
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional

from fastapi import WebSocket
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.classroom import ClassroomEvent

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 0.5


class ConnectionManager:
    """Per-worker-process registry of live WebSocket connections, grouped by session.

    Legitimately local — see module docstring. Cross-worker consistency comes from the
    poller below, not from this class.
    """

    def __init__(self) -> None:
        self._rooms: dict[int, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, session_id: int, ws: WebSocket) -> None:
        async with self._lock:
            self._rooms[session_id].add(ws)

    async def disconnect(self, session_id: int, ws: WebSocket) -> None:
        async with self._lock:
            room = self._rooms.get(session_id)
            if room is not None:
                room.discard(ws)
                if not room:
                    del self._rooms[session_id]

    async def local_broadcast(self, session_id: int, message: dict) -> None:
        conns = list(self._rooms.get(session_id, ()))
        if not conns:
            return
        text = json.dumps(message)
        dead: list[WebSocket] = []
        for ws in conns:
            try:
                await ws.send_text(text)
            except Exception:
                dead.append(ws)
        for ws in dead:
            await self.disconnect(session_id, ws)

    def local_connection_count(self, session_id: int) -> int:
        return len(self._rooms.get(session_id, ()))

    def active_session_ids(self) -> list[int]:
        return list(self._rooms.keys())


manager = ConnectionManager()


async def publish(db: AsyncSession, session_id: int, event_type: str, payload: dict) -> None:
    """Append an event to the outbox.

    Only flushes — the caller's ``get_db()`` dependency commits on a clean exit, same as
    every other write in this codebase. Every worker's poller (including this one's) picks
    the row up on its next tick once that commit lands; there is deliberately no local
    fast-path broadcast here, so there is exactly one delivery code path to reason about.
    """
    event = ClassroomEvent(
        session_id=session_id,
        event_type=event_type,
        payload_json=json.dumps(payload, default=str),
        created_at=datetime.now(timezone.utc),
    )
    db.add(event)
    await db.flush()


_poll_task: Optional[asyncio.Task] = None

# Aliveness signal for the poller (see poller_health below) — this loop is the entire
# cross-worker delivery mechanism (module docstring), so if it silently dies there is
# otherwise zero diagnostic signal beyond "realtime stuff stopped updating".
_last_tick_at: Optional[float] = None


async def _poll_tick(db: AsyncSession, last_seen: dict[int, int]) -> None:
    session_ids = manager.active_session_ids()

    # A session with local sockets but no cursor yet is new to this worker as of this
    # tick. Seed it to the current max id rather than 0 — otherwise a freshly-connected
    # student would get the session's entire event history replayed as if it were
    # happening now (every past slide change, every past code keystroke broadcast).
    # REST /classroom/{id}/state is what actually bootstraps "where things stand right
    # now"; the stream only ever needs to carry what happens from here on.
    fresh = [sid for sid in session_ids if sid not in last_seen]
    for session_id in fresh:
        max_id = await db.scalar(
            select(func.max(ClassroomEvent.id)).where(ClassroomEvent.session_id == session_id)
        )
        last_seen[session_id] = max_id or 0

    for session_id in session_ids:
        if session_id in fresh:
            continue
        cursor = last_seen[session_id]
        result = await db.execute(
            select(ClassroomEvent)
            .where(ClassroomEvent.session_id == session_id, ClassroomEvent.id > cursor)
            .order_by(ClassroomEvent.id)
        )
        rows = result.scalars().all()
        if not rows:
            continue
        last_seen[session_id] = rows[-1].id
        for row in rows:
            await manager.local_broadcast(
                session_id,
                {"type": row.event_type, "payload": json.loads(row.payload_json)},
            )

    # Sessions with no local sockets left don't need a tracked cursor — drop it so a
    # long-lived worker doesn't accumulate one entry per session forever.
    for session_id in list(last_seen):
        if session_id not in session_ids:
            del last_seen[session_id]


async def _poll_loop() -> None:
    global _last_tick_at
    last_seen: dict[int, int] = {}
    while True:
        try:
            if manager.active_session_ids():
                # A fresh session per tick, not a long-lived one: MySQL's default
                # REPEATABLE READ would otherwise pin this connection to the snapshot
                # from its first query and never observe rows other transactions commit
                # afterwards.
                async with AsyncSessionLocal() as db:
                    await _poll_tick(db, last_seen)
            # Recorded whether or not there were active sessions to poll — this tracks
            # "the loop is alive and cycling", not "there was something to deliver", so
            # an idle worker with zero connections never looks like a dead poller.
            _last_tick_at = time.time()
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 — one bad tick must not kill the loop
            logger.warning("Classroom event poll tick failed: %s", exc)
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


def start_poller() -> None:
    global _poll_task
    if _poll_task is None:
        _poll_task = asyncio.create_task(_poll_loop())
        logger.info("Classroom event poller started")


async def stop_poller() -> None:
    global _poll_task
    if _poll_task is not None:
        _poll_task.cancel()
        try:
            await _poll_task
        except asyncio.CancelledError:
            pass
        _poll_task = None
        logger.info("Classroom event poller stopped")


def poller_health() -> dict:
    """Cheap, synchronous aliveness check for the background poller — not wired to an
    HTTP route yet, just callable from anywhere in-process (e.g. a future /health
    endpoint) so the poller's state stops being a total black box.
    """
    now = time.time()
    return {
        "running": _poll_task is not None and not _poll_task.done(),
        "last_tick_at": _last_tick_at,
        "seconds_since_last_tick": (now - _last_tick_at) if _last_tick_at is not None else None,
    }
