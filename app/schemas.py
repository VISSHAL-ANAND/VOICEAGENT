from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "voiceagent-api"
    mode: str = "local-mock"


class RoomTypeSummary(BaseModel):
    room_type_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=120)
    max_guests: int = Field(ge=1, le=12)
    amenities: list[str]
    demo_price_per_night_inr: int = Field(ge=0)
    demo_only: Literal[True] = True


class PropertySummary(BaseModel):
    property_id: str
    name: str
    city: str
    supported_languages: list[str]
    amenities: list[str]
    room_types: list[RoomTypeSummary]
    demo_only: bool = True


class PropertyListResponse(BaseModel):
    items: list[PropertySummary]
    total: int
    demo_only: bool = True


class AvailabilityResponse(BaseModel):
    property_id: str
    check_in: date
    check_out: date
    guests: int
    status: str
    room_type_id: str | None = None
    room_type_name: str | None = None
    room_max_guests: int | None = None
    demo_only: Literal[True] = True
    notice: str


class BookingSimulationRequest(BaseModel):
    property_id: str = Field(min_length=1, max_length=100)
    check_in: date
    check_out: date
    guests: int = Field(ge=1, le=12)
    room_type_id: str | None = Field(default=None, min_length=1, max_length=100)
    idempotency_key: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def validate_date_order(self):
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self


class BookingSimulationResponse(BaseModel):
    request_id: str
    status: str
    property_id: str
    check_in: date
    check_out: date
    guests: int
    room_type_id: str | None = None
    room_type_name: str | None = None
    demo_only: bool = True
    message: str


class ManagerHandoffSimulationRequest(BaseModel):
    simulated_outcome: Literal["answered", "busy", "no_answer", "failed"]


class ManagerHandoffSimulationResponse(BaseModel):
    status: str
    demo_only: bool = True
    real_transfer: bool = False
    message: str
