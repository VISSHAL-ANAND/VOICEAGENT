import pytest
from pydantic import ValidationError

from app.voice_contracts import (
    AssistantTranscriptEvent,
    SessionEndedEvent,
    SessionErrorEvent,
    SessionStartedEvent,
    UserTranscriptEvent,
    voice_session_event_adapter,
)


def test_session_started_accepts_supported_language() -> None:
    event = SessionStartedEvent(
        kind="session_started",
        session_id="call-123",
        language="ta",
    )

    assert event.session_id == "call-123"
    assert event.language == "ta"


def test_session_started_rejects_unsupported_language() -> None:
    with pytest.raises(ValidationError):
        SessionStartedEvent(
            kind="session_started",
            session_id="call-123",
            language="fr",
        )


def test_user_transcript_requires_nonempty_text() -> None:
    with pytest.raises(ValidationError):
        UserTranscriptEvent(
            kind="user_transcript",
            session_id="call-123",
            text="   ",
            language="en",
        )


def test_transcript_rejects_unexpected_fields() -> None:
    with pytest.raises(ValidationError):
        UserTranscriptEvent(
            kind="user_transcript",
            session_id="call-123",
            text="I need a room",
            language="en",
            raw_provider_payload={"secret": "must-not-cross-boundary"},
        )


def test_event_adapter_selects_model_by_kind() -> None:
    event = voice_session_event_adapter.validate_python(
        {
            "kind": "user_transcript",
            "session_id": "call-123",
            "text": "I need a room",
            "language": "en",
        }
    )

    assert isinstance(event, UserTranscriptEvent)
    assert event.text == "I need a room"


def test_session_end_reason_is_normalized() -> None:
    event = SessionEndedEvent(
        kind="session_ended",
        session_id="call-123",
        reason="caller_hangup",
    )

    assert event.reason == "caller_hangup"


def test_session_error_uses_safe_normalized_code() -> None:
    event = SessionErrorEvent(
        kind="session_error",
        session_id="call-123",
        code="provider_disconnected",
        retryable=True,
    )

    assert event.code == "provider_disconnected"
    assert event.retryable is True


def test_session_error_rejects_raw_provider_message_as_code() -> None:
    with pytest.raises(ValidationError):
        SessionErrorEvent(
            kind="session_error",
            session_id="call-123",
            code="Customer +91 9876543210 token=secret",
            retryable=False,
        )


def test_assistant_transcript_is_typed_and_language_tagged() -> None:
    event = AssistantTranscriptEvent(
        kind="assistant_transcript",
        session_id="call-123",
        text="How can I help you?",
        language="en",
    )

    assert event.text == "How can I help you?"
    assert event.language == "en"
