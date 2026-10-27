import pytest
from pydantic import ValidationError

from app.contracts import BookingCommand, BookingResult, StayQuery


def test_stay_query_rejects_reversed_dates() -> None:
    with pytest.raises(ValidationError):
        StayQuery(
            property_id="demo-coimbatore-001",
            check_in="2026-11-12",
            check_out="2026-11-10",
            guests=2,
        )


def test_booking_command_requires_guest_confirmation() -> None:
    with pytest.raises(ValidationError, match="guest confirmation is required"):
        BookingCommand(
            property_id="demo-coimbatore-001",
            check_in="2026-11-10",
            check_out="2026-11-12",
            guests=2,
            idempotency_key="contract-test-01",
            guest_confirmed=False,
        )


def test_confirmed_booking_requires_authoritative_reference() -> None:
    with pytest.raises(ValidationError, match="authoritative result and booking reference"):
        BookingResult(status="confirmed", booking_reference="fake-demo-reference")


def test_pending_booking_result_does_not_claim_confirmation() -> None:
    result = BookingResult(status="pending")

    assert result.status == "pending"
    assert result.authoritative is False
    assert result.booking_reference is None


def test_authoritative_confirmation_requires_reference() -> None:
    result = BookingResult(
        status="confirmed",
        booking_reference="real-reference-from-adapter",
        authoritative=True,
    )

    assert result.status == "confirmed"
    assert result.authoritative is True
