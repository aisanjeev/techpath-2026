"""Schemas for the live classroom: student join/identify, realtime state, polls."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.training import LectureAssetResponse


# ---------- student join / identify ----------


class JoinRequest(BaseModel):
    join_code: str = Field(..., min_length=6, max_length=6)


class JoinResponse(BaseModel):
    session_id: int
    batch_name: str
    session_title: Optional[str] = None
    module_title: Optional[str] = None
    status: str


class IdentifyRequest(BaseModel):
    session_id: int
    email: Optional[str] = Field(None, max_length=255)
    guest_name: Optional[str] = Field(None, max_length=200)


class IdentifyResponse(BaseModel):
    matched: bool
    token: Optional[str] = None
    display_name: Optional[str] = None


# ---------- realtime state (bootstrap on connect/reconnect) ----------


class PollStateView(BaseModel):
    """A participant's view of the current poll — results are withheld until they vote,
    so an early tally can't bias the room before everyone has had a chance to answer."""

    id: int
    question: str
    options: List[str]
    status: str
    my_vote: Optional[int] = None
    results: Optional[dict[int, int]] = None


class CodeStateView(BaseModel):
    language: str
    content: str


class PresenceView(BaseModel):
    online: int


class TimerView(BaseModel):
    """A trainer-started countdown, as seen by a client bootstrapping mid-session. Only
    ever present while a timer is running (see ``TrainingSession.timer_started_at``) —
    remaining time is computed client-side from ``started_at`` + ``duration_seconds``,
    never here, since "has it already expired" depends on the reader's clock, not the
    server's."""

    duration_seconds: int
    started_at: datetime


class MediaView(BaseModel):
    """Live audio/video URLs and state for one session.

    ``whip_url`` (publish) is only ever populated on a trainer-facing response;
    ``whep_url``/``hls_url`` (playback) only on a participant-facing one — see
    ``contracts/live-media-api.md``. All three are ``None`` whenever the session has no
    ``live_stream_path`` yet (media hasn't started, or this is a chat/poll-only class).
    """

    whip_url: Optional[str] = None
    whep_url: Optional[str] = None
    hls_url: Optional[str] = None
    mic_muted: bool = False
    camera_off: bool = False
    screen_sharing: bool = False


class SessionStateResponse(BaseModel):
    session_id: int
    title: Optional[str] = None
    status: str
    batch_name: str
    module_title: Optional[str] = None
    current_asset: Optional[LectureAssetResponse] = None
    open_poll: Optional[PollStateView] = None
    code: Optional[CodeStateView] = None
    my_confusion: bool = False
    presence: PresenceView
    timer: Optional[TimerView] = None
    # Participant-facing view: whep_url/hls_url only, never whip_url (see MediaView).
    # Null whenever the trainer hasn't started publishing media for this session.
    media: Optional[MediaView] = None


class ConfusionRequest(BaseModel):
    confused: bool


class HandRaiseRequest(BaseModel):
    raised: bool


class ReactionRequest(BaseModel):
    emoji: str = Field(..., min_length=1, max_length=8)


class VoteRequest(BaseModel):
    option_index: int = Field(..., ge=0)


# ---------- trainer controls ----------


class SetSlideRequest(BaseModel):
    asset_id: int


class MediaStateRequest(BaseModel):
    """Partial update — a trainer toggling just the mic must not also imply anything
    about camera/screen-share state, so every field is optional and unset fields are
    left untouched (see the endpoint's ``exclude_unset`` usage)."""

    mic_muted: Optional[bool] = None
    camera_off: Optional[bool] = None
    screen_sharing: Optional[bool] = None


class StartTimerRequest(BaseModel):
    duration_seconds: int = Field(..., gt=0, le=14400)


class CreatePollRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    options: List[str] = Field(..., min_length=2, max_length=6)


class PollFromQuizRequest(BaseModel):
    """Launches a poll pre-seeded from one question of a quiz lecture asset, so the
    trainer doesn't have to retype it — see ``QuizQuestion`` in ``app/schemas/training.py``
    for the shape of the question this indexes into."""

    asset_id: int = Field(..., gt=0)
    question_index: int = Field(..., ge=0)


class PollResultsResponse(BaseModel):
    id: int
    question: str
    options: List[str]
    status: str
    results: dict[int, int]
    total_votes: int
    # Set only when this poll was launched from a quiz question (see
    # ``PollFromQuizRequest``); null for an ordinary trainer poll, which has no
    # "correct" answer. Never present on the broadcast a still-voting student receives —
    # only in a trainer-facing response.
    correct_option_index: Optional[int] = None
    created_at: datetime
    closed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=False)


class UpdateCodeRequest(BaseModel):
    language: str = Field(default="python", max_length=50)
    content: str = Field(default="", max_length=200_000)


class RosterParticipant(BaseModel):
    id: int
    display_name: str
    is_guest: bool
    is_online: bool
    is_confused: bool
    hand_raised: bool
    hand_raised_at: Optional[datetime] = None
    first_joined_at: datetime
    last_seen_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConfusionSummary(BaseModel):
    online: int
    confused: int
    ratio: float


class HandRaisedEntry(BaseModel):
    """One entry in the trainer's call-on-me queue, first raised first."""

    participant_id: int
    display_name: str
    hand_raised_at: Optional[datetime] = None


class RosterResponse(BaseModel):
    participants: List[RosterParticipant]
    confusion: ConfusionSummary
    hands_raised: List[HandRaisedEntry] = []
    timer: Optional[TimerView] = None


class RecordingView(BaseModel):
    """A session's VOD/replay status. ``watch_url`` is deterministic from the stream
    path (see media.watch_url) and is always present once a recording row exists — the
    frontend still gates actually linking/playing it on ``status == 'ready'``, per
    spec.md's edge case for a still-processing replay."""

    status: str
    watch_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class WsTokenResponse(BaseModel):
    """Short-lived, session-scoped — see identity.mint_trainer_ws_token for why this
    exists instead of putting the trainer's real auth token in a URL."""

    token: str
    expires_in_minutes: int
