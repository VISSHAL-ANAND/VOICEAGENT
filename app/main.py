"""Local-first FastAPI scaffold for VoiceAgent."""

from datetime import date
import logging

from fastapi import FastAPI, HTTPException, Query

from app.booking_simulator import check_demo_availability, create_demo_booking_request
from app.config import settings
from app.catalog import get_property, list_properties
from app.handoff_simulator import simulate_manager_handoff
from app.schemas import (
    AvailabilityResponse,
    BookingSimulationRequest,
    BookingSimulationResponse,
    HealthResponse,
    ManagerHandoffSimulationRequest,
    ManagerHandoffSimulationResponse,
    PropertyListResponse,
    PropertySummary,
)

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(
    title="VoiceAgent API",
    version="0.2.0",
    description="Local prototype. Property data and booking flows are simulations only.",
)

@app.get("/healthz", response_model=HealthResponse, tags=["operations"])
def health_check() -> HealthResponse:
    return HealthResponse(mode=settings.mode)

@app.get("/api/v1/properties", response_model=PropertyListResponse, tags=["properties"])
def properties(city: str | None = Query(default=None, min_length=1, max_length=100)) -> PropertyListResponse:
    items = [PropertySummary(**item) for item in list_properties(city)]
    return PropertyListResponse(items=items, total=len(items))

@app.get("/api/v1/properties/{property_id}", response_model=PropertySummary, tags=["properties"])
def property_detail(property_id: str) -> PropertySummary:
    item = get_property(property_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertySummary(**item)

@app.get("/api/v1/demo/availability", response_model=AvailabilityResponse, tags=["demo booking"])
def demo_availability(
    property_id: str,
    check_in: date,
    check_out: date,
    guests: int = Query(ge=1, le=12),
) -> AvailabilityResponse:
    """Return deterministic demo capacity, never live room availability."""
    return AvailabilityResponse(**check_demo_availability(property_id, check_in, check_out, guests))

@app.post("/api/v1/demo/booking-requests", response_model=BookingSimulationResponse, tags=["demo booking"])
def demo_booking_request(payload: BookingSimulationRequest) -> BookingSimulationResponse:
    """Record a local simulation request; never reserve or confirm a real room."""
    result = create_demo_booking_request(payload.model_dump())
    return BookingSimulationResponse(**result)


@app.post("/api/v1/demo/manager-handoff", response_model=ManagerHandoffSimulationResponse, tags=["demo handoff"])
def demo_manager_handoff(payload: ManagerHandoffSimulationRequest) -> ManagerHandoffSimulationResponse:
    """Simulate manager handoff outcomes; never transfers an actual call."""
    return ManagerHandoffSimulationResponse(
        **simulate_manager_handoff(payload.simulated_outcome)
    )
