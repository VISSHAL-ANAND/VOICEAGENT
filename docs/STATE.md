# Current State

## Verified checkpoint — 2026-10-27
- Repository: `VISSHAL-ANAND/VOICEAGENT`; branch: `main`.
- FastAPI app: `app/main.py`; typed schemas: `app/schemas.py`; synthetic property catalog: `app/catalog.py`.
- Endpoints implemented:
  - `GET /healthz`
  - `GET /api/v1/properties` with optional city filter
  - `GET /api/v1/properties/{property_id}`
  - `GET /api/v1/demo/availability` — deterministic synthetic capacity only
  - `POST /api/v1/demo/booking-requests` — idempotent in-memory simulation only
  - `POST /api/v1/demo/manager-handoff` — simulated answered/busy/no-answer/failure outcomes only
- Demo booking requests always return `simulated_not_reserved`; no real room is held, booked, or confirmed.
- Automated tests cover health, property listing/filtering/detail/404, demo availability, explicit non-reservation, idempotency, conflicting idempotency-key reuse, capacity failure, invalid date order, unknown-property availability, guest/date validation, retry after a rejected unknown-property request, booking-result invariants, and manager handoff outcomes.
- GitHub Actions workflow `.github/workflows/tests.yml` is active. GitHub Actions run #107 for commit `7f29bfd41c61cf793f625794a4c6932ac24e30e0` completed successfully: 36 tests passed, with one Starlette/httpx deprecation warning. GitHub Actions run #118 on commit `dbed4d974af3700541de4755b58826fb31e19621` passed all 38 tests, including the two additional idempotency regressions. One upstream deprecation warning remains in Starlette's TestClient integration with httpx.
- This is still a local prototype. No real property API, live availability, actual booking, voice integration, phone number, manager transfer, or deployment is implemented or verified.

## Confirmed requirements
Python + FastAPI; Tamil, Hindi, English, Kannada, Telugu; inbound virtual number; authoritative property API for availability and confirmed bookings; manager transfer when supported; ₹0 local/mock development until explicit approval for paid services.

## Blockers
- External API schema, authentication, availability semantics, and booking/idempotency behavior are unknown.
- Preliminary official-source research is recorded in `docs/VOICE_PROVIDER_RESEARCH.md`: Exotel AgentStream (India telephony/media transport), Nia Voice (realtime multilingual speech), Vakyam (TTS-only), and Twilio (pricing comparison). Exact eligibility, current costs, live transfer, quality, and production integration remain unverified; no provider selected.
- Recording, transcription, retention, and production compliance decisions remain open.
- The demo request store is in memory and resets on process restart; it is not production persistence.
- `app/config.py` validates environment configuration, loads `.env` when present, and refuses non-local modes until live integrations exist.
- `app/contracts.py` now defines provider-neutral internal property/availability/booking contracts and a `PropertyManagementPort` protocol. Booking commands require guest confirmation; confirmed results require an authoritative flag and booking reference.
- Added contract-validation tests. GitHub Actions run #59 on commit `1d737cc29de03d1326e0218fbcf94ef1f9718cbe` passed all 31 tests.
- Manager handoff endpoint is only a simulation; no telephony provider is configured and no real call can be transferred.

## Conversation audit cadence
Update affected Markdown after each project work unit. On the fourth user prompt in a cycle, audit every Markdown file against repository evidence, correct discrepancies, and verify the final tree. Full audit completed on 2026-10-27 for all 12 Markdown files: `AGENTS.md`, `README.md`, `SOUL.md`, `docs/PROJECT.md`, `docs/ARCHITECTURE.md`, `docs/STATE.md`, `docs/TASKS.md`, `docs/DECISIONS.md`, `docs/SECURITY.md`, `docs/TESTING.md`, `docs/CHANGELOG.md`, and `docs/INTERACTION_LOG.md`. Corrected stale architecture/testing/CI status. Cadence reset to 0/4 after this audit; cross-session counting may be imperfect.

## Latest work in progress
- Added a process-local lock around the demo idempotency check/insert and a concurrency test issuing 40 same-key requests across 12 threads. The current work adds regressions proving rejected unknown-property and invalid-guest requests do not poison a later valid retry, conflicting key reuse does not mutate the original result, and a `confirmed` result requires an authoritative booking reference. GitHub Actions run #118 passed all 38 tests.
- This does not solve durability or multi-process idempotency; production correctness requires support from the authoritative booking API/database.

## Next action
Verify CI for the two newest idempotency regression tests, then continue with safe failure/retry tests. Preliminary provider research is documented; next research step is to obtain concrete answers from Exotel about sandbox access, inbound-number eligibility, transfer support, and cost before any signup. Price-change behavior and true uncertain-outcome recovery remain blocked on the authoritative quote/booking API contract. Ask the user before any consequential provider, privacy, budget, or architecture choice.
