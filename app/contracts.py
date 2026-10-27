"""Provider-neutral internal contracts; not the external property API schema."""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Protocol

from pydantic import BaseModel, Field, model_validator


class StayQuery(BaseModel):
    property_id: str = Field(min_length=1, max_length=100)
    check_in: date
    check_out: date
    guests: int = Field(ge=1, le=12)

    @model_validator(mode="after")
    def validate_date_order(self) -> "StayQuery":
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self


class PropertyRecord(BaseModel):
    property_id: str
    name: str
    city: str
    supported_languages: list[str]
    amenities: list[str]


class AvailabilityResult(BaseModel):
    property_id: str
    check_in: date
    check_out: date
    guests: int
    status: Literal["available", "unavailable", "unknown"]
    total_price: Decimal | None = None
    currency: str | None = None
    quote_reference: str | None = None
    expires_at: datetime | None = None
    authoritative: bool = False


class BookingCommand(BaseModel):
    property_id: str = Field(min_length=1, max_length=100)
    check_in: date
    check_out: date
    guests: int = Field(ge=1, le=12)
    idempotency_key: str = Field(min_length=8, max_length=128)
    guest_confirmed: bool

    @model_validator(mode="after")
    def validate_booking_intent(self) -> "BookingCommand":
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        if not self.guest_confirmed:
            raise ValueError("guest confirmation is required before booking")
        return self


class BookingResult(BaseModel):
    status: Literal["confirmed", "pending", "failed", "unknown"]
    booking_reference: str | None = None
    authoritative: bool = False
    error_code: str | None = None

    @model_validator(mode="after")
    def validate_confirmation(self) -> "BookingResult":
        if self.status == "confirmed":
            if not self.authoritative or not self.booking_reference:
                raise ValueError(
                    "confirmed status requires an authoritative result and booking reference"
                )
        return self


class PropertyManagementPort(Protocol):
    """Internal adapter contract. External endpoint/schema mapping remains unknown."""

    async def get_property(self, property_id: str) -> PropertyRecord | None: ...

    async def check_availability(self, query: StayQuery) -> AvailabilityResult: ...

    async def create_booking(self, command: BookingCommand) -> BookingResult: ...
