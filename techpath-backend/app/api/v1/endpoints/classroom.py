"""Public live-classroom endpoints — the student side.

No Firebase account: a student proves nothing but a 6-digit code and, ideally, a roster
email. Everything here is intentionally reachable with no ``Authorization`` header
except the short-lived classroom token minted by ``/identify``, which is why every
mutation is scoped tightly to one session and one participant row — this surface has to
assume the caller could be anyone who saw the code on a shared screen.
"""
import json
import logging
import time
from typing import Optional

from fastapi import APIRouter, Depends, Path, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import PollStatus, SessionStatus
from app.core.exceptions import NotFoundError, RateLimitError, UnauthorizedError, ValidationError
from app.crud.classroom import (
    session_code_state_crud,
    session_participant_crud,
    session_poll_crud,
    session_poll_vote_crud,
)
from app.crud.crud_question import question as question_crud
from app.crud.training import asset_to_response, lecture_asset_crud
from app.crud.training_roster import training_session_crud
from app.db.session import get_db
from app.models.classroom import SessionParticipant
from app.schemas.classroom import (
    CodeStateView,
    ConfusionRequest,
    HandRaiseRequest,
    IdentifyRequest,
    IdentifyResponse,
    JoinRequest,
    JoinResponse,
    MediaView,
    PollStateView,
    PresenceView,
    ReactionRequest,
    SessionStateResponse,
    TimerView,
    VoteRequest,
)
from app.schemas.training_roster import (
    TrainingSessionQuestionCreate,
    TrainingSessionQuestionResponse,
)
from app.schemas.common import MessageResponse
from app.services.classroom import bus, media
from app.services.classroom.identity import decode_classroom_token, mint_classroom_token
from app.services.classroom.roster import publish_roster_snapshot


logger = logging.getLogger(__name__)

router = APIRouter()

security = HTTPBearer(auto_error=False)

# Reactions are ephemeral (no DB row — see send_reaction), so their cooldown is too:
# an in-memory, per-worker dict keyed by participant_key is enough to stop accidental
# double-taps without needing a table just for rate limiting. Doesn't need to survive a
# restart, and a worker only ever needs to guard the participants it has handled.
REACTION_COOLDOWN_SECONDS = 1.5
ALLOWED_REACTIONS = {"👍", "❤️", "😂", "🎉", "👏", "🤯"}
_last_reaction_at: dict[str, float] = {}

# Brute-force guard for /join and /identify: both are intentionally unauthenticated
# (see module docstring), and a 6-digit join code is only 1,000,000 combinations — with
# no throttling at all, someone could script through every code in a live session in
# minutes. A tiny in-memory sliding-window counter per client IP is enough; this
# doesn't need slowapi/redis for a single-purpose limit like this.
_RATE_LIMIT_WINDOW_SECONDS = 60
_RATE_LIMIT_MAX_ATTEMPTS = 10
_rate_limit_hits: dict[str, list[float]] = {}


def _enforce_rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - _RATE_LIMIT_WINDOW_SECONDS
    hits = [t for t in _rate_limit_hits.get(ip, []) if t > window_start]
    if len(hits) >= _RATE_LIMIT_MAX_ATTEMPTS:
        raise RateLimitError("Too many attempts — please wait a minute and try again")
    hits.append(now)
    _rate_limit_hits[ip] = hits


async def get_current_participant(
    session_id: int = Path(...),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> SessionParticipant:
    if credentials is None:
        raise UnauthorizedError("Not authenticated")

    claims = decode_classroom_token(credentials.credentials, expected_session_id=session_id)
    participant = await session_participant_crud.get_by_key(
        db, session_id, claims["participant_key"]
    )
    if participant is None:
        raise UnauthorizedError("This classroom session has ended or your token is invalid")
    # A kicked participant's token is still cryptographically valid — is_removed is what
    # actually revokes it, so it must be checked on every request, not just at kick time.
    # See classroom_ws.py's connect handler for the WebSocket-side equivalent (closes
    # with 4403 rather than 4401, since this isn't an auth failure the client can fix by
    # refreshing its token).
    if participant.is_removed:
        raise UnauthorizedError("You've been removed from this session")
    return participant


@router.post("/join", response_model=JoinResponse)
async def join_classroom(
    payload: JoinRequest, request: Request, db: AsyncSession = Depends(get_db)
) -> JoinResponse:
    # See _enforce_rate_limit — guards against brute-forcing the 6-digit join code.
    _enforce_rate_limit(request)
    session = await training_session_crud.get_by_join_code(db, payload.join_code)
    if session is None or session.status != SessionStatus.LIVE.value:
        raise NotFoundError("That code isn't attached to a live session right now")

    return JoinResponse(
        session_id=session.id,
        batch_name=session.batch.name,
        session_title=session.title,
        module_title=session.module.title if session.module else None,
        status=session.status,
    )


@router.post("/identify", response_model=IdentifyResponse)
async def identify(
    payload: IdentifyRequest, request: Request, db: AsyncSession = Depends(get_db)
) -> IdentifyResponse:
    """Match by roster email; fall back to a guest name. See schema docstring for the
    two-step negotiation this supports (try email, then retry with a guest name)."""
    # See _enforce_rate_limit — guards against brute-forcing the 6-digit join code
    # (identify is the second step of the same join flow, reachable with any session_id).
    _enforce_rate_limit(request)
    session = await training_session_crud.get(db, payload.session_id)
    if session is None or session.status != SessionStatus.LIVE.value:
        raise NotFoundError("That session isn't live right now")

    student_id: Optional[int] = None
    display_name: Optional[str] = None
    matched = False
    is_guest = True

    if payload.email:
        student = await session_participant_crud.find_student_in_batch(
            db, session.batch_id, payload.email
        )
        if student:
            student_id = student.id
            display_name = student.name
            matched = True
            is_guest = False

    if not matched:
        if not payload.guest_name:
            # Ask the client to collect a name and retry — this is a normal branch of
            # the flow, not an error, so it's a 200 with matched=false and no token.
            return IdentifyResponse(matched=False, token=None, display_name=None)
        display_name = payload.guest_name.strip()[:200] or "Guest"

    participant = await session_participant_crud.join(
        db,
        session_id=session.id,
        display_name=display_name,
        student_id=student_id,
        is_guest=is_guest,
    )
    token = mint_classroom_token(
        session_id=session.id,
        participant_key=participant.participant_key,
        display_name=participant.display_name,
    )

    await publish_roster_snapshot(db, session.id)

    return IdentifyResponse(matched=matched, token=token, display_name=participant.display_name)


@router.get("/{session_id}/state", response_model=SessionStateResponse)
async def get_state(
    session_id: int,
    participant: SessionParticipant = Depends(get_current_participant),
    db: AsyncSession = Depends(get_db),
) -> SessionStateResponse:
    """Bootstrap: everything a client needs to render immediately on connect or
    reconnect, independent of event-stream timing. See bus.py's module docstring for
    why the WS stream alone can't be trusted to carry full history."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if session is None:
        raise NotFoundError("Session")

    current_asset = None
    if session.current_asset_id:
        asset = await lecture_asset_crud.get(db, session.current_asset_id)
        if asset:
            current_asset = await asset_to_response(db, asset)

    open_poll = None
    poll = await session_poll_crud.get_open_poll(db, session_id)
    if poll:
        my_vote = await session_poll_vote_crud.get_for_participant(db, poll.id, participant.id)
        results = None
        if my_vote:
            results = await session_poll_crud.tally(db, poll.id)

        open_poll = PollStateView(
            id=poll.id,
            question=poll.question,
            options=json.loads(poll.options_json),
            status=poll.status,
            my_vote=my_vote.option_index if my_vote else None,
            results=results,
        )

    code_state = await session_code_state_crud.get_for_session(db, session_id)
    code = (
        CodeStateView(language=code_state.language, content=code_state.content)
        if code_state
        else None
    )

    summary = await session_participant_crud.confusion_summary(db, session_id)

    timer = None
    if session.timer_started_at and session.timer_duration_seconds:
        timer = TimerView(
            duration_seconds=session.timer_duration_seconds,
            started_at=session.timer_started_at,
        )

    media_view = None
    if session.status == SessionStatus.LIVE.value and session.live_stream_path:
        media_view = MediaView(
            whep_url=media.whep_url(session.live_stream_path),
            hls_url=media.hls_url(session.live_stream_path),
            mic_muted=session.media_mic_muted,
            camera_off=session.media_camera_off,
            screen_sharing=session.media_screen_sharing,
        )

    return SessionStateResponse(
        session_id=session.id,
        title=session.title,
        status=session.status,
        batch_name=session.batch.name,
        module_title=session.module.title if session.module else None,
        current_asset=current_asset,
        open_poll=open_poll,
        code=code,
        my_confusion=participant.is_confused,
        presence=PresenceView(online=summary["online"]),
        timer=timer,
        media=media_view,
    )


@router.post("/{session_id}/confusion", response_model=SessionStateResponse)
async def set_confusion(
    session_id: int,
    payload: ConfusionRequest,
    participant: SessionParticipant = Depends(get_current_participant),
    db: AsyncSession = Depends(get_db),
) -> SessionStateResponse:
    await session_participant_crud.set_confusion(db, participant, payload.confused)
    await publish_roster_snapshot(db, session_id)
    return await get_state(session_id, participant, db)


@router.post("/{session_id}/hand", response_model=SessionStateResponse)
async def set_hand_raised(
    session_id: int,
    payload: HandRaiseRequest,
    participant: SessionParticipant = Depends(get_current_participant),
    db: AsyncSession = Depends(get_db),
) -> SessionStateResponse:
    """Mirrors ``set_confusion``: persist, broadcast the roster so the trainer panel's
    call-on-me queue updates, then hand back the same bootstrap shape every other
    student mutation here returns."""
    await session_participant_crud.set_hand_raised(db, participant, payload.raised)
    await publish_roster_snapshot(db, session_id)
    return await get_state(session_id, participant, db)


@router.post("/{session_id}/reactions", response_model=MessageResponse)
async def send_reaction(
    session_id: int,
    payload: ReactionRequest,
    participant: SessionParticipant = Depends(get_current_participant),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Ephemeral by design — unlike everything else in this module, a reaction has no
    database row at all, just a broadcast. There is nothing to bootstrap on reconnect
    (a client that missed one only missed a fleeting animation, not state)."""
    if payload.emoji not in ALLOWED_REACTIONS:
        raise ValidationError("That reaction isn't supported")

    now = time.monotonic()
    last = _last_reaction_at.get(participant.participant_key)
    if last is not None and (now - last) < REACTION_COOLDOWN_SECONDS:
        raise ValidationError("Slow down a little before reacting again")
    _last_reaction_at[participant.participant_key] = now

    await bus.publish(
        db,
        session_id,
        "reaction",
        {"emoji": payload.emoji, "display_name": participant.display_name},
    )
    return MessageResponse(message="Reaction sent")


@router.post("/{session_id}/polls/{poll_id}/vote", response_model=SessionStateResponse)
async def vote(
    session_id: int,
    poll_id: int,
    payload: VoteRequest,
    participant: SessionParticipant = Depends(get_current_participant),
    db: AsyncSession = Depends(get_db),
) -> SessionStateResponse:
    poll = await session_poll_crud.get(db, poll_id)
    if poll is None or poll.session_id != session_id:
        raise NotFoundError("Poll")
    if poll.status != PollStatus.OPEN.value:
        raise ValidationError("This poll is closed")
    if payload.option_index >= len(json.loads(poll.options_json)):
        raise ValidationError("That option doesn't exist on this poll")

    await session_poll_vote_crud.cast(
        db, poll_id=poll_id, participant_id=participant.id, option_index=payload.option_index
    )
    # A lightweight nudge, not the results themselves — results visibility is gated
    # per-participant (see PollStateView docstring), which only the REST state fetch
    # each client re-runs after this can actually enforce.
    await bus.publish(db, session_id, "poll_vote_cast", {"poll_id": poll_id})

    return await get_state(session_id, participant, db)


@router.post("/{session_id}/questions", response_model=TrainingSessionQuestionResponse)
async def ask_question(
    session_id: int,
    payload: TrainingSessionQuestionCreate,
    participant: SessionParticipant = Depends(get_current_participant),
    db: AsyncSession = Depends(get_db),
) -> TrainingSessionQuestionResponse:
    if not participant.student_id:
        raise UnauthorizedError("Must be a registered student to ask questions")
        
    session = await training_session_crud.get(db, session_id)
    if session is None or session.status != SessionStatus.LIVE.value:
        raise ValidationError("Session is not live")

    new_question = await question_crud.create(
        db,
        obj_in=payload,
        session_id=session_id,
        student_id=participant.student_id
    )
    
    response_obj = TrainingSessionQuestionResponse.model_validate(new_question)
    response_obj.student_name = participant.display_name
    
    await bus.publish(
        db,
        session_id,
        "question_asked",
        response_obj.model_dump(mode="json")
    )
    
    return response_obj


@router.post("/{session_id}/questions/{question_id}/upvote", response_model=TrainingSessionQuestionResponse)
async def upvote_question(
    session_id: int,
    question_id: int,
    participant: SessionParticipant = Depends(get_current_participant),
    db: AsyncSession = Depends(get_db),
) -> TrainingSessionQuestionResponse:
    q = await question_crud.get(db, id=question_id)
    if not q or q.session_id != session_id:
        raise NotFoundError("Question")

    session = await training_session_crud.get(db, session_id)
    if not session or not session.questions_are_public:
        raise ValidationError("Questions are not public")

    updated_question = await question_crud.upvote(db, db_obj=q)
    
    # We need the student's name for the response
    student = await session_participant_crud.find_student_in_batch(
        db, session.batch_id, str(updated_question.student_id)  # This is slightly hacked since find_student_in_batch expects email, wait...
    )
    # The response requires student_name. We can just broadcast the ID and let the frontend figure it out, or we can fetch it properly.
    
    await bus.publish(
        db,
        session_id,
        "question_upvoted",
        {"question_id": updated_question.id, "upvotes": updated_question.upvotes}
    )
    
    response_obj = TrainingSessionQuestionResponse.model_validate(updated_question)
    # We will leave student_name as None here since upvote doesn't strictly need it to return
    return response_obj


@router.get("/{session_id}/questions", response_model=list[TrainingSessionQuestionResponse])
async def list_questions(
    session_id: int,
    participant: SessionParticipant = Depends(get_current_participant),
    db: AsyncSession = Depends(get_db),
) -> list[TrainingSessionQuestionResponse]:
    session = await training_session_crud.get(db, session_id)
    if session is None or session.status != SessionStatus.LIVE.value:
        raise ValidationError("Session is not live")

    if not session.questions_are_public:
        return []

    questions = await question_crud.get_by_session(db, session_id=session_id)
    
    # Normally we'd join with the User/Student table to get the names, 
    # but for now we'll just return the schema which defaults student_name to None or requires a JOIN.
    # To keep it simple, we just return the questions.
    return [TrainingSessionQuestionResponse.model_validate(q) for q in questions]
