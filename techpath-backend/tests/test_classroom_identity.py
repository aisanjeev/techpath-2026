"""Tests for live classroom identity tokens: minting/decoding round-trips, the
cross-session rejection check, and the ``type: classroom`` claim gate. See
``app/services/classroom/identity.py``'s module docstring for why this token shape
exists (a student never gets a Firebase account).
"""
import pytest

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token
from app.services.classroom.identity import (
    decode_classroom_token,
    mint_classroom_token,
    mint_trainer_ws_token,
)


class TestStudentTokenRoundTrip:
    def test_round_trips_and_defaults_role_to_student(self) -> None:
        token = mint_classroom_token(
            session_id=42, participant_key="abc-123", display_name="Aarav"
        )

        claims = decode_classroom_token(token, expected_session_id=42)

        assert claims["participant_key"] == "abc-123"
        assert claims["session_id"] == 42
        assert claims["name"] == "Aarav"
        assert claims["role"] == "student"


class TestTrainerWsTokenRoundTrip:
    def test_round_trips_with_trainer_role(self) -> None:
        token = mint_trainer_ws_token(session_id=7, user_id=99, display_name="Sanjeev")

        claims = decode_classroom_token(token, expected_session_id=7)

        assert claims["role"] == "trainer"
        assert claims["session_id"] == 7
        assert claims["participant_key"] == "trainer:99"
        assert claims["name"] == "Sanjeev"


class TestCrossSessionRejection:
    def test_token_minted_for_one_session_is_rejected_for_another(self) -> None:
        token = mint_classroom_token(
            session_id=1, participant_key="key-1", display_name="Student A"
        )

        with pytest.raises(UnauthorizedError):
            decode_classroom_token(token, expected_session_id=2)


class TestClassroomTypeClaimGate:
    def test_token_missing_the_type_claim_is_rejected(self) -> None:
        token = create_access_token(
            data={
                "sub": "some-key",
                "session_id": 5,
                "name": "Someone",
                "role": "student",
                # 'type' deliberately omitted
            }
        )

        with pytest.raises(UnauthorizedError):
            decode_classroom_token(token, expected_session_id=5)

    def test_token_with_a_different_type_claim_is_rejected(self) -> None:
        token = create_access_token(
            data={
                "sub": "some-key",
                "session_id": 5,
                "name": "Someone",
                "type": "admin",
                "role": "student",
            }
        )

        with pytest.raises(UnauthorizedError):
            decode_classroom_token(token, expected_session_id=5)
