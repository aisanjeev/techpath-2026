"""Admin endpoints for training content: programmes, modules and the asset library."""
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.v1.dependencies import get_current_admin_user
from app.core.constants import (
    ASSET_TYPE_RULES,
    ASSET_TYPES_ENABLED,
    AssetType,
)
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.crud.training import (
    asset_to_response,
    lecture_asset_crud,
    load_tags,
    module_asset_crud,
    training_module_crud,
    training_program_crud,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.training import (
    AssetTypeInfo,
    AssetUsage,
    AttachAssetRequest,
    LectureAssetCreate,
    LectureAssetResponse,
    LectureAssetUpdate,
    ModuleAssetLink,
    ReorderRequest,
    TrainingModuleCreate,
    TrainingModuleDetail,
    TrainingModuleResponse,
    TrainingModuleUpdate,
    TrainingProgramCreate,
    TrainingProgramDetail,
    TrainingProgramResponse,
    TrainingProgramUpdate,
)

router = APIRouter()


# ============================================
# Serialisation helpers
# ============================================


def _program_out(program, module_count: int = 0) -> TrainingProgramResponse:
    return TrainingProgramResponse(
        id=program.id,
        title=program.title,
        slug=program.slug,
        summary=program.summary,
        description=program.description,
        course_id=program.course_id,
        delivery_mode=program.delivery_mode,
        level=program.level,
        duration=program.duration,
        cover_image=program.cover_image,
        tags=load_tags(program.tags_json),
        status=program.status,
        display_order=program.display_order,
        is_active=program.is_active,
        module_count=module_count,
        created_at=program.created_at,
        updated_at=program.updated_at,
    )


def _module_out(module, asset_count: int = 0) -> TrainingModuleResponse:
    return TrainingModuleResponse(
        id=module.id,
        program_id=module.program_id,
        title=module.title,
        slug=module.slug,
        description=module.description,
        display_order=module.display_order,
        estimated_minutes=module.estimated_minutes,
        status=module.status,
        asset_count=asset_count,
        created_at=module.created_at,
        updated_at=module.updated_at,
    )


# ============================================
# Asset type registry
# ============================================


@router.get("/asset-types", response_model=List[AssetTypeInfo])
async def list_asset_types(
    current_admin: User = Depends(get_current_admin_user),
) -> List[AssetTypeInfo]:
    """Publish the asset-type registry so the admin UI and the API agree on the rules."""
    return [
        AssetTypeInfo(
            value=t.value,
            label=ASSET_TYPE_RULES[t].label,
            storage_kind=ASSET_TYPE_RULES[t].kind.value,
            max_size_mb=ASSET_TYPE_RULES[t].max_size_mb,
            allowed_content_types=ASSET_TYPE_RULES[t].allowed_content_types,
            allowed_extensions=ASSET_TYPE_RULES[t].allowed_extensions,
        )
        for t in ASSET_TYPES_ENABLED
    ]


# ============================================
# Programmes
# ============================================


@router.get("/programs")
async def list_programs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    course_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> JSONResponse:
    programs, total = await training_program_crud.search(
        db, skip=skip, limit=limit, status=status_filter, course_id=course_id, search=search
    )
    counts = await training_program_crud.module_counts(db, [p.id for p in programs])
    data = [_program_out(p, counts.get(p.id, 0)).model_dump(mode="json") for p in programs]
    return JSONResponse(content=data, headers={"X-Total-Count": str(total)})


@router.post("/programs", response_model=TrainingProgramDetail, status_code=status.HTTP_201_CREATED)
async def create_program(
    payload: TrainingProgramCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingProgramDetail:
    if await training_program_crud.get_by_slug(db, payload.slug):
        raise ConflictError(f"A training programme with slug '{payload.slug}' already exists")

    program = await training_program_crud.create_from_schema(db, obj_in=payload)
    return TrainingProgramDetail(**_program_out(program).model_dump(), modules=[])


@router.get("/programs/{program_id}", response_model=TrainingProgramDetail)
async def get_program(
    program_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingProgramDetail:
    program = await training_program_crud.get_with_modules(db, program_id)
    if not program:
        raise NotFoundError("Training programme")

    counts = await training_module_crud.asset_counts(db, [m.id for m in program.modules])
    modules = [_module_out(m, counts.get(m.id, 0)) for m in program.modules]
    return TrainingProgramDetail(
        **_program_out(program, len(program.modules)).model_dump(), modules=modules
    )


@router.put("/programs/{program_id}", response_model=TrainingProgramResponse)
async def update_program(
    program_id: int,
    payload: TrainingProgramUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingProgramResponse:
    program = await training_program_crud.get(db, program_id)
    if not program:
        raise NotFoundError("Training programme")

    if payload.slug and payload.slug != program.slug:
        clash = await training_program_crud.get_by_slug(db, payload.slug)
        if clash and clash.id != program_id:
            raise ConflictError(f"A training programme with slug '{payload.slug}' already exists")

    program = await training_program_crud.update_from_schema(db, db_obj=program, obj_in=payload)
    return _program_out(program)


@router.delete("/programs/{program_id}", response_model=MessageResponse)
async def delete_program(
    program_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    program = await training_program_crud.get(db, program_id)
    if not program:
        raise NotFoundError("Training programme")

    # Modules cascade; their asset *links* cascade too. The assets themselves survive,
    # which is the point of a shared library.
    await training_program_crud.delete(db, id=program_id)
    return MessageResponse(message="Training programme deleted")


# ============================================
# Modules
# ============================================


@router.get("/programs/{program_id}/modules", response_model=List[TrainingModuleResponse])
async def list_modules(
    program_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> List[TrainingModuleResponse]:
    if not await training_program_crud.get(db, program_id):
        raise NotFoundError("Training programme")

    modules = await training_module_crud.list_for_program(db, program_id)
    counts = await training_module_crud.asset_counts(db, [m.id for m in modules])
    return [_module_out(m, counts.get(m.id, 0)) for m in modules]


@router.post(
    "/programs/{program_id}/modules",
    response_model=TrainingModuleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_module(
    program_id: int,
    payload: TrainingModuleCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingModuleResponse:
    if not await training_program_crud.get(db, program_id):
        raise NotFoundError("Training programme")

    if await training_module_crud.get_by_slug(db, program_id, payload.slug):
        raise ConflictError(f"Module slug '{payload.slug}' is already used in this programme")

    data = payload.model_dump(exclude_unset=True)
    if not data.get("display_order"):
        data["display_order"] = await training_module_crud.next_order(db, program_id)

    module = await training_module_crud.create(db, obj_in={**data, "program_id": program_id})
    return _module_out(module)


@router.put("/programs/{program_id}/modules/order", response_model=MessageResponse)
async def reorder_modules(
    program_id: int,
    payload: ReorderRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    if not await training_program_crud.get(db, program_id):
        raise NotFoundError("Training programme")

    await training_module_crud.reorder(db, program_id, payload.items)
    return MessageResponse(message="Module order updated")


@router.get("/modules/{module_id}", response_model=TrainingModuleDetail)
async def get_module(
    module_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingModuleDetail:
    module = await training_module_crud.get_with_assets(db, module_id)
    if not module:
        raise NotFoundError("Module")

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
        **_module_out(module, len(assets)).model_dump(), assets=assets
    )


@router.put("/modules/{module_id}", response_model=TrainingModuleResponse)
async def update_module(
    module_id: int,
    payload: TrainingModuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingModuleResponse:
    module = await training_module_crud.get(db, module_id)
    if not module:
        raise NotFoundError("Module")

    if payload.slug and payload.slug != module.slug:
        clash = await training_module_crud.get_by_slug(db, module.program_id, payload.slug)
        if clash and clash.id != module_id:
            raise ConflictError(f"Module slug '{payload.slug}' is already used in this programme")

    module = await training_module_crud.update(db, db_obj=module, obj_in=payload)
    return _module_out(module)


@router.delete("/modules/{module_id}", response_model=MessageResponse)
async def delete_module(
    module_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    if not await training_module_crud.get(db, module_id):
        raise NotFoundError("Module")

    await training_module_crud.delete(db, id=module_id)
    return MessageResponse(message="Module deleted")


# ============================================
# Module <-> asset placement
# ============================================


@router.post(
    "/modules/{module_id}/assets",
    response_model=ModuleAssetLink,
    status_code=status.HTTP_201_CREATED,
)
async def attach_asset(
    module_id: int,
    payload: AttachAssetRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> ModuleAssetLink:
    if not await training_module_crud.get(db, module_id):
        raise NotFoundError("Module")

    asset = await lecture_asset_crud.get(db, payload.asset_id)
    if not asset:
        raise NotFoundError("Lecture asset")

    if await module_asset_crud.get_link(db, module_id, payload.asset_id):
        raise ConflictError("That asset is already attached to this module")

    link = await module_asset_crud.attach(
        db,
        module_id=module_id,
        asset_id=payload.asset_id,
        display_order=payload.display_order,
        is_required=payload.is_required,
        notes=payload.notes,
    )
    return ModuleAssetLink(
        id=link.id,
        asset_id=link.asset_id,
        display_order=link.display_order,
        is_required=link.is_required,
        notes=link.notes,
        asset=await asset_to_response(db, asset),
    )


@router.put("/modules/{module_id}/assets/order", response_model=MessageResponse)
async def reorder_module_assets(
    module_id: int,
    payload: ReorderRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    if not await training_module_crud.get(db, module_id):
        raise NotFoundError("Module")

    await module_asset_crud.reorder(db, module_id, payload.items)
    return MessageResponse(message="Asset order updated")


@router.delete("/modules/{module_id}/assets/{asset_id}", response_model=MessageResponse)
async def detach_asset(
    module_id: int,
    asset_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    link = await module_asset_crud.get_link(db, module_id, asset_id)
    if not link:
        raise NotFoundError("Asset placement")

    await module_asset_crud.delete(db, id=link.id)
    return MessageResponse(message="Asset detached from module")


# ============================================
# Asset library
# ============================================


@router.get("/assets/tags")
async def list_asset_tags(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> List[str]:
    return await lecture_asset_crud.distinct_tags(db)


@router.get("/assets")
async def list_assets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    asset_type: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    program_id: Optional[int] = Query(None),
    module_id: Optional[int] = Query(None),
    tag: Optional[str] = Query(None),
    unassigned: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> JSONResponse:
    if asset_type:
        try:
            AssetType(asset_type)
        except ValueError:
            raise ValidationError(f"Unknown asset type: {asset_type}")

    assets, total = await lecture_asset_crud.search(
        db,
        skip=skip,
        limit=limit,
        asset_type=asset_type,
        status=status_filter,
        search=search,
        program_id=program_id,
        module_id=module_id,
        tag=tag,
        unassigned=unassigned,
    )
    data = [(await asset_to_response(db, a)).model_dump(mode="json") for a in assets]
    return JSONResponse(content=data, headers={"X-Total-Count": str(total)})


@router.post("/assets", response_model=LectureAssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    payload: LectureAssetCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> LectureAssetResponse:
    """Create a reusable lecture asset.

    The request body is a discriminated union on ``asset_type``, so the payload is
    validated against that specific type before it reaches the database.
    """
    asset_type = AssetType(payload.asset_type)
    if asset_type not in ASSET_TYPES_ENABLED:
        raise ValidationError(f"Asset type '{asset_type.value}' is not available yet")

    asset = await lecture_asset_crud.create_from_union(
        db, obj_in=payload, created_by_id=current_admin.id
    )
    return await asset_to_response(db, asset)


@router.get("/assets/{asset_id}", response_model=LectureAssetResponse)
async def get_asset(
    asset_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> LectureAssetResponse:
    asset = await lecture_asset_crud.get(db, asset_id)
    if not asset:
        raise NotFoundError("Lecture asset")
    return await asset_to_response(db, asset)


@router.get("/assets/{asset_id}/usages", response_model=List[AssetUsage])
async def get_asset_usages(
    asset_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> List[AssetUsage]:
    """List every module this asset appears in.

    Assets are shared, so an edit here changes every lecture that uses it. The UI shows
    this before editing so that is a decision rather than a surprise.
    """
    if not await lecture_asset_crud.get(db, asset_id):
        raise NotFoundError("Lecture asset")
    return [AssetUsage(**u) for u in await lecture_asset_crud.usages(db, asset_id)]


@router.post("/assets/bulk-programs")
async def bulk_asset_programs(
    asset_ids: List[int] = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> dict:
    """Return program associations for a batch of asset IDs."""
    usages = await lecture_asset_crud.bulk_program_usages(db, asset_ids[:100])
    return {"data": {str(k): v for k, v in usages.items()}}


@router.put("/assets/{asset_id}", response_model=LectureAssetResponse)
async def update_asset(
    asset_id: int,
    payload: LectureAssetUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> LectureAssetResponse:
    asset = await lecture_asset_crud.get(db, asset_id)
    if not asset:
        raise NotFoundError("Lecture asset")

    asset = await lecture_asset_crud.update_from_schema(db, db_obj=asset, obj_in=payload)
    return await asset_to_response(db, asset)


@router.delete("/assets/{asset_id}", response_model=MessageResponse)
async def delete_asset(
    asset_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    asset = await lecture_asset_crud.get(db, asset_id)
    if not asset:
        raise NotFoundError("Lecture asset")

    # An asset in use must not disappear from under the modules teaching from it. The
    # DB enforces this with RESTRICT; check first so the caller gets a useful message
    # instead of an integrity error.
    usage_count = await lecture_asset_crud.usage_count(db, asset_id)
    if usage_count:
        raise ConflictError(
            f"This asset is used by {usage_count} module(s). Detach it from them, or "
            f"archive the asset instead of deleting it."
        )

    try:
        await lecture_asset_crud.delete(db, id=asset_id)
    except IntegrityError:
        raise ConflictError("This asset is still referenced and cannot be deleted")
    return MessageResponse(message="Lecture asset deleted")


@router.post("/assets/bulk-delete")
async def bulk_delete_assets(
    asset_ids: List[int] = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> dict:
    """Bulk delete a list of assets by ID. Assets in use by modules are skipped."""
    deleted = 0
    failed = 0
    in_use = 0

    for aid in asset_ids[:200]:
        asset = await lecture_asset_crud.get(db, aid)
        if not asset:
            failed += 1
            continue

        usage_count = await lecture_asset_crud.usage_count(db, aid)
        if usage_count > 0:
            in_use += 1
            continue

        try:
            await lecture_asset_crud.delete(db, id=aid)
            deleted += 1
        except IntegrityError:
            failed += 1

    return {
        "deleted": deleted,
        "failed": failed,
        "in_use": in_use,
        "message": f"Successfully deleted {deleted} asset(s)."
        + (f" {in_use} asset(s) were skipped because they are attached to modules." if in_use > 0 else ""),
    }
