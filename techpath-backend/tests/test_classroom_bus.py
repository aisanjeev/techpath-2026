"""Tests for the live classroom realtime bus: the durable outbox (``publish``), the
per-worker WebSocket registry (``ConnectionManager``), and the poller's cursor-seeding
behavior (``_poll_tick``) that keeps a freshly-connected client from being replayed a
session's entire event history. See ``app/services/classroom/bus.py``'s module
docstring for why this indirection exists (multiple uvicorn workers, no shared memory).
"""
import json
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.classroom import ClassroomEvent
from app.services.classroom import bus
from app.services.classroom.bus import ConnectionManager


class FakeWebSocket:
    """Minimal stand-in for fastapi.WebSocket — just enough surface for the
    connection manager and poller, which only ever call ``send_text``."""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.received: list[str] = []

    async def send_text(self, text: str) -> None:
        if self.fail:
            raise RuntimeError("connection closed")
        self.received.append(text)


class TestPublish:
    async def test_publish_inserts_event_row(self, test_db: AsyncSession) -> None:
        await bus.publish(test_db, 101, "slide_change", {"asset_id": 42, "title": "Intro"})

        result = await test_db.execute(
            select(ClassroomEvent).where(ClassroomEvent.session_id == 101)
        )
        events = result.scalars().all()
        assert len(events) == 1
        event = events[0]
        assert event.session_id == 101
        assert event.event_type == "slide_change"
        assert json.loads(event.payload_json) == {"asset_id": 42, "title": "Intro"}
        assert event.created_at is not None

    async def test_publish_serializes_non_json_native_values(
        self, test_db: AsyncSession
    ) -> None:
        """``json.dumps(..., default=str)`` is the guarantee that lets any payload be
        appended without every caller pre-serializing its own values."""
        when = datetime(2026, 7, 17, 12, 0, tzinfo=timezone.utc)
        await bus.publish(test_db, 102, "custom_event", {"when": when})

        result = await test_db.execute(
            select(ClassroomEvent).where(ClassroomEvent.session_id == 102)
        )
        event = result.scalar_one()
        payload = json.loads(event.payload_json)
        assert payload["when"] == str(when)


class TestConnectionManager:
    """Uses a fresh, local ``ConnectionManager`` rather than the module-level
    singleton, so these tests can't leak state into the poller tests below — which
    must use the real singleton because ``_poll_tick`` hardcodes a reference to it."""

    async def test_broadcast_reaches_all_connected_sockets(self) -> None:
        manager = ConnectionManager()
        ws1 = FakeWebSocket()
        ws2 = FakeWebSocket()
        await manager.connect(1, ws1)
        await manager.connect(1, ws2)

        await manager.local_broadcast(1, {"type": "ping"})

        assert len(ws1.received) == 1
        assert len(ws2.received) == 1
        assert json.loads(ws1.received[0]) == {"type": "ping"}
        assert json.loads(ws2.received[0]) == {"type": "ping"}

    async def test_disconnected_socket_does_not_receive_broadcast(self) -> None:
        manager = ConnectionManager()
        ws1 = FakeWebSocket()
        ws2 = FakeWebSocket()
        await manager.connect(1, ws1)
        await manager.connect(1, ws2)

        await manager.disconnect(1, ws2)
        await manager.local_broadcast(1, {"type": "ping"})

        assert len(ws1.received) == 1
        assert len(ws2.received) == 0

    async def test_broadcast_is_scoped_to_its_own_session(self) -> None:
        manager = ConnectionManager()
        ws1 = FakeWebSocket()
        await manager.connect(1, ws1)

        await manager.local_broadcast(2, {"type": "ping"})

        assert ws1.received == []

    async def test_a_raising_socket_is_dropped_without_crashing_the_broadcast(self) -> None:
        manager = ConnectionManager()
        good = FakeWebSocket()
        bad = FakeWebSocket(fail=True)
        await manager.connect(1, good)
        await manager.connect(1, bad)

        # Must not raise, even though bad.send_text raises internally.
        await manager.local_broadcast(1, {"type": "ping"})

        assert len(good.received) == 1
        assert manager.local_connection_count(1) == 1
        assert manager.active_session_ids() == [1]


class TestPollTickCursorSeeding:
    """The single most important behavior in the poller: a session's cursor must be
    seeded to the current max event id the moment it gets its first local socket, not
    left at (or defaulted to) 0 — otherwise a freshly-connected client would be
    replayed the session's entire event history as if it were happening live now."""

    async def test_first_tick_after_connecting_seeds_without_broadcasting_history(
        self, test_db: AsyncSession
    ) -> None:
        session_id = 900001
        bus.manager._rooms.pop(session_id, None)  # defensive: clean slate for this id
        fake_ws = FakeWebSocket()
        try:
            # History published BEFORE any local socket exists for this session.
            await bus.publish(test_db, session_id, "slide_change", {"n": 1})
            await bus.publish(test_db, session_id, "slide_change", {"n": 2})
            await bus.publish(test_db, session_id, "slide_change", {"n": 3})

            # A connection appears — this worker now has a local socket for it.
            await bus.manager.connect(session_id, fake_ws)

            last_seen: dict[int, int] = {}
            await bus._poll_tick(test_db, last_seen)

            # Seeding, not streaming: nothing from before the connection should arrive.
            assert fake_ws.received == []
            assert session_id in last_seen

            max_id = await test_db.scalar(
                select(func.max(ClassroomEvent.id)).where(
                    ClassroomEvent.session_id == session_id
                )
            )
            assert last_seen[session_id] == max_id

            # Only an event published AFTER seeding should stream through, and only it.
            await bus.publish(test_db, session_id, "slide_change", {"n": 4})
            await bus._poll_tick(test_db, last_seen)

            assert len(fake_ws.received) == 1
            message = json.loads(fake_ws.received[0])
            assert message == {"type": "slide_change", "payload": {"n": 4}}
        finally:
            await bus.manager.disconnect(session_id, fake_ws)

    async def test_cursor_is_dropped_once_the_session_has_no_local_sockets(
        self, test_db: AsyncSession
    ) -> None:
        session_id = 900002
        bus.manager._rooms.pop(session_id, None)
        fake_ws = FakeWebSocket()
        try:
            await bus.manager.connect(session_id, fake_ws)
            last_seen: dict[int, int] = {}
            await bus._poll_tick(test_db, last_seen)
            assert session_id in last_seen

            await bus.manager.disconnect(session_id, fake_ws)
            await bus._poll_tick(test_db, last_seen)

            assert session_id not in last_seen
        finally:
            bus.manager._rooms.pop(session_id, None)
