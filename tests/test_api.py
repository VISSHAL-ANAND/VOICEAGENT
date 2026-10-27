from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_reports_local_mock_mode() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "voiceagent-api",
        "mode": "local-mock",
    }


def test_property_list_contains_only_demo_records() -> None:
    response = client.get("/api/v1/properties")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    assert payload["demo_only"] is True
    assert all(item["demo_only"] is True for item in payload["items"])
    assert {item["city"] for item in payload["items"]} == {
        "Coimbatore",
        "Mysuru",
        "Madurai",
    }


def test_every_property_has_typed_demo_room_options() -> None:
    response = client.get("/api/v1/properties")

    assert response.status_code == 200
    properties = response.json()["items"]
    assert len(properties) == 3

    for property_record in properties:
        assert property_record["room_types"]
        assert property_record["demo_only"] is True
        for room in property_record["room_types"]:
            assert room["room_type_id"]
            assert room["name"]
            assert 1 <= room["max_guests"] <= 12
            assert isinstance(room["amenities"], list)
            assert room["demo_price_per_night_inr"] >= 0
            assert room["demo_only"] is True


def test_room_type_prices_are_explicitly_demo_only() -> None:
    response = client.get("/api/v1/properties/demo-coimbatore-001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["demo_only"] is True
    assert all(room["demo_only"] is True for room in payload["room_types"])
    assert {room["name"] for room in payload["room_types"]} == {
        "Standard Room",
        "Family Room",
    }
    # A demo price is sample data, not a quote or an availability guarantee.
    assert all("demo_price_per_night_inr" in room for room in payload["room_types"])


def test_property_list_filters_city_case_insensitively() -> None:
    response = client.get("/api/v1/properties", params={"city": "cOiMbAtOrE"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["city"] == "Coimbatore"


def test_unknown_property_returns_404() -> None:
    response = client.get("/api/v1/properties/not-real")

    assert response.status_code == 404
    assert response.json() == {"detail": "Property not found"}


def test_blank_city_is_rejected() -> None:
    response = client.get("/api/v1/properties", params={"city": ""})

    assert response.status_code == 422


def test_property_detail_returns_demo_record() -> None:
    response = client.get("/api/v1/properties/demo-coimbatore-001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["property_id"] == "demo-coimbatore-001"
    assert payload["demo_only"] is True
    assert len(payload["room_types"]) == 2


def test_property_detail_unknown_id_returns_404() -> None:
    response = client.get("/api/v1/properties/unknown-demo-id")

    assert response.status_code == 404
    assert response.json() == {"detail": "Property not found"}


def test_availability_response_rejects_partial_room_metadata() -> None:
    import pytest
    from pydantic import ValidationError

    from app.schemas import AvailabilityResponse

    with pytest.raises(ValidationError, match="must be provided together"):
        AvailabilityResponse(
            property_id="demo-coimbatore-001",
            check_in="2026-11-10",
            check_out="2026-11-12",
            guests=2,
            status="simulated_room_capacity_suitable",
            room_type_id="demo-coimbatore-standard",
            demo_only=True,
            notice="SIMULATION ONLY",
        )


def test_availability_response_rejects_room_status_without_room_metadata() -> None:
    import pytest
    from pydantic import ValidationError

    from app.schemas import AvailabilityResponse

    with pytest.raises(ValidationError, match="requires room metadata"):
        AvailabilityResponse(
            property_id="demo-coimbatore-001",
            check_in="2026-11-10",
            check_out="2026-11-12",
            guests=2,
            status="simulated_room_capacity_suitable",
            demo_only=True,
            notice="SIMULATION ONLY",
        )
