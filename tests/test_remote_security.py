from fastapi.testclient import TestClient

import app.main as main_module
from app.config import Settings


def remote_settings(token: str = "test-token-that-is-at-least-32-characters-long") -> Settings:
    return Settings.from_env({
        "VOICEAGENT_EXPOSURE": "remote",
        "VOICEAGENT_API_TOKEN": token,
    })


def test_remote_api_requires_bearer_token(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "settings", remote_settings())
    client = TestClient(main_module.app)

    response = client.get("/api/v1/properties")

    assert response.status_code == 401
    assert response.json() == {"detail": "Valid bearer token required"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_remote_api_rejects_wrong_bearer_token(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "settings", remote_settings())
    client = TestClient(main_module.app)

    response = client.get(
        "/api/v1/properties",
        headers={"Authorization": "Bearer wrong-token-that-is-long-enough-but-wrong"},
    )

    assert response.status_code == 401


def test_remote_api_accepts_correct_bearer_token(monkeypatch) -> None:
    token = "test-token-that-is-at-least-32-characters-long"
    monkeypatch.setattr(main_module, "settings", remote_settings(token))
    client = TestClient(main_module.app)

    response = client.get(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["demo_only"] is True


def test_remote_health_check_remains_available_without_token(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "settings", remote_settings())
    client = TestClient(main_module.app)

    response = client.get("/healthz")

    assert response.status_code == 200


def test_local_exposure_keeps_existing_local_demo_access(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "settings", Settings.from_env({}))
    client = TestClient(main_module.app)

    response = client.get("/api/v1/properties")

    assert response.status_code == 200



def test_request_body_larger_than_limit_is_rejected(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "settings", Settings.from_env({}))
    client = TestClient(main_module.app)

    response = client.post(
        "/api/v1/demo/booking-requests",
        content=b"x" * (65_536 + 1),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 413
    assert response.json() == {"detail": "Request body too large"}


def test_request_body_at_limit_reaches_normal_validation(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "settings", Settings.from_env({}))
    client = TestClient(main_module.app)

    response = client.post(
        "/api/v1/demo/booking-requests",
        content=b"x" * 65_536,
        headers={"Content-Type": "application/json"},
    )

    # The body is within the size cap, so FastAPI's JSON validation handles it.
    assert response.status_code == 422
