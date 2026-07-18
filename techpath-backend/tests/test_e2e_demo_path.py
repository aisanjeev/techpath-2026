"""End-to-end walk of the Phase 1 demo path.

Exercises the whole chain in one go, the way a person actually would:

    provision a trainer -> they sign in via Firebase -> admin builds a program with a
    module and three assets -> reorders them -> syncs the roster -> links a batch to the
    program -> trainer sees their batch -> picks a module -> starts presenting -> a join
    code is minted.

The per-area suites cover the edges; this one proves the pieces fit together.
"""
from datetime import datetime, timezone

import pytest
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.auth import provision_user
from app.api.v1.endpoints.trainer import _assert_owns_batch
from app.core.constants import SessionStatus, UserRole
from app.crud.training import (
    lecture_asset_crud,
    module_asset_crud,
    training_module_crud,
    training_program_crud,
)
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.crud.user import user_crud
from app.models.user import User
from app.schemas.training import (
    LectureAssetCreate,
    ReorderItem,
    TrainingModuleCreate,
    TrainingProgramCreate,
)
from app.schemas.user import UserProvision
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService

asset_adapter = TypeAdapter(LectureAssetCreate)

TRAINER_EMAIL = "techpath.biz@gmail.com"


async def test_full_demo_path(test_db: AsyncSession) -> None:
    # --- 1. An admin exists and provisions a trainer -------------------------------
    admin = User(
        email="admin@techpath.biz",
        name="Admin",
        firebase_uid="uid-admin",
        role=UserRole.ADMIN.value,
        is_active=True,
    )
    test_db.add(admin)
    await test_db.flush()

    await provision_user(
        UserProvision(email=TRAINER_EMAIL, name="Sanjeev", role="trainer"),
        db=test_db,
        current_admin=admin,
    )

    # --- 2. The trainer signs in with Firebase for the first time -------------------
    # Their account is created in the Firebase console; the local row is claimed by
    # email, so the provisioned role survives rather than being reset.
    trainer = await user_crud.get_or_create_from_firebase(
        test_db, "uid-trainer-firebase", TRAINER_EMAIL, "Sanjeev"
    )
    assert trainer.role == "trainer"
    assert trainer.is_active is True

    # --- 3. The admin builds a training program ------------------------------------
    program = await training_program_crud.create_from_schema(
        test_db,
        obj_in=TrainingProgramCreate(
            title="Python Fundamentals",
            slug="python-fundamentals",
            summary="Zero to comfortable",
            status="published",
            # No course_id: this is offline training with no public course page.
        ),
    )
    assert program.course_id is None

    module = await training_module_crud.create(
        test_db,
        obj_in={
            **TrainingModuleCreate(
                title="Introduction to Python", slug="intro", status="published"
            ).model_dump(),
            "program_id": program.id,
        },
    )

    # --- 4. Three assets of three different kinds ----------------------------------
    markdown = await lecture_asset_crud.create_from_union(
        test_db,
        obj_in=asset_adapter.validate_python(
            {
                "asset_type": "markdown",
                "title": "What is Python?",
                "body": "# Python\n\nA readable language.",
                "status": "published",
            }
        ),
        created_by_id=admin.id,
    )
    youtube = await lecture_asset_crud.create_from_union(
        test_db,
        obj_in=asset_adapter.validate_python(
            {
                "asset_type": "youtube",
                "title": "Install Python",
                "external_url": "https://youtu.be/install",
                "status": "published",
            }
        ),
        created_by_id=admin.id,
    )
    quiz = await lecture_asset_crud.create_from_union(
        test_db,
        obj_in=asset_adapter.validate_python(
            {
                "asset_type": "quiz",
                "title": "Check yourself",
                "questions": [
                    {"question": "print() does?", "options": ["prints", "eats"], "correct_index": 0}
                ],
                "status": "published",
            }
        ),
        created_by_id=admin.id,
    )

    # Each payload landed in the column its storage kind dictates.
    assert markdown.body and not markdown.external_url
    assert youtube.external_url and not youtube.body
    assert quiz.config_json and not quiz.body

    # --- 5. Place them in the module, then reorder ---------------------------------
    l1 = await module_asset_crud.attach(test_db, module_id=module.id, asset_id=markdown.id)
    l2 = await module_asset_crud.attach(test_db, module_id=module.id, asset_id=youtube.id)
    l3 = await module_asset_crud.attach(test_db, module_id=module.id, asset_id=quiz.id)

    await module_asset_crud.reorder(
        test_db,
        module.id,
        [
            ReorderItem(id=l2.id, display_order=1),
            ReorderItem(id=l1.id, display_order=2),
            ReorderItem(id=l3.id, display_order=3),
        ],
    )
    detail = await training_module_crud.get_with_assets(test_db, module.id)
    assert [link.asset.title for link in detail.asset_links] == [
        "Install Python",
        "What is Python?",
        "Check yourself",
    ]

    # --- 6. Sync the roster from the external system -------------------------------
    results = await RosterSyncService(provider=MockRosterProvider()).sync_all(test_db)
    assert results["batches"]["created"] == 5
    assert results["students"]["created"] == 6

    # --- 7. Link a batch to the program (the one field that is ours) ---------------
    batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-001")
    batch.program_id = program.id
    test_db.add(batch)
    await test_db.flush()

    # --- 8. The trainer sees their own batches, and only their own -----------------
    mine = await training_batch_crud.get_by_trainer_email(test_db, trainer.email)
    assert batch.id in {b.id for b in mine}

    foreign = await training_batch_crud.get_by_external_id(test_db, "BATCH-003")
    from app.core.exceptions import ForbiddenError

    with pytest.raises(ForbiddenError):
        await _assert_owns_batch(test_db, trainer, foreign)

    # --- 9. Create a session and start presenting ----------------------------------
    session = await training_session_crud.create(
        test_db,
        obj_in={
            "batch_id": batch.id,
            "module_id": module.id,
            "trainer_user_id": trainer.id,
            "title": module.title,
            "scheduled_start": datetime.now(timezone.utc),
            "status": SessionStatus.SCHEDULED.value,
        },
    )
    assert session.join_code is None

    session.join_code = await training_session_crud.generate_join_code(test_db)
    session.status = SessionStatus.LIVE.value
    session.started_at = datetime.now(timezone.utc)
    test_db.add(session)
    await test_db.flush()

    # --- 10. It is live, with a code students can use ------------------------------
    live = await training_session_crud.get_with_relations(test_db, session.id)
    assert live.status == "live"
    assert live.join_code and len(live.join_code) == 6 and live.join_code.isdigit()
    assert live.module.title == "Introduction to Python"
    assert live.batch.name == "Python Fundamentals — July Morning"

    today = await training_session_crud.get_today_for_trainer(test_db, trainer.email)
    assert session.id in {s.id for s in today}

    # The roster the trainer will take attendance against resolves with no network.
    roster = await training_batch_crud.students(test_db, batch.id)
    assert len(roster) == 3
