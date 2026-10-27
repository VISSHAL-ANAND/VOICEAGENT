"""Provider-neutral event contracts for voice sessions.

These contracts describe the boundary between a voice-provider adapter and the
conversation orchestrator. They intentionally do not prescribe audio codecs,
WebSocket framing, telephony events, or a vendor API.
"""

from collections.abc import AsyncIterator
from datetime import datetime
from typing import Annotated, Literal, Protocol, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_validator

VoiceLanguage: TypeAlias = Literal["ta", "hi", "en", "kn", "te"]


class VoiceEventBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1, max_length=128)
    occurred_at: datetime | None = None


class SessionStartedEvent(VoiceEventBase):
    kind: Literal["session_started"]
    language: VoiceLanguage


class UserTranscriptEvent(VoiceEventBase):
    kind: Literal["user_transcript"]
    text: str = Field(min_length=1, max_length=8000)
    language: VoiceLanguage

    @field_validator("text")
    @classmethod
    def reject_blank_transcript(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("transcript text must not be blank")
        return value


class AssistantTranscriptEvent(VoiceEventBase):
    kind: Literal["assistant_transcript"]
    text: str = Field(min_length=1, max_length=8000)
    language: VoiceLanguage

    @field_validator("text")
    @classmethod
    def reject_blank_transcript(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("transcript text must not be blank")
        return value


class SessionEndedEvent(VoiceEventBase):
    kind: Literal["session_ended"]
    reason: Literal[
        "caller_hangup",
        "provider_closed",
        "normal_completion",
        "unknown",
    ] = "unknown"


class SessionErrorEvent(VoiceEventBase):
    kind: Literal["session_error"]
    code: Literal[
        "provider_disconnected",
        "recognition_failed",
        "synthesis_failed",
        "session_not_found",
        "rate_limited",
        "unknown",
    ] = "unknown"
    retryable: bool = False


VoiceSessionEvent: TypeAlias = Annotated[
    SessionStartedEvent
    | UserTranscriptEvent
    | AssistantTranscriptEvent
    | SessionEndedEvent
    | SessionErrorEvent,
    Field(discriminator="kind"),
]

voice_session_event_adapter = TypeAdapter(VoiceSessionEvent)


class VoiceSessionPort(Protocol):
    """Interface consumed by the conversation orchestrator.

    A concrete adapter is responsible for mapping its vendor's audio and
    session protocol to these normalized events. Raw provider error messages
    should be mapped to the safe error codes above rather than forwarded.
    """

    async def start_session(
        self,
        session_id: str,
        preferred_language: VoiceLanguage | None = None,
    ) -> None: ...

    async def send_response(
        self,
        session_id: str,
        text: str,
        language: VoiceLanguage,
    ) -> None: ...

    async def end_session(self, session_id: str) -> None: ...

    def events(self) -> AsyncIterator[VoiceSessionEvent]: ...
