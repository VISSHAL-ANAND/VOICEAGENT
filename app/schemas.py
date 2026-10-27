from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str = 'ok'
    service: str = 'voiceagent-api'
    mode: str = 'local-mock'

class PropertySummary(BaseModel):
    property_id: str
    name: str
    city: str
    supported_languages: list[str]
    amenities: list[str]
    demo_only: bool = True

class PropertyListResponse(BaseModel):
    items: list[PropertySummary]
    total: int
    demo_only: bool = True

from datetime import date
from pydantic import Field, model_validator


class AvailabilityResponse(BaseModel):
    property_id: str
    check_in: date
    check_out: date
    guests: int
    status: str
    demo_only: bool = True
    notice: str


class BookingSimulationRequest(BaseModel):
    property_id: str = Field(min_length=1, max_length=100)
    check_in: date
    check_out: date
    guests: int = Field(ge=1, le=12)
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
    demo_only: bool = True
    message: str
