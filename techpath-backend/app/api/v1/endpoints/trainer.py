"""Trainer-facing endpoints.

A trainer sees only their own batches. The link is by email: the external roster carries
``trainer_email``, and it is matched against the authenticated TechPath user's email.
Admins are allowed through the same routes so they can support and demo the flow.
"""
import json
import logging
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_trainer_user
from app.core.constants import AssetType, PollStatus, SessionStatus, UserRole
from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.crud.classroom import (
    session_code_state_crud,
    session_participant_crud,
    session_poll_crud,
)
from app.crud.training import (
    asset_to_response,
    lecture_asset_crud,
    load_config,
    training_module_crud,
    training_program_crud,
)
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.db.session import get_db
from app.models.classroom import SessionParticipant
from app.models.user import User
from app.schemas.classroom import (
    ConfusionSummary,
    CreatePollRequest,
    HandRaisedEntry,
    PollFromQuizRequest,
    PollResultsResponse,
    RosterParticipant,
    RosterResponse,
    SetSlideRequest,
    StartTimerRequest,
    TimerView,
    UpdateCodeRequest,
    WsTokenResponse,
)
from app.schemas.common import MessageResponse
from app.schemas.training import (
    ModuleAssetLink,
    TrainingModuleDetail,
    TrainingModuleResponse,
)
from app.schemas.training_roster import (
    StartSessionRequest,
    TrainerBatchSummary,
    TrainingSessionCreate,
    TrainingSessionResponse,
    TrainingStudentResponse,
)
from app.services.classroom import bus
from app.services.classroom.identity import TRAINER_WS_TOKEN_MINUTES, mint_trainer_ws_token
from app.services.classroom.roster import publish_roster_snapshot


logger = logging.getLogger(__name__)

router = APIRouter()


def _session_out(session) -> TrainingSessionResponse:
    return TrainingSessionResponse(
        id=session.id,
        batch_id=session.batch_id,
        batch_name=session.batch.name if session.batch else None,
        module_id=session.module_id,
        module_title=session.module.title if session.module else None,
        title=session.title,
        scheduled_start=session.scheduled_start,
        scheduled_end=session.scheduled_end,
        status=session.status,
        join_code=session.join_code,
        started_at=session.started_at,
        ended_at=session.ended_at,
        materials_published_at=session.materials_published_at,
    )


async def _assert_owns_batch(db: AsyncSession, user: User, batch) -> None:
    """A trainer may only touch their own batches; an admin may touch any."""
    if user.role == UserRole.ADMIN.value:
        return
    if not batch.trainer_email or batch.trainer_email.lower() != user.email.lower():
        raise ForbiddenError("This batch is not assigned to you")


@router.get("/me/batches", response_model=List[TrainerBatchSummary])
async def my_batches(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> List[TrainerBatchSummary]:
    """Batches assigned to the signed-in trainer."""
    batches = await training_batch_crud.get_by_trainer_email(db, current_user.email)

    out: List[TrainerBatchSummary] = []
    for batch in batches:
        program_title = None
        module_count = 0
        if batch.program_id:
            program = await training_program_crud.get(db, batch.program_id)
            if program:
                program_title = program.title
                module_count = len(await training_module_crud.list_for_program(db, program.id))
        out.append(
            TrainerBatchSummary(
                id=batch.id,
                external_id=batch.external_id,
                name=batch.name,
                code=batch.code,
                status=batch.status,
                mode=batch.mode,
                location=batch.location,
                start_date=batch.start_date,
                end_date=batch.end_date,
                student_count=batch.student_count,
                program_id=batch.program_id,
                program_title=program_title,
                module_count=module_count,
            )
        )
    return out


@router.get("/me/sessions/today", response_model=List[TrainingSessionResponse])
async def my_sessions_today(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> List[TrainingSessionResponse]:
    """Today's sessions, plus anything already live."""
    sessions = await training_session_crud.get_today_for_trainer(db, current_user.email)
    return [_session_out(s) for s in sessions]


@router.get("/batches/{batch_id}", response_model=TrainerBatchSummary)
async def get_my_batch(
    batch_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainerBatchSummary:
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")
    await _assert_owns_batch(db, current_user, batch)

    program_title = None
    module_count = 0
    if batch.program_id:
        program = await training_program_crud.get(db, batch.program_id)
        if program:
            program_title = program.title
            module_count = len(await training_module_crud.list_for_program(db, program.id))

    return TrainerBatchSummary(
        id=batch.id,
        external_id=batch.external_id,
        name=batch.name,
        code=batch.code,
        status=batch.status,
        mode=batch.mode,
        location=batch.location,
        start_date=batch.start_date,
        end_date=batch.end_date,
        student_count=batch.student_count,
        program_id=batch.program_id,
        program_title=program_title,
        module_count=module_count,
    )


@router.get("/batches/{batch_id}/students", response_model=List[TrainingStudentResponse])
async def get_my_batch_students(
    batch_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> List[TrainingStudentResponse]:
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")
    await _assert_owns_batch(db, current_user, batch)

    students = await training_batch_crud.students(db, batch_id)
    return [TrainingStudentResponse.model_validate(s) for s in students]


@router.get("/batches/{batch_id}/modules", response_model=List[TrainingModuleResponse])
async def get_my_batch_modules(
    batch_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> List[TrainingModuleResponse]:
    """The modules available to present for this batch, via its linked programme."""
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")
    await _assert_owns_batch(db, current_user, batch)

    if not batch.program_id:
        return []

    modules = await training_module_crud.list_for_program(db, batch.program_id)
    counts = await training_module_crud.asset_counts(db, [m.id for m in modules])
    return [
        TrainingModuleResponse(
            id=m.id,
            program_id=m.program_id,
            title=m.title,
            slug=m.slug,
            description=m.description,
            display_order=m.display_order,
            estimated_minutes=m.estimated_minutes,
            status=m.status,
            asset_count=counts.get(m.id, 0),
            created_at=m.created_at,
            updated_at=m.updated_at,
        )
        for m in modules
    ]


@router.get("/modules/{module_id}", response_model=TrainingModuleDetail)
async def get_module_for_trainer(
    module_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingModuleDetail:
    """Module detail with assets. Access is allowed if the module belongs to a
    programme linked to any of the trainer's batches (or user is admin)."""
    module = await training_module_crud.get_with_assets(db, module_id)
    if not module:
        raise NotFoundError("Module")

    if current_user.role != UserRole.ADMIN.value:
        batches = await training_batch_crud.get_by_trainer_email(db, current_user.email)
        allowed_program_ids = {b.program_id for b in batches if b.program_id}
        if module.program_id not in allowed_program_ids:
            raise ForbiddenError("This module is not part of your assigned programmes")

    assets = [
        ModuleAssetLink(
            id=link.id,
            asset_id=link.asset_id,
            display_order=link.display_order,
            is_required=link.is_required,
            notes=link.notes,
            asset=await asset_to_response(db, link.asset),
        )
        for link in module.asset_links
    ]
    return TrainingModuleDetail(
        id=module.id,
        program_id=module.program_id,
        title=module.title,
        slug=module.slug,
        description=module.description,
        display_order=module.display_order,
        estimated_minutes=module.estimated_minutes,
        status=module.status,
        asset_count=len(assets),
        created_at=module.created_at,
        updated_at=module.updated_at,
        assets=assets,
    )


@router.get("/batches/{batch_id}/sessions", response_model=List[TrainingSessionResponse])
async def list_batch_sessions(
    batch_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> List[TrainingSessionResponse]:
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")
    await _assert_owns_batch(db, current_user, batch)

    sessions = await training_session_crud.list_for_batch(db, batch_id)
    for s in sessions:
        s.batch = batch
    return [_session_out(s) for s in sessions]


@router.post(
    "/sessions", response_model=TrainingSessionResponse, status_code=status.HTTP_201_CREATED
)
async def create_session(
    payload: TrainingSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    batch = await training_batch_crud.get(db, payload.batch_id)
    if not batch:
        raise NotFoundError("Batch")
    await _assert_owns_batch(db, current_user, batch)

    if payload.module_id is not None:
        module = await training_module_crud.get(db, payload.module_id)
        if not module:
            raise NotFoundError("Module")
        if batch.program_id and module.program_id != batch.program_id:
            raise ValidationError("That module belongs to a different training programme")

    session = await training_session_crud.create(
        db,
        obj_in={
            "batch_id": payload.batch_id,
            "module_id": payload.module_id,
            "trainer_user_id": current_user.id,
            "title": payload.title,
            "scheduled_start": payload.scheduled_start,
            "scheduled_end": payload.scheduled_end,
            "status": SessionStatus.SCHEDULED.value,
        },
    )
    session = await training_session_crud.get_with_relations(db, session.id)
    return _session_out(session)


@router.get("/sessions/{session_id}", response_model=TrainingSessionResponse)
async def get_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)
    return _session_out(session)


@router.post("/sessions/{session_id}/start", response_model=TrainingSessionResponse)
async def start_session(
    session_id: int,
    payload: StartSessionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    """Begin presenting: flip to live and mint the join code students will use.

    The live classroom transport does not exist yet, so this establishes the session
    and its code and nothing more.
    """
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    if session.status == SessionStatus.ENDED.value:
        raise ValidationError("This session has already ended")

    module_id = payload.module_id or session.module_id
    if module_id is None:
        raise ValidationError("Choose a module to present before starting")

    module = await training_module_crud.get(db, module_id)
    if not module:
        raise NotFoundError("Module")
    if session.batch.program_id and module.program_id != session.batch.program_id:
        raise ValidationError("That module belongs to a different training programme")

    # Restarting a live session must not invalidate the code students already typed in.
    if session.status != SessionStatus.LIVE.value:
        session.join_code = await training_session_crud.generate_join_code(db)
        session.started_at = datetime.now(timezone.utc)
        session.status = SessionStatus.LIVE.value

    session.module_id = module_id
    session.trainer_user_id = current_user.id
    db.add(session)
    await db.flush()

    session = await training_session_crud.get_with_relations(db, session_id)
    logger.info("Session %s went live (batch=%s)", session_id, session.batch_id)
    return _session_out(session)


@router.post("/sessions/{session_id}/end", response_model=TrainingSessionResponse)
async def end_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    """Finish presenting and release the join code back to the pool."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    session.status = SessionStatus.ENDED.value
    session.ended_at = datetime.now(timezone.utc)
    session.join_code = None
    db.add(session)
    await db.flush()

    # Otherwise a student's screen just goes silent with no explanation — nothing else
    # tells them the trainer walked away rather than the connection dropping.
    open_poll = await session_poll_crud.get_open_poll(db, session_id)
    if open_poll:
        open_poll.status = PollStatus.CLOSED.value
        open_poll.closed_at = datetime.now(timezone.utc)
        db.add(open_poll)
        await db.flush()
    await bus.publish(db, session_id, "session_ended", {})

    session = await training_session_crud.get_with_relations(db, session_id)
    return _session_out(session)


@router.post("/sessions/{session_id}/materials/publish", response_model=TrainingSessionResponse)
async def publish_materials(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    """Whole-session publish switch for the student portal (``student_portal.py``) —
    every asset in the module this session used becomes visible to everyone who
    attended, in one action. Only meaningful once the class actually happened; gating
    on ``ended`` also means a student can never see this session listed until the
    trainer has had a chance to review it."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    if session.status != SessionStatus.ENDED.value:
        raise ValidationError("End the session before publishing its materials")

    session.materials_published_at = datetime.now(timezone.utc)
    session.materials_published_by_user_id = current_user.id
    db.add(session)
    await db.flush()

    session = await training_session_crud.get_with_relations(db, session_id)
    return _session_out(session)


@router.post("/sessions/{session_id}/materials/unpublish", response_model=TrainingSessionResponse)
async def unpublish_materials(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    """Revokes portal access immediately — not status-gated like publish, since taking
    materials back should always be available, not just while a session is in some
    particular state."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    session.materials_published_at = None
    session.materials_published_by_user_id = None
    db.add(session)
    await db.flush()

    session = await training_session_crud.get_with_relations(db, session_id)
    return _session_out(session)


@router.post("/sessions/{session_id}/ws-token", response_model=WsTokenResponse)
async def mint_session_ws_token(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> WsTokenResponse:
    """A native WebSocket handshake can't carry an Authorization header — only a query
    string — so this hands out a short-lived, session-scoped token for that one purpose
    instead of ever putting the real Firebase ID token in a URL."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    token = mint_trainer_ws_token(
        session_id=session_id, user_id=current_user.id, display_name=current_user.name
    )
    return WsTokenResponse(token=token, expires_in_minutes=TRAINER_WS_TOKEN_MINUTES)


@router.post("/sessions/{session_id}/slide", response_model=TrainingSessionResponse)
async def set_current_slide(
    session_id: int,
    payload: SetSlideRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    """Change what students see. Broadcasts the full asset payload so a client renders
    immediately, with no follow-up fetch on the critical path."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    asset = await lecture_asset_crud.get(db, payload.asset_id)
    if asset is None:
        raise NotFoundError("Lecture asset")

    session.current_asset_id = asset.id
    db.add(session)
    await db.flush()

    asset_payload = await asset_to_response(db, asset)
    await bus.publish(
        db, session_id, "slide_change", {"asset": asset_payload.model_dump(mode="json")}
    )

    session = await training_session_crud.get_with_relations(db, session_id)
    return _session_out(session)


@router.get("/sessions/{session_id}/polls/{poll_id}", response_model=PollResultsResponse)
async def get_poll_results(
    session_id: int,
    poll_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> PollResultsResponse:
    """Live tally while a poll is still open. Unlike the student-facing endpoint,
    results here are never withheld — the bias risk that gates them per-participant
    while voting is live doesn't apply to the trainer, who isn't a voter."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    poll = await session_poll_crud.get(db, poll_id)
    if not poll or poll.session_id != session_id:
        raise NotFoundError("Poll")

    results = await session_poll_crud.tally(db, poll_id)
    return PollResultsResponse(
        id=poll.id,
        question=poll.question,
        options=json.loads(poll.options_json),
        status=poll.status,
        results=results,
        total_votes=sum(results.values()),
        correct_option_index=poll.correct_option_index,
        created_at=poll.created_at,
        closed_at=poll.closed_at,
    )


@router.post(
    "/sessions/{session_id}/polls",
    response_model=PollResultsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_poll(
    session_id: int,
    payload: CreatePollRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> PollResultsResponse:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    # At most one open poll at a time — opening a new one while another is live almost
    # always means the trainer wants to move on, and two simultaneous polls is a
    # confusing thing to hand a student's screen.
    existing = await session_poll_crud.get_open_poll(db, session_id)
    if existing:
        existing.status = PollStatus.CLOSED.value
        existing.closed_at = datetime.now(timezone.utc)
        db.add(existing)
        await db.flush()

    poll = await session_poll_crud.create(
        db,
        obj_in={
            "session_id": session_id,
            "question": payload.question,
            "options_json": json.dumps(payload.options),
            "status": PollStatus.OPEN.value,
        },
    )

    await bus.publish(
        db,
        session_id,
        "poll_open",
        {"id": poll.id, "question": poll.question, "options": payload.options},
    )

    return PollResultsResponse(
        id=poll.id,
        question=poll.question,
        options=payload.options,
        status=poll.status,
        results={},
        total_votes=0,
        created_at=poll.created_at,
        closed_at=None,
    )


@router.post(
    "/sessions/{session_id}/polls/from-quiz",
    response_model=PollResultsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_poll_from_quiz(
    session_id: int,
    payload: PollFromQuizRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> PollResultsResponse:
    """Same close-existing/open-new flow as ``create_poll``, seeded from one question of
    a quiz lecture asset instead of trainer-typed text — see ``PollFromQuizRequest``."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    asset = await lecture_asset_crud.get(db, payload.asset_id)
    if asset is None:
        raise NotFoundError("Lecture asset")
    if asset.asset_type != AssetType.QUIZ.value:
        raise ValidationError("That asset isn't a quiz")

    config = load_config(asset.config_json) or {}
    questions = config.get("questions") or []
    if payload.question_index >= len(questions):
        raise ValidationError("That question doesn't exist on this quiz")

    question = questions[payload.question_index]
    options = question["options"]

    existing = await session_poll_crud.get_open_poll(db, session_id)
    if existing:
        existing.status = PollStatus.CLOSED.value
        existing.closed_at = datetime.now(timezone.utc)
        db.add(existing)
        await db.flush()

    poll = await session_poll_crud.create(
        db,
        obj_in={
            "session_id": session_id,
            "question": question["question"],
            "options_json": json.dumps(options),
            "status": PollStatus.OPEN.value,
            "correct_option_index": question["correct_index"],
        },
    )

    # Question and options only — the correct answer never goes out on the open-poll
    # broadcast, or a student could read it straight off the wire before voting. It only
    # ever reaches a client via the trainer-only responses here and the post-close
    # broadcast in close_poll, once voting is no longer possible.
    await bus.publish(
        db,
        session_id,
        "poll_open",
        {"id": poll.id, "question": poll.question, "options": options},
    )

    return PollResultsResponse(
        id=poll.id,
        question=poll.question,
        options=options,
        status=poll.status,
        results={},
        total_votes=0,
        correct_option_index=poll.correct_option_index,
        created_at=poll.created_at,
        closed_at=None,
    )


@router.post("/sessions/{session_id}/polls/{poll_id}/close", response_model=PollResultsResponse)
async def close_poll(
    session_id: int,
    poll_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> PollResultsResponse:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    poll = await session_poll_crud.get(db, poll_id)
    if not poll or poll.session_id != session_id:
        raise NotFoundError("Poll")

    poll.status = PollStatus.CLOSED.value
    poll.closed_at = datetime.now(timezone.utc)
    db.add(poll)
    await db.flush()

    results = await session_poll_crud.tally(db, poll_id)
    options = json.loads(poll.options_json)

    # Unlike while open, results are broadcast to everyone unconditionally once closed —
    # the bias risk that gates results per-participant while voting is live is gone the
    # moment voting stops. correct_option_index travels with it for the same reason: once
    # nobody can vote anymore, revealing the right answer (for a quiz-launched poll; null
    # and a no-op for an ordinary one) is exactly what a results view is for.
    await bus.publish(
        db,
        session_id,
        "poll_closed",
        {
            "id": poll.id,
            "results": results,
            "total_votes": sum(results.values()),
            "correct_option_index": poll.correct_option_index,
        },
    )

    return PollResultsResponse(
        id=poll.id,
        question=poll.question,
        options=options,
        status=poll.status,
        results=results,
        total_votes=sum(results.values()),
        correct_option_index=poll.correct_option_index,
        created_at=poll.created_at,
        closed_at=poll.closed_at,
    )


@router.post("/sessions/{session_id}/code", response_model=MessageResponse)
async def update_live_code(
    session_id: int,
    payload: UpdateCodeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> MessageResponse:
    """Broadcast the trainer's live-coding buffer. The client is expected to debounce
    keystrokes before calling this — see the presenter's code panel."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    await session_code_state_crud.upsert(
        db, session_id=session_id, language=payload.language, content=payload.content
    )
    await bus.publish(
        db, session_id, "code_update", {"language": payload.language, "content": payload.content}
    )
    return MessageResponse(message="Broadcast")


@router.get("/sessions/{session_id}/roster", response_model=RosterResponse)
async def get_roster(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> RosterResponse:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    participants = await session_participant_crud.list_for_session(db, session_id)
    summary = await session_participant_crud.confusion_summary(db, session_id)
    hands_raised = await session_participant_crud.hands_raised_queue(db, session_id)

    timer = None
    if session.timer_started_at and session.timer_duration_seconds:
        timer = TimerView(
            duration_seconds=session.timer_duration_seconds,
            started_at=session.timer_started_at,
        )

    return RosterResponse(
        participants=[RosterParticipant.model_validate(p) for p in participants],
        confusion=ConfusionSummary(**summary),
        hands_raised=[
            HandRaisedEntry(
                participant_id=p.id,
                display_name=p.display_name,
                hand_raised_at=p.hand_raised_at,
            )
            for p in hands_raised
        ],
        timer=timer,
    )


async def _get_owned_participant(
    db: AsyncSession, current_user: User, session_id: int, participant_id: int
) -> SessionParticipant:
    """Shared lookup for the per-participant trainer actions below: confirms the
    session belongs to this trainer, then confirms the participant belongs to that
    session — the same two-step scoping every other session-scoped route here does."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    participant = await session_participant_crud.get(db, participant_id)
    if not participant or participant.session_id != session_id:
        raise NotFoundError("Participant")
    return participant


@router.post(
    "/sessions/{session_id}/participants/{participant_id}/kick",
    response_model=MessageResponse,
)
async def kick_participant(
    session_id: int,
    participant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> MessageResponse:
    """Removes a participant and revokes their session token going forward (see
    SessionParticipant.is_removed, enforced in classroom.py's get_current_participant
    and classroom_ws.py's connect handler — this endpoint only flips the flag)."""
    participant = await _get_owned_participant(db, current_user, session_id, participant_id)

    await session_participant_crud.kick(db, participant)
    await publish_roster_snapshot(db, session_id)
    # Carries participant_key, not the numeric id: that's what a student's browser holds
    # locally to recognise "this event is about me" and react (e.g. show a removed
    # screen, stop reconnecting).
    await bus.publish(
        db, session_id, "participant_kicked", {"participant_key": participant.participant_key}
    )

    return MessageResponse(message="Participant removed")


@router.post(
    "/sessions/{session_id}/participants/{participant_id}/lower-hand",
    response_model=MessageResponse,
)
async def lower_participant_hand(
    session_id: int,
    participant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> MessageResponse:
    """Trainer-initiated equivalent of a student lowering their own hand — e.g. after
    calling on them. Same CRUD method the student endpoint uses."""
    participant = await _get_owned_participant(db, current_user, session_id, participant_id)

    await session_participant_crud.set_hand_raised(db, participant, False)
    await publish_roster_snapshot(db, session_id)

    return MessageResponse(message="Hand lowered")


@router.post("/sessions/{session_id}/timer/start", response_model=MessageResponse)
async def start_timer(
    session_id: int,
    payload: StartTimerRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> MessageResponse:
    """Starts (or restarts) a countdown broadcast to every client. Persisted on the
    session, not just broadcast, so a client bootstrapping mid-countdown (GET
    /classroom/{id}/state or the trainer's GET .../roster) can compute remaining time
    itself instead of depending on having seen the event live."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    started_at = datetime.now(timezone.utc)
    session.timer_started_at = started_at
    session.timer_duration_seconds = payload.duration_seconds
    db.add(session)
    await db.flush()

    await bus.publish(
        db,
        session_id,
        "timer_started",
        {
            "duration_seconds": payload.duration_seconds,
            "started_at": started_at.isoformat(),
        },
    )
    return MessageResponse(message="Timer started")


@router.post("/sessions/{session_id}/timer/cancel", response_model=MessageResponse)
async def cancel_timer(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> MessageResponse:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    session.timer_started_at = None
    session.timer_duration_seconds = None
    db.add(session)
    await db.flush()

    await bus.publish(db, session_id, "timer_cancelled", {})
    return MessageResponse(message="Timer cancelled")
