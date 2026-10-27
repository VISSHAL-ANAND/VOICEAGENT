# VoiceAgent — Multilingual Homestay AI Receptionist

A planned phone-based AI receptionist for a company managing multiple homestays/hotels. The agent is intended to answer guest calls, retrieve verified property information, check availability and prices, create reservations through the existing management application, and transfer callers to a manager when requested.

**Status:** Initial repository setup. No application implementation or integration has been verified yet.

## Product goals
- Voice conversations in Tamil, Hindi, English, Kannada, and Telugu.
- Property search and availability through the existing application's API.
- Confirmed reservations created only by the authoritative booking system.
- Live manager handoff through a compatible telephony provider.
- Auditable outcomes, secure handling of guest data, and honest failure behavior.
- ₹0 initial development using local execution and mocked/synthetic services.

## Planned technology
- Python + FastAPI backend.
- Provider-neutral interfaces for realtime voice AI and telephony.
- Adapter for the property-management API.
- PostgreSQL/Supabase or another justified persistence choice after requirements are reviewed.
- Local mocks and synthetic fixtures before real credentials/services are available.

These are project intentions, not claims that integrations are implemented or free. Real voice-model usage, phone numbers, calling, hosting, and database plans may incur costs. No paid service should be activated without explicit approval.

## Requirements before real integration
Obtain from the other developer:
1. Sanitized example JSON/API response and schema.
2. API endpoint documentation and authentication requirements.
3. Availability freshness and reservation consistency semantics.
4. Create/confirm/cancel booking endpoints, idempotency behavior, and error model.
5. Tenant/property scoping and rate limits.

Do not use a static JSON export as the production source of truth for availability.

## Development
The repository is currently an initial documentation baseline. Setup and test commands will be added after the application scaffold and dependencies are established. Do not infer that the application runs until a runnable implementation and executed test results are recorded.

## Project rules
Read [AGENTS.md](AGENTS.md) before contributing. Current project state and next tasks are in [docs/STATE.md](docs/STATE.md) and [docs/TASKS.md](docs/TASKS.md).

## Documentation
- [Project requirements](docs/PROJECT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Decisions](docs/DECISIONS.md)
- [Security and privacy](docs/SECURITY.md)
- [Testing strategy](docs/TESTING.md)
- [Current state](docs/STATE.md)
- [Prioritized tasks](docs/TASKS.md)
- [Changelog](docs/CHANGELOG.md)
- [Interaction log and handoffs](docs/INTERACTION_LOG.md)
