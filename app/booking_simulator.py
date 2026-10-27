"""In-memory booking simulation. This module never creates real reservations."""

from datetime import date
from uuid import uuid4

from fastapi import HTTPException

from app.catalog import get_property

_CAPACITY = {
    "demo-coimbatore-001": 4,
    "demo-mysuru-001": 4,
    "demo-madurai-001": 2,
}
_requests: dict[str, tuple[dict, dict]] = {}


def check_demo_availability(
    property_id: str, check_in: date, check_out: date, guests: int
) -> dict:
    if get_property(property_id) is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if check_out <= check_in:
        raise HTTPException(status_code=422, detail="Check-out must be after check-in")
    if guests < 1 or guests > 12:
        raise HTTPException(status_code=422, detail="Guests must be between 1 and 12")

    capacity = _CAPACITY[property_id]
    available = guests <= capacity
    return {
        "property_id": property_id,
        "check_in": check_in.isoformat(),
        "check_out": check_out.isoformat(),
        "guests": guests,
        "status": "simulated_available" if available else "simulated_unavailable",
        "demo_only": True,
        "notice": "SIMULATION ONLY — this is not live inventory or a real availability check.",
    }


def create_demo_booking_request(payload: dict) -> dict:
    """Create an idempotent demo request, never a real or confirmed reservation."""
    key = payload["idempotency_key"]
    normalized = dict(payload)
    normalized["check_in"] = payload["check_in"].isoformat()
    normalized["check_out"] = payload["check_out"].isoformat()

    existing = _requests.get(key)
    if existing:
        previous_payload, previous_response = existing
        if previous_payload != normalized:
            raise HTTPException(
                status_code=409,
                detail="Idempotency key was already used with different booking details",
            )
        return dict(previous_response)

    availability = check_demo_availability(
        normalized["property_id"],
        payload["check_in"],
        payload["check_out"],
        payload["guests"],
    )
    request_id = "demo-request-" + uuid4().hex[:12]
    if availability["status"] == "simulated_available":
        message = "Simulation recorded only. No room has been reserved."
    else:
        message = "Simulation indicates capacity is insufficient. No room has been reserved."

    response = {
        "request_id": request_id,
        "status": "simulated_not_reserved",
        "property_id": normalized["property_id"],
        "check_in": normalized["check_in"],
        "check_out": normalized["check_out"],
        "guests": normalized["guests"],
        "demo_only": True,
        "message": message,
    }
    _requests[key] = (normalized, response)
    return dict(response)
