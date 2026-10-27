"""Simulation-only manager handoff outcomes; no telephony is performed."""

from typing import Literal

HandoffOutcome = Literal["answered", "busy", "no_answer", "failed"]

_OUTCOMES = {
    "answered": ("simulated_connected", "Simulation only: a manager would answer."),
    "busy": ("simulated_busy", "Simulation only: the manager is busy."),
    "no_answer": ("simulated_no_answer", "Simulation only: the manager did not answer."),
    "failed": ("simulated_failed", "Simulation only: the transfer attempt failed."),
}


def simulate_manager_handoff(outcome: HandoffOutcome) -> dict:
    status, message = _OUTCOMES[outcome]
    return {
        "status": status,
        "demo_only": True,
        "real_transfer": False,
        "message": message + " No real call was transferred.",
    }
