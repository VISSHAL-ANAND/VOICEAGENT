import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    ("outcome", "expected_status"),
    [
        ("answered", "simulated_connected"),
        ("busy", "simulated_busy"),
        ("no_answer", "simulated_no_answer"),
        ("failed", "simulated_failed"),
    ],
)
def test_manager_handoff_outcomes_are_simulated(
    outcome: str, expected_status: str
) -> None:
    response = client.post(
        "/api/v1/demo/manager-handoff",
        json={"simulated_outcome": outcome},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == expected_status
    assert payload["demo_only"] is True
    assert payload["real_transfer"] is False
    assert "No real call was transferred" in payload["message"]


def test_unknown_handoff_outcome_is_rejected() -> None:
    response = client.post(
        "/api/v1/demo/manager-handoff",
        json={"simulated_outcome": "pretend_transfer"},
    )

    assert response.status_code == 422
