"""Tests for streaming lecture-asset uploads and their per-type validation."""
import pytest
from fastapi import UploadFile

from app.api.v1.endpoints.uploads import (
    CHUNK_SIZE,
    _spool_and_hash,
    _validate_asset_file,
)
from app.core.constants import AssetType, asset_rule
from app.core.exceptions import ValidationError


def _upload(content: bytes, filename: str, content_type: str) -> UploadFile:
    import io

    return UploadFile(
        file=io.BytesIO(content),
        filename=filename,
        headers={"content-type": content_type},
    )


class TestStreamAndHash:
    async def test_hashes_and_sizes_correctly(self) -> None:
        import hashlib

        content = b"%PDF-1.4 hello world"
        spool, digest, size, head = await _spool_and_hash(_upload(content, "a.pdf", "application/pdf"), 1024)

        assert digest == hashlib.sha256(content).hexdigest()
        assert size == len(content)
        assert head.startswith(b"%PDF-")
        assert spool.read() == content
        spool.close()

    async def test_rejects_oversize_before_buffering_everything(self) -> None:
        """The cap must bite during streaming, not after the whole body is in memory."""
        oversized = b"x" * (3 * CHUNK_SIZE)
        with pytest.raises(ValidationError, match="too large"):
            await _spool_and_hash(_upload(oversized, "big.mp4", "video/mp4"), 2 * CHUNK_SIZE)

    async def test_rejects_empty_file(self) -> None:
        with pytest.raises(ValidationError, match="empty"):
            await _spool_and_hash(_upload(b"", "empty.pdf", "application/pdf"), 1024)

    async def test_handles_multi_chunk_content(self) -> None:
        content = b"%PDF-" + b"a" * (CHUNK_SIZE * 2)
        spool, _, size, head = await _spool_and_hash(
            _upload(content, "big.pdf", "application/pdf"), 10 * CHUNK_SIZE
        )
        assert size == len(content)
        # head must come from the first chunk only
        assert head.startswith(b"%PDF-")
        spool.close()


class TestAssetFileValidation:
    def test_accepts_a_well_formed_pdf(self) -> None:
        _validate_asset_file(_upload(b"", "notes.pdf", "application/pdf"), AssetType.PDF, b"%PDF-1.7")

    def test_rejects_wrong_content_type(self) -> None:
        with pytest.raises(ValidationError, match="Invalid content type"):
            _validate_asset_file(
                _upload(b"", "notes.pdf", "image/png"), AssetType.PDF, b"%PDF-1.7"
            )

    def test_rejects_wrong_extension(self) -> None:
        with pytest.raises(ValidationError, match="Invalid file extension"):
            _validate_asset_file(
                _upload(b"", "notes.txt", "application/pdf"), AssetType.PDF, b"%PDF-1.7"
            )

    def test_rejects_content_type_lie(self) -> None:
        """A renamed executable claiming to be a PDF must not get through on the
        client's say-so — the bytes decide."""
        with pytest.raises(ValidationError, match="do not look like"):
            _validate_asset_file(
                _upload(b"", "evil.pdf", "application/pdf"), AssetType.PDF, b"MZ\x90\x00"
            )

    def test_rejects_zip_that_is_not_a_zip(self) -> None:
        with pytest.raises(ValidationError, match="do not look like"):
            _validate_asset_file(
                _upload(b"", "x.zip", "application/zip"), AssetType.ZIP, b"not a zip"
            )

    def test_accepts_real_zip_magic(self) -> None:
        _validate_asset_file(
            _upload(b"", "x.zip", "application/zip"), AssetType.ZIP, b"PK\x03\x04\x14\x00"
        )

    def test_pptx_is_sniffed_as_a_zip_container(self) -> None:
        _validate_asset_file(
            _upload(
                b"",
                "deck.pptx",
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ),
            AssetType.PPT,
            b"PK\x03\x04\x14\x00",
        )

    def test_video_is_not_sniffed_but_still_type_checked(self) -> None:
        """We have no reliable prefix for every container, so mp4 passes on type+ext."""
        _validate_asset_file(
            _upload(b"", "clip.mp4", "video/mp4"), AssetType.VIDEO, b"\x00\x00\x00 ftypmp42"
        )
        with pytest.raises(ValidationError):
            _validate_asset_file(
                _upload(b"", "clip.avi", "video/mp4"), AssetType.VIDEO, b"\x00\x00\x00 "
            )


class TestRegistryLimits:
    def test_video_cap_is_500mb(self) -> None:
        assert asset_rule(AssetType.VIDEO).max_size_mb == 500

    def test_pdf_cap_is_50mb(self) -> None:
        assert asset_rule(AssetType.PDF).max_size_mb == 50
