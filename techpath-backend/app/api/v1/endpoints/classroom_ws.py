"""The live classroom's realtime channel — receive-only from the client's point of view.

Every state change (slide, poll, code, confusion, roster) goes through a normal REST
call, validated and persisted the same way as everything else in this codebase. This
socket exists purely to *deliver* the resulting events; it never interprets anything a
client sends over it. That keeps there being exactly one code path per action instead
of two (a REST handler and a parallel WS message handler that could drift apart), and
it means auth only has to be checked once, at connect time, not per message.

A WebSocket is pinned to whichever worker accepted it, so nothing here can rely on the
long-lived ``db`` a normal request would get from ``Depends(get_db)`` — that dependency
only commits when the endpoint function returns, which for a socket is "whenever it
closes." Every write below opens and commits its own short session instead. See
``app/services/classroom/bus.py`` for the delivery side of this.
"""
import logging
from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.crud.classroom import session_participant_crud
from app.db.session import AsyncSessionLocal
from app.models.classroom import SessionParticipant
from app.services.classroom import bus
from app.services.classroom.identity import decode_classroom_token
from app.services.classroom.roster import publish_roster_snapshot


logger = logging.getLogger(__name__)

router = APIRouter()


async def _publish_roster_snapshot_committed(session_id: int) -> None:
    """publish_roster_snapshot only flushes, matching every other write in this
    codebase — but nothing here has a get_db() dependency around it to commit on exit,
    so this owns its own session and commits explicitly."""
    async with AsyncSessionLocal() as db:
        await publish_roster_snapshot(db, session_id)
        await db.commit()


@router.websocket("/classroom/{session_id}")
async def classroom_socket(websocket: WebSocket, session_id: int) -> None:
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4401)
        return

    try:
        claims = decode_classroom_token(token, expected_session_id=session_id)
    except Exception:
        await websocket.close(code=4401)
        return

    is_student = claims["role"] == "student"
    participant_id: Optional[int] = None

    if is_student:
        async with AsyncSessionLocal() as db:
            participant = await session_participant_crud.get_by_key(
                db, session_id, claims["participant_key"]
            )
            if participant is None:
                await websocket.close(code=4401)
                return
            # 4403 is deliberately distinct from 4401: 4401 means "bad or expired
            # token" — worth an automatic reconnect, e.g. after minting a fresh one.
            # 4403 means "the trainer kicked you" — a still-valid token, but the
            # frontend must NOT auto-reconnect on this code, or a kicked student's tab
            # would silently rejoin in a loop. See SessionParticipant.is_removed and
            # get_current_participant's identical check on the REST side.
            if participant.is_removed:
                await websocket.close(code=4403)
                return
            participant_id = participant.id
            await session_participant_crud.touch(db, participant)
            await db.commit()

        await _publish_roster_snapshot_committed(session_id)

    await websocket.accept()
    await bus.manager.connect(session_id, websocket)

    try:
        while True:
            # The client never needs to send anything meaningful — this call exists so
            # Starlette can raise WebSocketDisconnect the moment the browser closes the
            # tab or loses the connection. Anything received is discarded.
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    except Exception as exc:  # noqa: BLE001 — a broken socket must not take the worker down
        logger.warning("Classroom socket error (session=%s): %s", session_id, exc)
    finally:
        await bus.manager.disconnect(session_id, websocket)

        if is_student and participant_id is not None:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(SessionParticipant).where(SessionParticipant.id == participant_id)
                )
                participant = result.scalar_one_or_none()
                if participant is not None:
                    await session_participant_crud.mark_offline(db, participant)
                    await db.commit()

            await _publish_roster_snapshot_committed(session_id)
