# Changelog

Changes are recorded after they are actually made and verified.

## 2026-10-27
- Added `AGENTS.md` with project-wide engineering, security, testing, booking, voice, Git, documentation, and production rules.
- Added `SOUL.md` defining the receptionist's identity, communication style, truthfulness, booking boundaries, escalation, privacy, and failure behavior.
- Added `README.md` and project documentation for scope, architecture, decisions, security, testing, state, tasks, and handoffs.
- Verified the original eleven Markdown files in the GitHub recursive tree before adding `SOUL.md`; final verification of the complete twelve-file set is pending.
- No application code or external integration is claimed as implemented.

## 2026-10-27 — Backend scaffold
- Added typed response schemas and synthetic property fixtures for local-only development.
- Added FastAPI health, property-list, and property-detail endpoints.
- Added meaningful API tests and a GitHub Actions pytest workflow. The workflow is committed, but no run has been observed yet.
- No real booking or voice/telephony behavior is implemented.

- Added deterministic demo-capacity checking and an idempotent in-memory booking-request simulation. Responses are always `simulated_not_reserved`; no real booking is made.
- Added tests for simulation-only availability, non-reservation, idempotency, conflicting key reuse, capacity failure, and invalid date order.
- GitHub Actions run #10 completed successfully on the booking-simulation test commit; pytest passed.

- Expanded endpoint tests for property detail success/404, unknown-property availability, reversed availability dates, and invalid guest counts.
- GitHub Actions run #19 passed all 16 pytest tests on the latest application/test commit.

- Added a manager-handoff simulation for answered, busy, no-answer, and failure outcomes. Every response clearly states that no real call was transferred.
- Added handoff tests and confirmed GitHub Actions run #29 passed all 22 tests. CI currently reports one upstream Starlette/httpx TestClient deprecation warning.

- Added validated configuration that accepts only local-mock mode and checks log-level values; wired it into the app.
- Added configuration tests. GitHub Actions run #39 passed all 26 tests. A Starlette/httpx TestClient deprecation warning remains.
