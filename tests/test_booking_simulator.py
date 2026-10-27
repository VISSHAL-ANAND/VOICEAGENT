from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def booking_payload(**overrides):
    payload = {
        "property_id": "demo-coimbatore-001",
        "check_in": "2026-11-10",
        "check_out": "2026-11-12",
        "guests": 2,
        "idempotency_key": "test-key-0001",
    }
    payload.update(overrides)
    return payload


def test_demo_availability_is_explicitly_not_live() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "demo-coimbatore-001",
            "check_in": "2026-11-10",
            "check_out": "2026-11-12",
            "guests": 2,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_available"
    assert payload["demo_only"] is True
    assert "not live inventory" in payload["notice"]


def test_demo_booking_never_claims_to_reserve_a_room() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(idempotency_key="test-key-never-reserve"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_not_reserved"
    assert payload["demo_only"] is True
    assert "No room has been reserved" in payload["message"]


def test_same_idempotency_key_returns_same_simulation_request() -> None:
    payload = booking_payload(idempotency_key="test-key-repeat-01")
    first = client.post("/api/v1/demo/booking-requests", json=payload)
    second = client.post("/api/v1/demo/booking-requests", json=payload)

    assert first.status_code == second.status_code == 200
    assert first.json()["request_id"] == second.json()["request_id"]


def test_reusing_idempotency_key_with_different_details_is_rejected() -> None:
    key = "test-key-conflict"
    first = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(idempotency_key=key),
    )
    second = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(idempotency_key=key, guests=3),
    )

    assert first.status_code == 200
    assert second.status_code == 409


def test_demo_capacity_failure_never_reserves_room() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            property_id="demo-madurai-001",
            guests=3,
            idempotency_key="test-key-capacity",
        ),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_not_reserved"
    assert "capacity is insufficient" in payload["message"]
    assert payload["demo_only"] is True


def test_invalid_date_order_is_rejected() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            check_in="2026-11-12",
            check_out="2026-11-10",
            idempotency_key="test-key-bad-date",
        ),
    )

    assert response.status_code == 422


def test_unknown_property_availability_returns_404() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "unknown-demo-id",
            "check_in": "2026-11-10",
            "check_out": "2026-11-12",
            "guests": 2,
        },
    )

    assert response.status_code == 404


def test_demo_availability_rejects_checkout_before_checkin() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "demo-coimbatore-001",
            "check_in": "2026-11-12",
            "check_out": "2026-11-10",
            "guests": 2,
        },
    )

    assert response.status_code == 422


def test_demo_booking_rejects_guest_count_outside_range() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(guests=0, idempotency_key="test-key-bad-guests"),
    )

    assert response.status_code == 422


def test_concurrent_same_idempotency_key_creates_one_simulation_request() -> None:
    from concurrent.futures import ThreadPoolExecutor
    from datetime import date

    from app.booking_simulator import create_demo_booking_request

    payload = {
        "property_id": "demo-coimbatore-001",
        "check_in": date(2026, 11, 10),
        "check_out": date(2026, 11, 12),
        "guests": 2,
        "idempotency_key": "concurrent-same-key-0001",
    }

    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(
            lambda _: create_demo_booking_request(dict(payload)),
            range(40),
        ))

    request_ids = {result["request_id"] for result in results}
    assert len(request_ids) == 1
    assert all(result["status"] == "simulated_not_reserved" for result in results)


def test_booking_request_for_unknown_property_returns_404() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            property_id="not-a-demo-property",
            idempotency_key="unknown-property-key-01",
        ),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Property not found"


def test_booking_request_rejects_short_idempotency_key() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(idempotency_key="short"),
    )

    assert response.status_code == 422


def test_rejected_unknown_property_does_not_poison_idempotency_key() -> None:
    key = "retry-after-404-0001"
    rejected = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            property_id="not-a-demo-property",
            idempotency_key=key,
        ),
    )
    retried = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(idempotency_key=key),
    )

    assert rejected.status_code == 404
    assert retried.status_code == 200
    assert retried.json()["status"] == "simulated_not_reserved"


def test_invalid_request_does_not_poison_idempotency_key() -> None:
    key = "invalid-then-valid-0001"
    rejected = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(guests=0, idempotency_key=key),
    )
    retried = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(idempotency_key=key),
    )

    assert rejected.status_code == 422
    assert retried.status_code == 200
    assert retried.json()["status"] == "simulated_not_reserved"


def test_conflicting_reuse_does_not_change_original_idempotency_result() -> None:
    key = "conflict-preserves-original-01"
    original_payload = booking_payload(idempotency_key=key)
    first = client.post("/api/v1/demo/booking-requests", json=original_payload)
    conflict = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(idempotency_key=key, guests=3),
    )
    replay = client.post("/api/v1/demo/booking-requests", json=original_payload)

    assert first.status_code == 200
    assert conflict.status_code == 409
    assert replay.status_code == 200
    assert replay.json()["request_id"] == first.json()["request_id"]
    assert replay.json()["guests"] == 2


def test_room_specific_capacity_check_returns_selected_room_metadata() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "demo-coimbatore-001",
            "check_in": "2026-11-10",
            "check_out": "2026-11-12",
            "guests": 2,
            "room_type_id": "demo-coimbatore-standard",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_room_capacity_suitable"
    assert payload["room_type_id"] == "demo-coimbatore-standard"
    assert payload["room_type_name"] == "Standard Room"
    assert payload["room_max_guests"] == 2
    assert payload["demo_only"] is True
    assert "does not check dates, inventory, pricing, or real availability" in payload["notice"]


def test_room_specific_capacity_check_flags_guest_count_over_room_limit() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "demo-coimbatore-001",
            "check_in": "2026-11-10",
            "check_out": "2026-11-12",
            "guests": 3,
            "room_type_id": "demo-coimbatore-standard",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_room_capacity_exceeded"
    assert payload["room_max_guests"] == 2
    assert payload["demo_only"] is True
    assert "not live inventory" not in payload["notice"].lower() or "simulation only" in payload["notice"].lower()


def test_room_type_from_another_property_is_not_accepted() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "demo-coimbatore-001",
            "check_in": "2026-11-10",
            "check_out": "2026-11-12",
            "guests": 2,
            "room_type_id": "demo-mysuru-garden",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Room type not found for this property"}


def test_unknown_room_type_is_not_accepted() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "demo-coimbatore-001",
            "check_in": "2026-11-10",
            "check_out": "2026-11-12",
            "guests": 2,
            "room_type_id": "made-up-room-type",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Room type not found for this property"}


def test_room_specific_check_preserves_legacy_property_level_behavior() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "demo-coimbatore-001",
            "check_in": "2026-11-10",
            "check_out": "2026-11-12",
            "guests": 2,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_available"
    assert payload["room_type_id"] is None
    assert payload["room_type_name"] is None
    assert payload["room_max_guests"] is None
    assert payload["demo_only"] is True


def test_blank_room_type_id_is_rejected() -> None:
    response = client.get(
        "/api/v1/demo/availability",
        params={
            "property_id": "demo-coimbatore-001",
            "check_in": "2026-11-10",
            "check_out": "2026-11-12",
            "guests": 2,
            "room_type_id": "",
        },
    )

    assert response.status_code == 422


def test_demo_booking_request_validates_and_echoes_selected_room() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            room_type_id="demo-coimbatore-standard",
            idempotency_key="room-booking-valid-01",
        ),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_not_reserved"
    assert payload["room_type_id"] == "demo-coimbatore-standard"
    assert payload["room_type_name"] == "Standard Room"
    assert payload["demo_only"] is True
    assert "No room has been reserved" in payload["message"]


def test_demo_booking_request_rejects_guest_count_over_selected_room_capacity() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            guests=3,
            room_type_id="demo-coimbatore-standard",
            idempotency_key="room-booking-over-capacity-01",
        ),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_not_reserved"
    assert payload["room_type_id"] == "demo-coimbatore-standard"
    assert "selected room's capacity is insufficient" in payload["message"]
    assert "No room has been reserved" in payload["message"]


def test_invalid_selected_room_does_not_poison_booking_idempotency_key() -> None:
    key = "room-booking-invalid-retry-01"
    rejected = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            room_type_id="demo-mysuru-garden",
            idempotency_key=key,
        ),
    )
    retried = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            room_type_id="demo-coimbatore-standard",
            idempotency_key=key,
        ),
    )

    assert rejected.status_code == 404
    assert retried.status_code == 200
    assert retried.json()["room_type_id"] == "demo-coimbatore-standard"
    assert retried.json()["status"] == "simulated_not_reserved"


def test_reusing_booking_idempotency_key_with_different_room_is_rejected() -> None:
    key = "room-booking-key-conflict-01"
    first = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            room_type_id="demo-coimbatore-standard",
            idempotency_key=key,
        ),
    )
    conflict = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            room_type_id="demo-coimbatore-family",
            idempotency_key=key,
        ),
    )
    replay = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(
            room_type_id="demo-coimbatore-standard",
            idempotency_key=key,
        ),
    )

    assert first.status_code == 200
    assert conflict.status_code == 409
    assert replay.status_code == 200
    assert replay.json()["request_id"] == first.json()["request_id"]
    assert replay.json()["room_type_id"] == "demo-coimbatore-standard"


def test_booking_request_without_room_selection_remains_compatible() -> None:
    response = client.post(
        "/api/v1/demo/booking-requests",
        json=booking_payload(idempotency_key="room-booking-legacy-01"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "simulated_not_reserved"
    assert payload["room_type_id"] is None
    assert payload["room_type_name"] is None
