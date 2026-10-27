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


def test_property_detail_unknown_id_returns_404() -> None:
    response = client.get("/api/v1/properties/unknown-demo-id")

    assert response.status_code == 404
    assert response.json() == {"detail": "Property not found"}
