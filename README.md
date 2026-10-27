# VoiceAgent — Multilingual Homestay AI Receptionist

VoiceAgent is being built as a phone-based AI receptionist for a company managing multiple homestays/hotels. The target product will answer guest calls, use verified property information, check availability and prices, create reservations through the existing management application, and transfer callers to a manager when requested.

**Current status:** Local prototype with passing GitHub Actions tests. FastAPI health/property endpoints and simulation-only availability/booking-request endpoints are committed. The demo booking flow never reserves or confirms a real room. Real property API, live availability/booking, voice, telephony, live manager transfer, and deployment are not implemented. Do not use this prototype for real guest calls.

## Product goals
- Voice conversations in Tamil, Hindi, English, Kannada, and Telugu.
- Property search and availability through the existing application's API.
- Confirmed reservations created only by the authoritative booking system.
- Live manager handoff through a compatible telephony provider.
- Auditable outcomes, secure handling of guest data, and honest failure behavior.
- ₹0 initial development using local execution and mocked/synthetic services.

## Technology and cost
- Python + FastAPI backend with validated local-only configuration.
- Provider-neutral interfaces for voice, telephony, and the property-management API.
- Synthetic fixtures and mocked external services before real credentials are available.
- GitHub Actions run #39 passed all 26 pytest tests. One upstream Starlette/httpx TestClient deprecation warning remains.

No paid service should be activated without explicit approval. Voice-model usage, phone numbers, calling, hosting, and database plans may incur costs.

## Local development
Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/healthz` for the health response and `http://127.0.0.1:8000/docs` for the FastAPI API explorer. The automated test workflow has passed in GitHub Actions; the assistant has not deployed this application to a public server.

## Local demo booking endpoints
- `GET /api/v1/demo/availability?property_id=demo-coimbatore-001&check_in=2026-11-10&check_out=2026-11-12&guests=2` returns fictional capacity data.
- `POST /api/v1/demo/booking-requests` accepts property/date/guest details and an idempotency key. It returns `simulated_not_reserved` even when the fictional capacity rule says available.
- `POST /api/v1/demo/manager-handoff` simulates answered, busy, no-answer, and failed handoff outcomes. It always sets `real_transfer: false`.
- All demo availability and booking responses are explicitly marked as simulation-only. These endpoints must never be presented to guests as real availability or a confirmed reservation.

## Requirements before real integration
Obtain from the other developer:
1. Sanitized example JSON/API response and schema.
2. API endpoint documentation and authentication requirements.
3. Availability freshness and reservation consistency semantics.
4. Create/confirm/cancel booking endpoints, idempotency behavior, and error model.
5. Tenant/property scoping and rate limits.

Do not use a static JSON export as the production source of truth for availability. Never claim a booking is confirmed unless the authoritative API verifies it.

## Project rules and documentation
Read [AGENTS.md](AGENTS.md) for engineering rules and [SOUL.md](SOUL.md) for the receptionist's identity and behavior. Current state and next tasks are in [docs/STATE.md](docs/STATE.md) and [docs/TASKS.md](docs/TASKS.md).

- [Project requirements](docs/PROJECT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Decisions](docs/DECISIONS.md)
- [Security and privacy](docs/SECURITY.md)
- [Testing strategy](docs/TESTING.md)
- [Current state](docs/STATE.md)
- [Prioritized tasks](docs/TASKS.md)
- [Changelog](docs/CHANGELOG.md)
- [Interaction log and handoffs](docs/INTERACTION_LOG.md)
