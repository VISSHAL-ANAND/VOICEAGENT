"""In-memory booking simulation. This module never creates real reservations."""

from datetime import date
from threading import Lock
from uuid import uuid4

from fastapi import HTTPException

from app.catalog import get_property

_CAPACITY = {
    "demo-coimbatore-001": 4,
    "demo-mysuru-001": 4,
    "demo-madurai-001": 2,
}
_requests: dict[str, tuple[dict, dict]] = {}
_requests_lock = Lock()


def check_demo_availability(
    property_id: str,
    check_in: date,
    check_out: date,
    guests: int,
    room_type_id: str | None = None,
) -> dict:
    """Return demo-only capacity guidance, never live room availability."""
    property_record = get_property(property_id)
    if property_record is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if check_out <= check_in:
        raise HTTPException(status_code=422, detail="Check-out must be after check-in")
    if guests < 1 or guests > 12:
        raise HTTPException(status_code=422, detail="Guests must be between 1 and 12")

    base = {
        "property_id": property_id,
        "check_in": check_in.isoformat(),
        "check_out": check_out.isoformat(),
        "guests": guests,
        "room_type_id": None,
        "room_type_name": None,
        "room_max_guests": None,
        "demo_only": True,
    }

    if room_type_id is not None:
        room = next(
            (
                item
                for item in property_record["room_types"]
                if item["room_type_id"] == room_type_id
            ),
            None,
        )
        if room is None:
            raise HTTPException(
                status_code=404,
                detail="Room type not found for this property",
            )

        suitable = guests <= room["max_guests"]
        return {
            **base,
            "room_type_id": room["room_type_id"],
            "room_type_name": room["name"],
            "room_max_guests": room["max_guests"],
            "status": (
                "simulated_room_capacity_suitable"
                if suitable
                else "simulated_room_capacity_exceeded"
            ),
            "notice": (
                "SIMULATION ONLY — this checks fictional room capacity only. "
                "It does not check dates, inventory, pricing, or real availability."
            ),
        }

    available = guests <= _CAPACITY[property_id]
    return {
        **base,
        "status": "simulated_available" if available else "simulated_unavailable",
        "notice": (
            "SIMULATION ONLY — this is a fictional property-level capacity rule, "
            "not live inventory or a real availability check."
        ),
    }


def create_demo_booking_request(payload: dict) -> dict:
    """Create an idempotent demo request, never a real or confirmed reservation."""
    # Protect lookup, validation, and insertion as one in-process operation.
    # This is not durable or cross-process idempotency.
    with _requests_lock:
        key = payload["idempotency_key"]
        normalized = dict(payload)
        normalized["check_in"] = payload["check_in"].isoformat()
        normalized["check_out"] = payload["check_out"].isoformat()
        normalized.setdefault("room_type_id", None)

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
            room_type_id=normalized["room_type_id"],
        )
        request_id = "demo-request-" + uuid4().hex[:12]
        capacity_suitable_statuses = {
            "simulated_available",
            "simulated_room_capacity_suitable",
        }
        if availability["status"] in capacity_suitable_statuses:
            message = "Simulation recorded only. No room has been reserved."
        else:
            message = (
                "Simulation indicates the selected room's capacity is insufficient. "
                "No room has been reserved."
                if normalized["room_type_id"] is not None
                else "Simulation indicates capacity is insufficient. No room has been reserved."
            )

        response = {
            "request_id": request_id,
            "status": "simulated_not_reserved",
            "capacity_status": availability["status"],
            "property_id": normalized["property_id"],
            "check_in": normalized["check_in"],
            "check_out": normalized["check_out"],
            "guests": normalized["guests"],
            "room_type_id": availability["room_type_id"],
            "room_type_name": availability["room_type_name"],
            "demo_only": True,
            "message": message,
        }
        _requests[key] = (normalized, response)
        return dict(response)
