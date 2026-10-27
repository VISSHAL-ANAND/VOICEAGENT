# Architecture Decision Record

## D-001 — Python + FastAPI backend
- **Status:** Accepted
- **Context:** User explicitly selected option A.
- **Decision:** Use Python with FastAPI for backend development.
- **Consequences:** Use typed request/response models, clear modules, async I/O where appropriate, and automated tests.

## D-002 — ₹0 local-first prototype
- **Status:** Accepted
- **Context:** Initial development/testing budget is zero; client may fund production.
- **Decision:** Start with local execution, synthetic fixtures, and mocked external services. Do not activate paid services without approval.
- **Consequences:** Real telephony and paid realtime AI may remain untested until funding/credits are available. Document the difference between simulation and real integration.

## D-003 — Existing application is the booking source of truth
- **Status:** Accepted in principle; API contract pending
- **Context:** Another developer owns the stay-management application and expects to provide an API plus JSON data.
- **Decision:** Retrieve current availability/pricing and create reservations through the existing application where its API supports those operations. Do not maintain a competing source of truth.
- **Consequences:** Integration is blocked until schema, authentication, and booking semantics are documented.

## D-004 — Multilingual voice scope
- **Status:** Accepted requirement; provider capability unverified
- **Decision:** Target Tamil, Hindi, English, Kannada, and Telugu.
- **Consequences:** Evaluate each language independently; do not promise equal quality before tests.

## D-005 — Manager handoff is a core requirement
- **Status:** Accepted requirement; telephony provider pending
- **Decision:** A guest request to speak with the manager should transfer the active call where supported, with honest fallbacks.
- **Consequences:** Provider selection must verify inbound number and transfer capabilities in India.

## Open decisions
- Voice model/provider and telephony provider.
- Persistence choice for local prototype and production.
- Exact property API contract, idempotency, and concurrency semantics.
- Call recording/transcription policy and retention.
- Hosting choice, availability target, latency target, and approved production budget.
