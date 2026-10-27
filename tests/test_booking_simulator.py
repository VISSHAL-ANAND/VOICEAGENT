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
