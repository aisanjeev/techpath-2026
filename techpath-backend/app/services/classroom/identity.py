"""Classroom identity tokens.

A student never gets a Firebase account — the plan settled on a 6-digit join code plus
a roster-email match instead. What they get after identifying is a short-lived signed
token (the same JWT machinery ``app/core/security.py`` already uses for admin/trainer
sessions, just with a ``classroom`` type claim so it can never be mistaken for one).
``sub`` is the participant's ``participant_key`` — a UUID minted once at identify-time
and reused across reconnects, which is what poll votes and confusion state are keyed
against, matched or guest alike.

The trainer side of the WebSocket uses the same token shape with ``role="trainer"``,
minted separately by ``POST /trainer/sessions/{id}/ws-token`` — a browser's native
WebSocket handshake can't carry an Authorization header, only a query string, and
putting the trainer's actual Firebase ID token in a URL means it lands in access logs.
This token is scoped to one session, expires in minutes, and is worthless for anything
but opening that one socket.
"""
from datetime import timedelta
from typing import Literal, TypedDict

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, decode_access_token

STUDENT_TOKEN_HOURS = 10
TRAINER_WS_TOKEN_MINUTES = 15

Role = Literal["student", "trainer"]


class ClassroomClaims(TypedDict):
    participant_key: str
    session_id: int
    name: str
    role: Role


def mint_classroom_token(*, session_id: int, participant_key: str, display_name: str) -> str:
    return create_access_token(
        data={
            "sub": participant_key,
            "session_id": session_id,
            "name": display_name,
            "type": "classroom",
            "role": "student",
        },
        expires_delta=timedelta(hours=STUDENT_TOKEN_HOURS),
    )


def mint_trainer_ws_token(*, session_id: int, user_id: int, display_name: str) -> str:
    return create_access_token(
        data={
            "sub": f"trainer:{user_id}",
            "session_id": session_id,
            "name": display_name,
            "type": "classroom",
            "role": "trainer",
        },
        expires_delta=timedelta(minutes=TRAINER_WS_TOKEN_MINUTES),
    )


def decode_classroom_token(token: str, *, expected_session_id: int) -> ClassroomClaims:
    payload = decode_access_token(token)
    if payload.get("type") != "classroom":
        raise UnauthorizedError("Not a classroom token")
    if payload.get("session_id") != expected_session_id:
        raise UnauthorizedError("Token is not valid for this session")
    participant_key = payload.get("sub")
    if not participant_key:
        raise UnauthorizedError("Invalid classroom token")
    return ClassroomClaims(
        participant_key=participant_key,
        session_id=payload["session_id"],
        name=payload.get("name", ""),
        role=payload.get("role", "student"),
    )
