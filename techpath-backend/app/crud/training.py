"""CRUD for training content."""
import csv
import io
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any, List, Literal, Optional, Sequence

import httpx
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.constants import AssetStorageKind, AssetType, asset_rule
from app.crud.base import CRUDBase
from app.crud.media import media_file_crud
from app.models.training import (
    LectureAsset,
    TrainingModule,
    TrainingModuleAsset,
    TrainingProgram,
)
from app.schemas.training import (
    CsvPreview,
    LectureAssetResponse,
    TrainingModuleCreate,
    TrainingModuleUpdate,
    TrainingProgramCreate,
    TrainingProgramUpdate,
)
from app.services.storage_service import storage_service

logger = logging.getLogger(__name__)

CSV_PREVIEW_ROW_LIMIT = 200
CSV_PREVIEW_BYTE_LIMIT = 262_144  # 256 KiB — comfortably covers 200 rows of normal width
CSV_PREVIEW_CACHE_TTL_SECONDS = 300

# Keyed by the media file's stable stored_path (NOT the signed file_url — that carries a
# fresh SAS signature/expiry on every call, so caching by full URL would never hit, see
# asset_to_response). Left unbounded: this is one training platform's worth of CSV
# lecture assets, not a public multi-tenant service, so a plain dict that never evicts by
# size is a reasonable simplification here rather than an oversight.
_csv_preview_cache: dict[str, tuple[float, Optional[CsvPreview]]] = {}


def _dump_tags(tags: Optional[Sequence[str]]) -> Optional[str]:
    return json.dumps(list(tags)) if tags else None


def load_tags(raw: Optional[str]) -> List[str]:
    """Tolerate hand-edited or legacy rows rather than 500ing a list page."""
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except (ValueError, TypeError):
        return []
    return [str(t) for t in parsed] if isinstance(parsed, list) else []


def load_config(raw: Optional[str]) -> Optional[dict]:
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except (ValueError, TypeError):
        return None
    return parsed if isinstance(parsed, dict) else None


async def _fetch_csv_preview(cache_key: str, url: str) -> Optional[CsvPreview]:
    """Best-effort, bounded fetch — never lets a slow or broken file break the asset
    response. A Range request caps how much of a multi-MB dataset we ever pull down
    just to show a couple hundred rows.

    Deliberately server-side: object storage providers generally grant no CORS to
    arbitrary origins by default (Azure Blob included), so a browser-side fetch() of
    the same URL is silently blocked before it reaches the network — this is not
    optional plumbing, it's the only way the preview can work at all.

    Cached in-process for CSV_PREVIEW_CACHE_TTL_SECONDS under ``cache_key`` (the stable
    storage path — see caller) so this same file isn't re-fetched from storage on every
    single read of the asset. A failed fetch/parse is cached as ``None`` too, so a
    broken file doesn't get hammered on every page load until the TTL expires.
    """
    cached = _csv_preview_cache.get(cache_key)
    if cached is not None and time.time() - cached[0] < CSV_PREVIEW_CACHE_TTL_SECONDS:
        return cached[1]

    def _store(preview: Optional[CsvPreview]) -> Optional[CsvPreview]:
        _csv_preview_cache[cache_key] = (time.time(), preview)
        return preview

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
            resp = await client.get(
                url, headers={"Range": f"bytes=0-{CSV_PREVIEW_BYTE_LIMIT - 1}"}
            )
        if resp.status_code not in (200, 206):
            return _store(None)
        raw = resp.content
    except Exception as exc:  # noqa: BLE001 — a broken preview must not break the asset
        logger.warning("CSV preview fetch failed: %s", exc)
        return _store(None)

    byte_truncated = resp.status_code == 206 or len(raw) >= CSV_PREVIEW_BYTE_LIMIT
    text = raw.decode("utf-8", errors="replace")
    if byte_truncated:
        # The byte cutoff can land mid-row; drop a possibly-partial trailing line
        # rather than show a corrupted last row.
        text = text.rsplit("\n", 1)[0]

    try:
        all_rows = list(csv.reader(io.StringIO(text)))
    except csv.Error as exc:
        logger.warning("CSV preview parse failed: %s", exc)
        return _store(None)
    if not all_rows:
        return _store(None)

    header, *body = all_rows
    return _store(
        CsvPreview(
            header=header,
            rows=body[:CSV_PREVIEW_ROW_LIMIT],
            total_rows=len(body),
            truncated=byte_truncated or len(body) > CSV_PREVIEW_ROW_LIMIT,
        )
    )


Audience = Literal["trainer", "student"]


def _redact_quiz_config_for_student(config: Optional[dict]) -> Optional[dict]:
    """Strip the answer key out of a quiz asset's config.

    Removes ``correct_index`` and ``explanation`` from every question — the keys are
    dropped entirely rather than nulled, so nothing about the right answer survives in
    the payload's shape either.

    Works on a copy. ``load_config`` parses fresh JSON per call today, but mutating a
    dict that reached us from anywhere else would silently poison the trainer's view of
    the same asset, and that failure would be near-impossible to trace back here.
    """
    if not config:
        return config
    questions = config.get("questions")
    if not isinstance(questions, list):
        return config

    redacted = dict(config)
    redacted["questions"] = [
        {k: v for k, v in question.items() if k not in ("correct_index", "explanation")}
        if isinstance(question, dict)
        else question
        for question in questions
    ]
    return redacted


async def asset_to_response(
    db: AsyncSession, asset: LectureAsset, *, audience: Audience = "trainer"
) -> LectureAssetResponse:
    """Shared by the admin module endpoint, the trainer's slide broadcast, and the
    student classroom state fetch — one place decides what an asset looks like off
    the wire so the three surfaces can't quietly drift apart.

    File-backed assets (pdf, ppt, video, ...) only ever had ``media_file_id`` reliably
    set — the admin upload form never wrote a usable path into ``config`` — so
    ``file_url`` is resolved here from the media file's actual storage location via
    ``storage_service``, not trusted from anything the client sent. This also means it
    correctly regenerates a fresh signed URL under Azure Blob storage, where a stored
    path alone isn't servable and a client-side guess would be flatly wrong.

    ``audience`` decides whether a quiz asset carries its answer key. It defaults to
    ``"trainer"`` because most callers here are the CMS and the presenter, which need
    it — but that means **any new student-facing caller must pass
    ``audience="student"`` explicitly**. Forgetting to is exactly how the answer key
    leaked to students before; ``tests/test_student_quiz_flow.py`` asserts on the
    student endpoints specifically to catch a regression.
    """
    file_url: Optional[str] = None
    stored_path: Optional[str] = None
    if asset.media_file_id:
        media_file = await media_file_crud.get(db, asset.media_file_id)
        if media_file:
            stored_path = media_file.stored_path
            file_url = await storage_service.get_file_url(media_file.stored_path)

    csv_preview: Optional[CsvPreview] = None
    if asset.asset_type == AssetType.CSV.value and file_url and stored_path:
        # stored_path is the stable cache key; file_url is a freshly-signed SAS link
        # that's only good for the actual fetch — see _fetch_csv_preview.
        csv_preview = await _fetch_csv_preview(stored_path, file_url)

    config = load_config(asset.config_json)
    if audience == "student" and asset.asset_type == AssetType.QUIZ.value:
        config = _redact_quiz_config_for_student(config)

    return LectureAssetResponse(
        id=asset.id,
        public_id=asset.public_id,
        title=asset.title,
        asset_type=asset.asset_type,
        description=asset.description,
        body=asset.body,
        media_file_id=asset.media_file_id,
        external_url=asset.external_url,
        config=config,
        tags=load_tags(asset.tags_json),
        status=asset.status,
        is_active=asset.is_active,
        storage_kind=asset_rule(asset.asset_type).kind.value,
        csv_preview=csv_preview,
        file_url=file_url,
        created_at=asset.created_at,
        updated_at=asset.updated_at,
    )


class CRUDTrainingProgram(CRUDBase[TrainingProgram, TrainingProgramCreate, TrainingProgramUpdate]):
    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[TrainingProgram]:
        result = await db.execute(select(TrainingProgram).where(TrainingProgram.slug == slug))
        return result.scalar_one_or_none()

    async def get_with_modules(self, db: AsyncSession, id: int) -> Optional[TrainingProgram]:
        result = await db.execute(
            select(TrainingProgram)
            .where(TrainingProgram.id == id)
            .options(selectinload(TrainingProgram.modules))
        )
        return result.scalar_one_or_none()

    async def get_with_modules_and_assets(
        self, db: AsyncSession, id: int
    ) -> Optional[TrainingProgram]:
        """Deep load: programme -> modules -> asset_links -> asset."""
        result = await db.execute(
            select(TrainingProgram)
            .where(TrainingProgram.id == id)
            .options(
                selectinload(TrainingProgram.modules).selectinload(
                    TrainingModule.asset_links
                ).selectinload(TrainingModuleAsset.asset)
            )
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        course_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[List[TrainingProgram], int]:
        """List with the filters the admin UI actually offers.

        ``CRUDBase.get_multi`` only does equality, so anything with a LIKE lives here.
        """
        query = select(TrainingProgram)
        count_query = select(func.count(TrainingProgram.id))

        conditions = []
        if status:
            conditions.append(TrainingProgram.status == status)
        if course_id is not None:
            conditions.append(TrainingProgram.course_id == course_id)
        if search:
            term = f"%{search}%"
            conditions.append(
                or_(TrainingProgram.title.ilike(term), TrainingProgram.summary.ilike(term))
            )

        for cond in conditions:
            query = query.where(cond)
            count_query = count_query.where(cond)

        query = query.order_by(TrainingProgram.display_order, TrainingProgram.id.desc())
        query = query.offset(skip).limit(limit)

        rows = list((await db.execute(query)).scalars().all())
        total = (await db.execute(count_query)).scalar() or 0
        return rows, total

    async def create_from_schema(
        self, db: AsyncSession, *, obj_in: TrainingProgramCreate
    ) -> TrainingProgram:
        data = obj_in.model_dump(exclude_unset=True)
        tags = data.pop("tags", None)
        db_obj = TrainingProgram(**data, tags_json=_dump_tags(tags))
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update_from_schema(
        self, db: AsyncSession, *, db_obj: TrainingProgram, obj_in: TrainingProgramUpdate
    ) -> TrainingProgram:
        data = obj_in.model_dump(exclude_unset=True)
        if "tags" in data:
            db_obj.tags_json = _dump_tags(data.pop("tags"))
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def module_counts(self, db: AsyncSession, program_ids: Sequence[int]) -> dict[int, int]:
        if not program_ids:
            return {}
        result = await db.execute(
            select(TrainingModule.program_id, func.count(TrainingModule.id))
            .where(TrainingModule.program_id.in_(program_ids))
            .group_by(TrainingModule.program_id)
        )
        return {pid: count for pid, count in result.all()}


class CRUDTrainingModule(CRUDBase[TrainingModule, TrainingModuleCreate, TrainingModuleUpdate]):
    async def list_for_program(self, db: AsyncSession, program_id: int) -> List[TrainingModule]:
        result = await db.execute(
            select(TrainingModule)
            .where(TrainingModule.program_id == program_id)
            .order_by(TrainingModule.display_order, TrainingModule.id)
        )
        return list(result.scalars().all())

    async def get_with_assets(self, db: AsyncSession, id: int) -> Optional[TrainingModule]:
        result = await db.execute(
            select(TrainingModule)
            .where(TrainingModule.id == id)
            .options(
                selectinload(TrainingModule.asset_links).selectinload(TrainingModuleAsset.asset)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_slug(
        self, db: AsyncSession, program_id: int, slug: str
    ) -> Optional[TrainingModule]:
        result = await db.execute(
            select(TrainingModule).where(
                TrainingModule.program_id == program_id, TrainingModule.slug == slug
            )
        )
        return result.scalar_one_or_none()

    async def next_order(self, db: AsyncSession, program_id: int) -> int:
        result = await db.execute(
            select(func.max(TrainingModule.display_order)).where(
                TrainingModule.program_id == program_id
            )
        )
        return (result.scalar() or 0) + 1

    async def asset_counts(self, db: AsyncSession, module_ids: Sequence[int]) -> dict[int, int]:
        if not module_ids:
            return {}
        result = await db.execute(
            select(TrainingModuleAsset.module_id, func.count(TrainingModuleAsset.id))
            .where(TrainingModuleAsset.module_id.in_(module_ids))
            .group_by(TrainingModuleAsset.module_id)
        )
        return {mid: count for mid, count in result.all()}

    async def reorder(self, db: AsyncSession, program_id: int, items: list) -> None:
        """Apply a whole ordering in one transaction, ignoring ids from other programmes."""
        by_id = {i.id: i.display_order for i in items}
        rows = await db.execute(
            select(TrainingModule).where(
                TrainingModule.program_id == program_id, TrainingModule.id.in_(by_id)
            )
        )
        for module in rows.scalars().all():
            module.display_order = by_id[module.id]
            db.add(module)
        await db.flush()


class CRUDLectureAsset(CRUDBase[LectureAsset, Any, Any]):
    async def get_by_public_id(self, db: AsyncSession, public_id: str) -> Optional[LectureAsset]:
        result = await db.execute(select(LectureAsset).where(LectureAsset.public_id == public_id))
        return result.scalar_one_or_none()

    async def search(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        asset_type: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> tuple[List[LectureAsset], int]:
        query = select(LectureAsset)
        count_query = select(func.count(LectureAsset.id))

        conditions = []
        if asset_type:
            conditions.append(LectureAsset.asset_type == asset_type)
        if status:
            conditions.append(LectureAsset.status == status)
        if is_active is not None:
            conditions.append(LectureAsset.is_active.is_(is_active))
        if search:
            term = f"%{search}%"
            conditions.append(
                or_(LectureAsset.title.ilike(term), LectureAsset.description.ilike(term))
            )

        for cond in conditions:
            query = query.where(cond)
            count_query = count_query.where(cond)

        query = query.order_by(LectureAsset.id.desc()).offset(skip).limit(limit)
        rows = list((await db.execute(query)).scalars().all())
        total = (await db.execute(count_query)).scalar() or 0
        return rows, total

    async def create_from_union(
        self, db: AsyncSession, *, obj_in, created_by_id: Optional[int] = None
    ) -> LectureAsset:
        """Persist a validated asset, routing its payload to the column its type uses."""
        data = obj_in.model_dump(exclude_unset=True, mode="json")
        asset_type = AssetType(data.pop("asset_type"))
        kind = asset_rule(asset_type).kind

        common = {
            "public_id": str(uuid.uuid4()),
            "title": data.pop("title"),
            "asset_type": asset_type.value,
            "description": data.pop("description", None),
            "status": data.pop("status", "draft"),
            "tags_json": _dump_tags(data.pop("tags", None)),
            "created_by_id": created_by_id,
        }

        if kind is AssetStorageKind.INLINE_TEXT:
            common["body"] = data.pop("body")
            language = data.pop("language", None)
            if language:
                common["config_json"] = json.dumps({"language": language})
        elif kind is AssetStorageKind.FILE:
            common["media_file_id"] = data.pop("media_file_id")
        elif kind is AssetStorageKind.LINK:
            common["external_url"] = str(data.pop("external_url"))
        elif kind is AssetStorageKind.STRUCTURED:
            # Whatever remains after the common fields IS the structured payload.
            common["config_json"] = json.dumps(data)

        db_obj = LectureAsset(**common)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update_from_schema(self, db: AsyncSession, *, db_obj: LectureAsset, obj_in):
        data = obj_in.model_dump(exclude_unset=True)
        if "tags" in data:
            db_obj.tags_json = _dump_tags(data.pop("tags"))
        if "config" in data:
            config = data.pop("config")
            db_obj.config_json = json.dumps(config) if config is not None else None
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def usages(self, db: AsyncSession, asset_id: int) -> List[dict]:
        """Every module this asset is placed in, with its programme, for the UI."""
        result = await db.execute(
            select(
                TrainingModuleAsset.module_id,
                TrainingModule.title,
                TrainingProgram.id,
                TrainingProgram.title,
            )
            .join(TrainingModule, TrainingModuleAsset.module_id == TrainingModule.id)
            .join(TrainingProgram, TrainingModule.program_id == TrainingProgram.id)
            .where(TrainingModuleAsset.asset_id == asset_id)
            .order_by(TrainingProgram.title, TrainingModule.display_order)
        )
        return [
            {
                "module_id": module_id,
                "module_title": module_title,
                "program_id": program_id,
                "program_title": program_title,
            }
            for module_id, module_title, program_id, program_title in result.all()
        ]

    async def usage_count(self, db: AsyncSession, asset_id: int) -> int:
        result = await db.execute(
            select(func.count(TrainingModuleAsset.id)).where(
                TrainingModuleAsset.asset_id == asset_id
            )
        )
        return result.scalar() or 0


class CRUDModuleAsset(CRUDBase[TrainingModuleAsset, Any, Any]):
    async def get_link(
        self, db: AsyncSession, module_id: int, asset_id: int
    ) -> Optional[TrainingModuleAsset]:
        result = await db.execute(
            select(TrainingModuleAsset).where(
                TrainingModuleAsset.module_id == module_id,
                TrainingModuleAsset.asset_id == asset_id,
            )
        )
        return result.scalar_one_or_none()

    async def next_order(self, db: AsyncSession, module_id: int) -> int:
        result = await db.execute(
            select(func.max(TrainingModuleAsset.display_order)).where(
                TrainingModuleAsset.module_id == module_id
            )
        )
        return (result.scalar() or 0) + 1

    async def attach(
        self,
        db: AsyncSession,
        *,
        module_id: int,
        asset_id: int,
        display_order: Optional[int] = None,
        is_required: bool = True,
        notes: Optional[str] = None,
    ) -> TrainingModuleAsset:
        link = TrainingModuleAsset(
            module_id=module_id,
            asset_id=asset_id,
            display_order=(
                display_order
                if display_order is not None
                else await self.next_order(db, module_id)
            ),
            is_required=is_required,
            notes=notes,
            created_at=datetime.now(timezone.utc),
        )
        db.add(link)
        await db.flush()
        await db.refresh(link)
        return link

    async def reorder(self, db: AsyncSession, module_id: int, items: list) -> None:
        by_id = {i.id: i.display_order for i in items}
        rows = await db.execute(
            select(TrainingModuleAsset).where(
                TrainingModuleAsset.module_id == module_id, TrainingModuleAsset.id.in_(by_id)
            )
        )
        for link in rows.scalars().all():
            link.display_order = by_id[link.id]
            db.add(link)
        await db.flush()


training_program_crud = CRUDTrainingProgram(TrainingProgram)
training_module_crud = CRUDTrainingModule(TrainingModule)
lecture_asset_crud = CRUDLectureAsset(LectureAsset)
module_asset_crud = CRUDModuleAsset(TrainingModuleAsset)
