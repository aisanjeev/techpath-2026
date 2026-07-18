"""Tests for training content: the asset registry, the typed payload union, and reuse."""
import uuid

import pytest
from pydantic import TypeAdapter, ValidationError as PydanticValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    ASSET_TYPE_RULES,
    ASSET_TYPES_DISABLED,
    ASSET_TYPES_ENABLED,
    AssetStorageKind,
    AssetType,
    asset_rule,
)
from app.crud.training import (
    lecture_asset_crud,
    load_config,
    load_tags,
    module_asset_crud,
    training_module_crud,
    training_program_crud,
)
from app.schemas.training import (
    LectureAssetCreate,
    ReorderItem,
    TrainingModuleCreate,
    TrainingProgramCreate,
)

asset_adapter = TypeAdapter(LectureAssetCreate)


class TestAssetRegistry:
    def test_every_type_has_a_rule(self) -> None:
        """A type without a rule would crash serialisation at runtime, not at import."""
        missing = [t for t in AssetType if t not in ASSET_TYPE_RULES]
        assert missing == []

    def test_html_bundle_is_withheld(self) -> None:
        assert AssetType.HTML_BUNDLE in ASSET_TYPES_DISABLED
        assert AssetType.HTML_BUNDLE not in ASSET_TYPES_ENABLED
        assert len(ASSET_TYPES_ENABLED) == len(list(AssetType)) - 1

    def test_file_types_declare_limits(self) -> None:
        """A file type with no size cap or MIME list would accept anything."""
        for t, rule in ASSET_TYPE_RULES.items():
            if rule.kind is AssetStorageKind.FILE:
                assert rule.max_size_mb > 0, f"{t.value} has no size limit"
                assert rule.allowed_content_types, f"{t.value} allows any content type"
                assert rule.allowed_extensions, f"{t.value} allows any extension"

    def test_video_limit_is_larger_than_pdf(self) -> None:
        assert asset_rule(AssetType.VIDEO).max_size_mb > asset_rule(AssetType.PDF).max_size_mb


class TestAssetPayloadUnion:
    """The table is one wide row; these are what stop the payload being a free-for-all."""

    def test_markdown_requires_a_body(self) -> None:
        with pytest.raises(PydanticValidationError):
            asset_adapter.validate_python({"asset_type": "markdown", "title": "Empty"})

    def test_youtube_requires_a_valid_url(self) -> None:
        with pytest.raises(PydanticValidationError):
            asset_adapter.validate_python(
                {"asset_type": "youtube", "title": "Bad", "external_url": "not-a-url"}
            )

    def test_file_asset_requires_media_file_id(self) -> None:
        with pytest.raises(PydanticValidationError):
            asset_adapter.validate_python({"asset_type": "pdf", "title": "No file"})

    def test_quiz_correct_index_must_be_in_range(self) -> None:
        with pytest.raises(PydanticValidationError):
            asset_adapter.validate_python(
                {
                    "asset_type": "quiz",
                    "title": "Bad quiz",
                    "questions": [
                        {"question": "2+2?", "options": ["3", "4"], "correct_index": 7}
                    ],
                }
            )

    def test_unknown_type_is_rejected(self) -> None:
        with pytest.raises(PydanticValidationError):
            asset_adapter.validate_python({"asset_type": "hologram", "title": "Nope"})

    def test_payload_of_the_wrong_type_is_rejected(self) -> None:
        """A markdown body on a quiz must not quietly validate."""
        with pytest.raises(PydanticValidationError):
            asset_adapter.validate_python(
                {"asset_type": "quiz", "title": "Wrong shape", "body": "# hello"}
            )

    def test_valid_payloads_round_trip(self) -> None:
        ok = asset_adapter.validate_python(
            {"asset_type": "markdown", "title": "Intro", "body": "# Python"}
        )
        assert ok.body == "# Python"


class TestAssetPersistence:
    async def _asset(self, db: AsyncSession, payload: dict):
        return await lecture_asset_crud.create_from_union(
            db, obj_in=asset_adapter.validate_python(payload)
        )

    async def test_inline_text_lands_in_body(self, test_db: AsyncSession) -> None:
        asset = await self._asset(
            test_db, {"asset_type": "markdown", "title": "M", "body": "# Hi"}
        )
        assert asset.body == "# Hi"
        assert asset.external_url is None
        assert asset.media_file_id is None

    async def test_link_lands_in_external_url(self, test_db: AsyncSession) -> None:
        asset = await self._asset(
            test_db,
            {"asset_type": "youtube", "title": "Vid", "external_url": "https://youtu.be/abc"},
        )
        assert asset.external_url == "https://youtu.be/abc"
        assert asset.body is None

    async def test_structured_lands_in_config_json(self, test_db: AsyncSession) -> None:
        asset = await self._asset(
            test_db,
            {
                "asset_type": "quiz",
                "title": "Q",
                "questions": [{"question": "2+2?", "options": ["3", "4"], "correct_index": 1}],
                "pass_mark_percent": 50,
            },
        )
        config = load_config(asset.config_json)
        assert config["pass_mark_percent"] == 50
        assert config["questions"][0]["correct_index"] == 1
        assert asset.body is None

    async def test_code_snippet_keeps_language(self, test_db: AsyncSession) -> None:
        asset = await self._asset(
            test_db,
            {
                "asset_type": "code_snippet",
                "title": "Loop",
                "body": "for i in range(5): print(i)",
                "language": "python",
            },
        )
        assert load_config(asset.config_json) == {"language": "python"}

    async def test_public_id_is_a_random_uuid4(self, test_db: AsyncSession) -> None:
        """Sandboxed asset URLs are built from public_id, so it must not be guessable
        from the sequential primary key."""
        a = await self._asset(test_db, {"asset_type": "notes", "title": "A", "body": "a"})
        b = await self._asset(test_db, {"asset_type": "notes", "title": "B", "body": "b"})

        assert a.public_id != b.public_id
        assert uuid.UUID(a.public_id).version == 4
        # Consecutive rows must not yield adjacent handles.
        assert b.id == a.id + 1
        assert uuid.UUID(b.public_id).int - uuid.UUID(a.public_id).int != 1


class TestAssetReuse:
    """The whole point of the asset library: author once, place many times."""

    async def _fixture(self, db: AsyncSession):
        program = await training_program_crud.create_from_schema(
            db, obj_in=TrainingProgramCreate(title="Python", slug="python")
        )
        m1 = await training_module_crud.create(
            db,
            obj_in={
                **TrainingModuleCreate(title="Intro", slug="intro").model_dump(),
                "program_id": program.id,
            },
        )
        m2 = await training_module_crud.create(
            db,
            obj_in={
                **TrainingModuleCreate(title="Loops", slug="loops").model_dump(),
                "program_id": program.id,
            },
        )
        asset = await lecture_asset_crud.create_from_union(
            db,
            obj_in=asset_adapter.validate_python(
                {"asset_type": "cheat_sheet", "title": "Syntax", "body": "..."}
            ),
        )
        return program, m1, m2, asset

    async def test_one_asset_can_live_in_two_modules(self, test_db: AsyncSession) -> None:
        _, m1, m2, asset = await self._fixture(test_db)

        await module_asset_crud.attach(test_db, module_id=m1.id, asset_id=asset.id)
        await module_asset_crud.attach(test_db, module_id=m2.id, asset_id=asset.id)

        assert await lecture_asset_crud.usage_count(test_db, asset.id) == 2
        usages = await lecture_asset_crud.usages(test_db, asset.id)
        assert {u["module_title"] for u in usages} == {"Intro", "Loops"}
        # One row, two placements — not two copies.
        assert all(u["program_title"] == "Python" for u in usages)

    async def test_editing_a_shared_asset_propagates(self, test_db: AsyncSession) -> None:
        _, m1, m2, asset = await self._fixture(test_db)
        await module_asset_crud.attach(test_db, module_id=m1.id, asset_id=asset.id)
        await module_asset_crud.attach(test_db, module_id=m2.id, asset_id=asset.id)

        asset.title = "Syntax v2"
        test_db.add(asset)
        await test_db.flush()

        for module_id in (m1.id, m2.id):
            module = await training_module_crud.get_with_assets(test_db, module_id)
            assert module.asset_links[0].asset.title == "Syntax v2"

    async def test_attach_is_idempotent_per_module(self, test_db: AsyncSession) -> None:
        _, m1, _, asset = await self._fixture(test_db)
        await module_asset_crud.attach(test_db, module_id=m1.id, asset_id=asset.id)
        assert await module_asset_crud.get_link(test_db, m1.id, asset.id) is not None

    async def test_placement_order_is_applied(self, test_db: AsyncSession) -> None:
        _, m1, _, asset = await self._fixture(test_db)
        second = await lecture_asset_crud.create_from_union(
            test_db,
            obj_in=asset_adapter.validate_python(
                {"asset_type": "notes", "title": "Second", "body": "x"}
            ),
        )
        l1 = await module_asset_crud.attach(test_db, module_id=m1.id, asset_id=asset.id)
        l2 = await module_asset_crud.attach(test_db, module_id=m1.id, asset_id=second.id)
        assert l1.display_order < l2.display_order

        await module_asset_crud.reorder(
            test_db,
            m1.id,
            [ReorderItem(id=l1.id, display_order=5), ReorderItem(id=l2.id, display_order=1)],
        )
        module = await training_module_crud.get_with_assets(test_db, m1.id)
        assert [link.asset.title for link in module.asset_links] == ["Second", "Syntax"]

    async def test_detach_leaves_the_asset_intact(self, test_db: AsyncSession) -> None:
        _, m1, _, asset = await self._fixture(test_db)
        link = await module_asset_crud.attach(test_db, module_id=m1.id, asset_id=asset.id)

        await module_asset_crud.delete(test_db, id=link.id)

        assert await lecture_asset_crud.get(test_db, asset.id) is not None
        assert await lecture_asset_crud.usage_count(test_db, asset.id) == 0


class TestProgramCourseLink:
    async def test_course_id_is_optional(self, test_db: AsyncSession) -> None:
        """Offline-only training has no public course, so this must not be required."""
        program = await training_program_crud.create_from_schema(
            db=test_db, obj_in=TrainingProgramCreate(title="Offline", slug="offline")
        )
        assert program.course_id is None
        assert program.delivery_mode == "offline"

    async def test_tags_round_trip(self, test_db: AsyncSession) -> None:
        program = await training_program_crud.create_from_schema(
            test_db,
            obj_in=TrainingProgramCreate(title="T", slug="t", tags=["python", "beginner"]),
        )
        assert load_tags(program.tags_json) == ["python", "beginner"]

    def test_malformed_tags_do_not_explode(self) -> None:
        """Legacy or hand-edited rows must not 500 a list page."""
        assert load_tags("not json") == []
        assert load_tags('{"a": 1}') == []
        assert load_tags(None) == []
