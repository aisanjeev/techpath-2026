"""Pydantic schemas for training content.

The interesting part is ``LectureAssetCreate``. ``lecture_assets`` is one wide table with
an ``asset_type`` discriminator, which keeps the storage simple but would leave the
payload unvalidated if we stopped there. So the shape of each type is pinned here
instead: a discriminated union means a quiz must carry questions, a YouTube asset must
carry a URL, and a markdown asset must carry a body — enforced on write, at the edge.
"""
from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from app.core.constants import AssetStatus, AssetType, TrainingDeliveryMode


# ============================================
# Lecture assets — per-type payloads
# ============================================


class _AssetCommon(BaseModel):
    """Fields every asset carries regardless of type."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    status: AssetStatus = AssetStatus.DRAFT


class InlineTextAssetIn(_AssetCommon):
    asset_type: Literal[
        AssetType.NOTES, AssetType.CHEAT_SHEET, AssetType.CODE_SNIPPET
    ]
    body: str = Field(..., min_length=1)
    # Only meaningful for code_snippet; harmless elsewhere.
    language: Optional[str] = Field(None, max_length=40)


class FileAssetIn(_AssetCommon):
    asset_type: Literal[
        AssetType.MARKDOWN,
        AssetType.PDF,
        AssetType.PPT,
        AssetType.VIDEO,
        AssetType.NOTEBOOK,
        AssetType.ZIP,
        AssetType.EXCEL,
        AssetType.CSV,
        AssetType.TERMINAL_RECORDING,
        AssetType.HTML_BUNDLE,
    ]
    media_file_id: int = Field(..., gt=0)


class LinkAssetIn(_AssetCommon):
    asset_type: Literal[AssetType.EXTERNAL_URL, AssetType.GITHUB_REPO, AssetType.YOUTUBE]
    external_url: HttpUrl


class QuizQuestion(BaseModel):
    question: str = Field(..., min_length=1)
    options: List[str] = Field(..., min_length=2)
    correct_index: int = Field(..., ge=0)
    explanation: Optional[str] = None

    @field_validator("correct_index")
    @classmethod
    def _index_in_range(cls, v: int, info) -> int:
        options = info.data.get("options")
        if options is not None and v >= len(options):
            raise ValueError(f"correct_index {v} is out of range for {len(options)} options")
        return v


class QuizAssetIn(_AssetCommon):
    asset_type: Literal[AssetType.QUIZ]
    questions: List[QuizQuestion] = Field(..., min_length=1)
    pass_mark_percent: int = Field(default=60, ge=0, le=100)


class AssignmentAssetIn(_AssetCommon):
    asset_type: Literal[AssetType.ASSIGNMENT]
    instructions: str = Field(..., min_length=1)
    due_in_days: Optional[int] = Field(None, ge=0)
    rubric: Optional[List[str]] = None


class LabStep(BaseModel):
    title: str = Field(..., min_length=1)
    instructions: str = ""


class LabAssetIn(_AssetCommon):
    asset_type: Literal[AssetType.LAB]
    objective: str = Field(..., min_length=1)
    steps: List[Union[LabStep, str]] = Field(..., min_length=1)
    starter_code: Optional[str] = None
    expected_output: Optional[str] = None


LectureAssetCreate = Annotated[
    Union[
        InlineTextAssetIn,
        FileAssetIn,
        LinkAssetIn,
        QuizAssetIn,
        AssignmentAssetIn,
        LabAssetIn,
    ],
    Field(discriminator="asset_type"),
]


class LectureAssetUpdate(BaseModel):
    """Partial update. The asset type is immutable — its payload column depends on it,
    so changing it would orphan the existing payload. Delete and recreate instead."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    status: Optional[AssetStatus] = None
    is_active: Optional[bool] = None
    body: Optional[str] = None
    media_file_id: Optional[int] = None
    external_url: Optional[str] = None
    config: Optional[dict] = None


class CsvPreview(BaseModel):
    header: List[str] = []
    rows: List[List[str]] = []
    total_rows: int
    truncated: bool


class LectureAssetResponse(BaseModel):
    id: int
    public_id: str
    title: str
    asset_type: str
    description: Optional[str] = None
    body: Optional[str] = None
    media_file_id: Optional[int] = None
    external_url: Optional[str] = None
    config: Optional[dict] = None
    tags: List[str] = []
    status: str
    is_active: bool
    storage_kind: str
    # Resolved server-side from media_file_id via storage_service — local storage and
    # Azure Blob need different URL shapes (Azure's is a signed, expiring SAS URL), so
    # no client should ever construct this from a raw path itself.
    file_url: Optional[str] = None
    # Also resolved server-side, for the same reason file_url is: object storage
    # providers generally don't grant CORS to arbitrary origins by default, so a
    # browser-side fetch() of file_url would be silently blocked before it ever reaches
    # the network. A server-to-server fetch has no such restriction.
    csv_preview: Optional[CsvPreview] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetUsage(BaseModel):
    """Where an asset is currently placed. Shown before edit or delete so nobody
    changes shared content without seeing the blast radius."""

    module_id: int
    module_title: str
    program_id: int
    program_title: str

    model_config = ConfigDict(from_attributes=True)


# ============================================
# Modules
# ============================================


class TrainingModuleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: Optional[str] = None
    display_order: int = 0
    estimated_minutes: Optional[int] = Field(None, ge=0)
    status: AssetStatus = AssetStatus.DRAFT


class TrainingModuleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: Optional[str] = None
    display_order: Optional[int] = None
    estimated_minutes: Optional[int] = Field(None, ge=0)
    status: Optional[AssetStatus] = None


class ModuleAssetLink(BaseModel):
    """An asset as placed in a module."""

    id: int
    asset_id: int
    display_order: int
    is_required: bool
    notes: Optional[str] = None
    asset: LectureAssetResponse

    model_config = ConfigDict(from_attributes=True)


class TrainingModuleResponse(BaseModel):
    id: int
    program_id: int
    title: str
    slug: str
    description: Optional[str] = None
    display_order: int
    estimated_minutes: Optional[int] = None
    status: str
    asset_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TrainingModuleDetail(TrainingModuleResponse):
    assets: List[ModuleAssetLink] = []


class AttachAssetRequest(BaseModel):
    asset_id: int = Field(..., gt=0)
    display_order: Optional[int] = None
    is_required: bool = True
    notes: Optional[str] = None


class ReorderItem(BaseModel):
    id: int = Field(..., gt=0)
    display_order: int = Field(..., ge=0)


class ReorderRequest(BaseModel):
    items: List[ReorderItem] = Field(..., min_length=1)


# ============================================
# Programmes
# ============================================


class TrainingProgramCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    summary: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    # Optional by design: offline-only training has no public course.
    course_id: Optional[int] = None
    delivery_mode: TrainingDeliveryMode = TrainingDeliveryMode.OFFLINE
    level: Optional[str] = Field(None, max_length=20)
    duration: Optional[str] = Field(None, max_length=100)
    cover_image: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    status: AssetStatus = AssetStatus.DRAFT
    display_order: int = 0


class TrainingProgramUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    summary: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    course_id: Optional[int] = None
    delivery_mode: Optional[TrainingDeliveryMode] = None
    level: Optional[str] = None
    duration: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[AssetStatus] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class TrainingProgramResponse(BaseModel):
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    description: Optional[str] = None
    course_id: Optional[int] = None
    delivery_mode: str
    level: Optional[str] = None
    duration: Optional[str] = None
    cover_image: Optional[str] = None
    tags: List[str] = []
    status: str
    display_order: int
    is_active: bool
    module_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TrainingProgramDetail(TrainingProgramResponse):
    modules: List[TrainingModuleResponse] = []


class AssetTypeInfo(BaseModel):
    """Registry entry, published so the admin UI builds its type picker from the same
    source of truth the backend validates against."""

    value: str
    label: str
    storage_kind: str
    max_size_mb: int
    allowed_content_types: List[str]
    allowed_extensions: List[str]
