"""Trainer-facing endpoints.

A trainer sees only their own batches. The link is by email: the external roster carries
``trainer_email``, and it is matched against the authenticated TechPath user's email.
Admins are allowed through the same routes so they can support and demo the flow.
"""
import json
import logging
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_trainer_user
from app.core.constants import AssetType, PollStatus, RecordingStatus, SessionStatus, UserRole
from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.crud.classroom import (
    session_code_state_crud,
    session_participant_crud,
    session_poll_crud,
    session_recording_crud,
)
from app.crud.training import (
    asset_to_response,
    lecture_asset_crud,
    load_config,
    training_module_crud,
    training_program_crud,
)
from app.crud.crud_question import question as question_crud
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.db.session import get_db
from app.models.classroom import SessionParticipant
from app.models.user import User
from app.schemas.classroom import (
    ConfusionSummary,
    CreatePollRequest,
    HandRaisedEntry,
    MediaStateRequest,
    MediaView,
    PollFromQuizRequest,
    PollResultsResponse,
    RecordingView,
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
    LectureAssetResponse,
)
from app.schemas.training_roster import (
    StartSessionRequest,
    TrainerBatchSummary,
    TrainingSessionCreate,
    TrainingSessionResponse,
    TrainingStudentResponse,
    ToggleRecordingRequest,
    ToggleQuestionsPublicRequest,
    TrainingSessionQuestionResponse,
    BatchProgramSummary,
)
from app.services.classroom import bus, media
from app.services.classroom.identity import TRAINER_WS_TOKEN_MINUTES, mint_trainer_ws_token
from app.services.classroom.roster import publish_roster_snapshot


logger = logging.getLogger(__name__)

router = APIRouter()


def _trainer_media_view(session) -> Optional[MediaView]:
    """Trainer-facing media block: whip_url only, only while there's a stream path to
    publish to (i.e. the session has gone live at least once since it last ended)."""
    if not session.live_stream_path:
        return None
    return MediaView(
        whip_url=media.whip_url(session.live_stream_path),
        broadcasting=session.media_broadcasting,
        mic_muted=session.media_mic_muted,
        camera_off=session.media_camera_off,
        screen_sharing=session.media_screen_sharing,
    )


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
        keep_recording=session.keep_recording,
        materials_published_at=session.materials_published_at,
        media=_trainer_media_view(session),
    )


def _effective_email(user: User, impersonate: Optional[str]) -> str:
    """The trainer email to scope queries to.

    Admins may pass ``X-Impersonate-Email`` to see the portal as a specific
    trainer.  Without it an admin sees all batches (returns empty string as a
    sentinel the callers check).  Non-admins always use their own email.
    """
    if user.role == UserRole.ADMIN.value:
        return (impersonate or "").strip().lower()
    return user.email.lower()


async def _assert_owns_batch(
    db: AsyncSession, user: User, batch, *, impersonate: Optional[str] = None
) -> None:
    """A trainer may only touch their own batches; an admin may touch any
    (or scope to the impersonated trainer)."""
    if user.role == UserRole.ADMIN.value:
        email = _effective_email(user, impersonate)
        if not email:
            return
        if batch.trainer_email and batch.trainer_email.lower() == email:
            return
        raise ForbiddenError("This batch is not assigned to the impersonated trainer")
    if not batch.trainer_email or batch.trainer_email.lower() != user.email.lower():
        raise ForbiddenError("This batch is not assigned to you")


@router.get("/me/batches", response_model=List[TrainerBatchSummary])
async def my_batches(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
    x_impersonate_email: Optional[str] = Header(None),
) -> List[TrainerBatchSummary]:
    """Batches assigned to the signed-in trainer (or impersonated trainer for admins)."""
    email = _effective_email(current_user, x_impersonate_email)
    if email:
        batches = await training_batch_crud.get_by_trainer_email(db, email)
    else:
        batches = await training_batch_crud.get_multi(db, limit=200)

    out: List[TrainerBatchSummary] = []
    for batch in batches:
        programs_out = []
        module_count = 0
        if batch.programs:
            for p in batch.programs:
                programs_out.append(BatchProgramSummary(id=p.id, title=p.title))
                module_count += len(await training_module_crud.list_for_program(db, p.id))
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
                programs=programs_out,
                module_count=module_count,
            )
        )
    return out


@router.get("/me/sessions/today", response_model=List[TrainingSessionResponse])
async def my_sessions_today(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
    x_impersonate_email: Optional[str] = Header(None),
) -> List[TrainingSessionResponse]:
    """Today's sessions, plus anything already live."""
    email = _effective_email(current_user, x_impersonate_email) or None
    sessions = await training_session_crud.get_today_for_trainer(db, email)
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

    programs_out = []
    module_count = 0
    total_asset_count = 0
    if batch.programs:
        for p in batch.programs:
            program_full = await training_program_crud.get_with_modules_and_assets(db, p.id)
            if program_full:
                prog_mod_count = len(program_full.modules)
                prog_asset_count = sum(len(m.asset_links) for m in program_full.modules)
                programs_out.append(BatchProgramSummary(
                    id=p.id, 
                    title=p.title,
                    summary=p.summary,
                    level=p.level,
                    module_count=prog_mod_count,
                    asset_count=prog_asset_count
                ))
                module_count += prog_mod_count
                total_asset_count += prog_asset_count
            else:
                programs_out.append(BatchProgramSummary(id=p.id, title=p.title))

    sessions = await training_session_crud.list_for_batch(db, batch_id)
    completed_modules = len(set(s.module_id for s in sessions if s.status == "ended" and s.module_id is not None))

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
        programs=programs_out,
        module_count=module_count,
        asset_count=total_asset_count,
        completed_module_count=completed_modules,
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


@router.get("/batches/{batch_id}/modules", response_model=List[TrainingModuleDetail])
async def get_my_batch_modules(
    batch_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> List[TrainingModuleDetail]:
    """The modules available to present for this batch, via its linked programme."""
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")
    await _assert_owns_batch(db, current_user, batch)

    if not batch.programs:
        return []

    modules: List[TrainingModule] = []
    from sqlalchemy.orm import selectinload
    from sqlalchemy import select
    from app.models.training import TrainingModule, TrainingModuleAsset

    for p in batch.programs:
        result = await db.execute(
            select(TrainingModule)
            .where(TrainingModule.program_id == p.id)
            .options(
                selectinload(TrainingModule.asset_links).selectinload(TrainingModuleAsset.asset)
            )
            .order_by(TrainingModule.display_order, TrainingModule.id)
        )
        modules.extend(result.scalars().all())

    from app.crud.training import asset_to_response

    response_modules = []
    for m in modules:
        assets = []
        for link in sorted(m.asset_links, key=lambda l: l.display_order):
            asset_resp = await asset_to_response(db, link.asset, audience="trainer")
            assets.append(
                ModuleAssetLink(
                    id=link.id,
                    asset_id=link.asset_id,
                    display_order=link.display_order,
                    is_required=link.is_required,
                    notes=link.notes,
                    asset=asset_resp,
                )
            )
        
        response_modules.append(
            TrainingModuleDetail(
                id=m.id,
                program_id=m.program_id,
                title=m.title,
                slug=m.slug,
                description=m.description,
                display_order=m.display_order,
                estimated_minutes=m.estimated_minutes,
                status=m.status,
                asset_count=len(m.asset_links),
                created_at=m.created_at,
                updated_at=m.updated_at,
                assets=assets,
            )
        )
    return response_modules


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
        allowed_program_ids = {p.id for b in batches for p in b.programs}
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
        if batch.programs and module.program_id not in [p.id for p in batch.programs]:
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
    """Begin presenting: flip to live, mint the join code students will use, and mint
    the live-media stream path the trainer's browser will publish audio/video to."""
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
    if session.batch.programs and module.program_id not in [p.id for p in session.batch.programs]:
        raise ValidationError("That module belongs to a different training programme")

    if session.status != SessionStatus.LIVE.value:
        conflicting = await training_session_crud.get_other_live_session(
            db, session.batch_id, exclude_session_id=session.id
        )
        if conflicting:
            raise ValidationError(
                "Another session for this batch is already live — end it before starting a new one"
            )

    # Restarting a live session must not invalidate the code students already typed in,
    # nor the stream path a browser may already be mid-WHIP-handshake against.
    if session.status != SessionStatus.LIVE.value:
        session.join_code = await training_session_crud.generate_join_code(db)
        session.started_at = datetime.now(timezone.utc)
        session.status = SessionStatus.LIVE.value
        session.media_broadcasting = False
        session.media_mic_muted = False
        session.media_camera_off = False
        session.media_screen_sharing = False

    await training_session_crud.mint_live_media(db, session)

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
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    """Finish presenting and release the join code and live-media stream path back to
    the pool. If the session had live media, kicks off a recording/VOD row and the
    external transcode trigger for absent students to replay later."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    stream_path = session.live_stream_path  # captured before release clears it below

    session.status = SessionStatus.ENDED.value
    session.ended_at = datetime.now(timezone.utc)
    session.join_code = None
    db.add(session)
    await db.flush()
    await training_session_crud.release_live_media(db, session)

    if stream_path:
        if session.keep_recording:
            await session_recording_crud.create(
                db,
                obj_in={
                    "session_id": session_id,
                    "status": RecordingStatus.PROCESSING.value,
                    "recording_path": stream_path,
                    "watch_url": media.watch_url(stream_path),
                },
            )
            background_tasks.add_task(media.trigger_transcode, stream_path)
        else:
            from app.services.storage_service import storage_service
            # Delete the recording in the background since we don't want it
            background_tasks.add_task(storage_service.delete_recording, stream_path)

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


@router.post("/sessions/{session_id}/media/state", response_model=TrainingSessionResponse)
async def update_media_state(
    session_id: int,
    payload: MediaStateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    """Mute/camera/screen-share toggles. Only meaningful while presenting — a session
    that isn't live has no students listening for the broadcast this triggers."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    if session.status != SessionStatus.LIVE.value:
        raise ValidationError("Session must be live to change media state")

    updates = payload.model_dump(exclude_unset=True)
    if "broadcasting" in updates:
        session.media_broadcasting = updates["broadcasting"]
        # Stale mute/camera/share flags from a previous broadcast would otherwise leak
        # into the next one — the trainer's browser tears the whole capture down and
        # starts fresh, so the persisted state has to match that.
        if not session.media_broadcasting:
            session.media_mic_muted = False
            session.media_camera_off = False
            session.media_screen_sharing = False
    if "mic_muted" in updates:
        session.media_mic_muted = updates["mic_muted"]
    if "camera_off" in updates:
        session.media_camera_off = updates["camera_off"]
    if "screen_sharing" in updates:
        session.media_screen_sharing = updates["screen_sharing"]
    db.add(session)
    await db.flush()

    await bus.publish(
        db,
        session_id,
        "media_state_changed",
        {
            "broadcasting": session.media_broadcasting,
            "mic_muted": session.media_mic_muted,
            "camera_off": session.media_camera_off,
            "screen_sharing": session.media_screen_sharing,
        },
    )

    session = await training_session_crud.get_with_relations(db, session_id)
    return _session_out(session)


@router.patch("/sessions/{session_id}/recording", response_model=TrainingSessionResponse)
async def toggle_recording(
    session_id: int,
    payload: ToggleRecordingRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    """Toggle whether this session's background recording will be kept or deleted at the end."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    session.keep_recording = payload.keep_recording
    db.add(session)
    await db.flush()

    # We do NOT broadcast this state to students because they do not care if it's recorded
    return _session_out(session)


@router.get("/sessions/{session_id}/recording", response_model=RecordingView)
async def get_recording(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> RecordingView:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    recording = await session_recording_crud.get_by_session(db, session_id)
    if not recording:
        raise NotFoundError("Recording")
    return RecordingView.model_validate(recording)


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

    # audience="student" even though this endpoint is trainer-authenticated: the payload
    # is broadcast to every connected student, so it's the *audience of the broadcast*
    # that decides redaction, not the caller's role. Without this, putting a quiz slide
    # on screen ships its answer key to the whole class over the WebSocket.
    asset_payload = await asset_to_response(db, asset, audience="student")
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
    from app.schemas.classroom import DoubtRequestView
    from app.crud.classroom import doubt_request_crud
    from app.services.classroom.media import whep_url as build_whep_url

    doubts = await doubt_request_crud.list_by_session(db, session_id, statuses=["pending", "approved"])
    doubt_views = [
        DoubtRequestView(
            id=d.id,
            participant_id=d.participant_id,
            display_name=d.participant.display_name,
            status=d.status,
            requested_at=d.created_at,
            whep_url=build_whep_url(f"doubt-{d.id}") if d.status == "approved" else None
        )
        for d in doubts
    ]

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
        doubt_requests=[
            {
                "id": d.id,
                "participant_id": d.participant_id,
                "display_name": d.participant.display_name,
                "status": d.status,
                "requested_at": d.created_at,
                "whep_url": build_whep_url(f"class-{session_id}-doubt-{d.participant_id}") if d.status == "approved" else None
            }
            for d in doubts
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


@router.get("/sessions/{session_id}/questions", response_model=list[TrainingSessionQuestionResponse])
async def trainer_list_questions(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> list[TrainingSessionQuestionResponse]:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    questions = await question_crud.get_by_session(db, session_id=session_id)
    return [TrainingSessionQuestionResponse.model_validate(q) for q in questions]


@router.post("/sessions/{session_id}/questions/{question_id}/answer", response_model=TrainingSessionQuestionResponse)
async def trainer_answer_question(
    session_id: int,
    question_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionQuestionResponse:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    q = await question_crud.get(db, id=question_id)
    if not q or q.session_id != session_id:
        raise NotFoundError("Question")

    updated_question = await question_crud.mark_answered(db, db_obj=q)

    await bus.publish(
        db,
        session_id,
        "question_answered",
        {"question_id": updated_question.id}
    )
    
    response_obj = TrainingSessionQuestionResponse.model_validate(updated_question)
    return response_obj


@router.patch("/sessions/{session_id}/settings", response_model=TrainingSessionResponse)
async def update_session_settings(
    session_id: int,
    payload: ToggleQuestionsPublicRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionResponse:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    session.questions_are_public = payload.questions_are_public
    db.add(session)
    await db.flush()

    await bus.publish(
        db,
        session_id,
        "questions_visibility_changed",
        {"questions_are_public": session.questions_are_public}
    )
    
    return _session_out(session)


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


@router.get("/sessions/{session_id}/questions", response_model=list[TrainingSessionQuestionResponse])
async def trainer_list_questions(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> list[TrainingSessionQuestionResponse]:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    questions = await question_crud.get_by_session(db, session_id=session_id)
    return [TrainingSessionQuestionResponse.model_validate(q) for q in questions]


@router.post("/sessions/{session_id}/questions/{question_id}/answer", response_model=TrainingSessionQuestionResponse)
async def trainer_answer_question(
    session_id: int,
    question_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> TrainingSessionQuestionResponse:
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    q = await question_crud.get(db, id=question_id)
    if not q or q.session_id != session_id:
        raise NotFoundError("Question")

    updated_question = await question_crud.mark_answered(db, db_obj=q)

    await bus.publish(
        db,
        session_id,
        "question_answered",
        {"question_id": updated_question.id}
    )
    
    response_obj = TrainingSessionQuestionResponse.model_validate(updated_question)
    return response_obj


    await db.flush()

    await bus.publish(
        db,
        session_id,
        "questions_visibility_changed",
        {"questions_are_public": session.questions_are_public}
    )
    
    return _session_out(session)

@router.post("/sessions/{session_id}/doubts/{doubt_id}/approve", response_model=MessageResponse)
async def approve_doubt(
    session_id: int,
    doubt_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> MessageResponse:
    from app.crud.classroom import doubt_request_crud
    from app.services.classroom.media import whip_url as build_whip_url, whep_url as build_whep_url
    from app.models.classroom import DOUBT_APPROVED
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)
    
    req = await doubt_request_crud.update_status(db, doubt_id, "approved")
    if not req:
        raise NotFoundError("DoubtRequest")
    
    whip_path = f"class-{session_id}-doubt-{req.participant_id}"
    full_whip_url = build_whip_url(whip_path)
    full_whep_url = build_whep_url(whip_path)
    
    await bus.publish(db, session_id, DOUBT_APPROVED, {
        "participant_id": req.participant_id, 
        "doubt_id": doubt_id,
        "whip_url": full_whip_url,
        "whep_url": full_whep_url
    })
    return MessageResponse(message="Doubt approved")

@router.post("/sessions/{session_id}/doubts/{doubt_id}/complete", response_model=MessageResponse)
async def complete_doubt(
    session_id: int,
    doubt_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> MessageResponse:
    from app.crud.classroom import doubt_request_crud
    from app.models.classroom import DOUBT_COMPLETED
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)
    
    req = await doubt_request_crud.update_status(db, doubt_id, "completed")
    if not req:
        raise NotFoundError("DoubtRequest")
    
    await bus.publish(db, session_id, DOUBT_COMPLETED, {
        "participant_id": req.participant_id, 
        "doubt_id": doubt_id
    })
    return MessageResponse(message="Doubt audio stopped")
