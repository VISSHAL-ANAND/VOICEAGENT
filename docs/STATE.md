# Current State

## Verified checkpoint — 2026-10-28
- Repository: `VISSHAL-ANAND/VOICEAGENT`; branch: `main`.
- FastAPI app: `app/main.py`; typed schemas: `app/schemas.py`; synthetic property catalog: `app/catalog.py`.
- Endpoints implemented:
  - `GET /healthz`
  - `GET /api/v1/properties` with optional city filter; responses include fictional room types and demo prices
  - `GET /api/v1/properties/{property_id}` with fictional room type details
  - `GET /api/v1/demo/availability` — deterministic synthetic capacity only
  - `POST /api/v1/demo/booking-requests` — idempotent in-memory simulation only
  - `POST /api/v1/demo/manager-handoff` — simulated answered/busy/no-answer/failure outcomes only
- Demo booking requests always return `simulated_not_reserved`; no real room is held, booked, or confirmed.
- Automated tests cover health, property listing/filtering/detail/404, demo availability, explicit non-reservation, idempotency, conflicting idempotency-key reuse, capacity failure, invalid date order, unknown-property availability, guest/date validation, retry after a rejected unknown-property request, booking-result invariants, and manager handoff outcomes.
- GitHub Actions workflow `.github/workflows/tests.yml` is active. Run #156 on commit `7763dc4fe5ff3b4002f886d312e38adbd33c1521` passed all 49 application tests, including voice-session contract and synthetic room-type coverage. One upstream Starlette/httpx TestClient deprecation warning remains.
- This is still a local prototype. No real property API, live availability, actual booking, voice-provider adapter/audio transport, phone number, manager transfer, or deployment is implemented or verified.

## Confirmed requirements
Python + FastAPI; Tamil, Hindi, English, Kannada, Telugu; inbound virtual number; authoritative property API for availability and confirmed bookings; manager transfer when supported; ₹0 local/mock development until explicit approval for paid services.

## Blockers
- External API schema, authentication, availability semantics, and booking/idempotency behavior are unknown.
- Preliminary official-source research is recorded in `docs/VOICE_PROVIDER_RESEARCH.md`: Exotel AgentStream (India telephony/media transport), Nia Voice (realtime multilingual speech), Vakyam (TTS-only), and Twilio (pricing comparison). Exact eligibility, current costs, live transfer, quality, and production integration remain unverified; no provider selected.
- Recording, transcription, retention, and production compliance decisions remain open.
- The demo request store is in memory and resets on process restart; it is not production persistence.
- `app/config.py` validates environment configuration, loads `.env` when present, and refuses non-local modes until live integrations exist.
- `app/contracts.py` defines provider-neutral internal property/availability/booking contracts and a `PropertyManagementPort` protocol. Booking commands require guest confirmation; confirmed results require an authoritative flag and booking reference.
- `app/voice_contracts.py` defines normalized voice session events and a `VoiceSessionPort` protocol. It avoids prescribing an audio protocol or provider; all 47 tests passed in GitHub Actions run #135.
- Added contract-validation tests. GitHub Actions run #59 on commit `1d737cc29de03d1326e0218fbcf94ef1f9718cbe` passed all 31 tests.
- Manager handoff endpoint is only a simulation; no telephony provider is configured and no real call can be transferred.

## Conversation audit cadence
Update affected Markdown after each project work unit. On the fourth user prompt in a cycle, audit every Markdown file against repository evidence, correct discrepancies, and verify the final tree. Full audit completed on 2026-10-27 for the then-existing 12 Markdown files. A new full audit was completed on 2026-10-28 for all 13 current Markdown files, including `docs/VOICE_PROVIDER_RESEARCH.md`; the recursive tree returned `truncated=false`. This audit reconciled current implementation/test evidence, voice-contract status, and stale test-count/status notes. Cadence reset to 0/4 after this audit; cross-session counting may be imperfect.

## Booking simulation limits
- The process-local lock and regression tests protect only the in-memory demo simulator. Run #118 passed the 38-test suite at that checkpoint; later run #135 passed 47 tests after voice-contract coverage was added.
- This does not solve durability or multi-process idempotency; production correctness requires support from the authoritative booking API/database.
- Room-type fixtures are now implemented: each of the three synthetic properties exposes two typed demo room options with capacity, amenities, and illustrative INR nightly prices. New API tests are committed; GitHub Actions run #156 on commit `7763dc4fe5ff3b4002f886d312e38adbd33c1521` passed all 49 tests. These records are not real inventory, availability, or authoritative quotes.

## Full Markdown audit — 2026-10-28
- Read all 13 Markdown files currently present on `main`: `AGENTS.md`, `README.md`, `SOUL.md`, and the ten files under `docs/` including `VOICE_PROVIDER_RESEARCH.md`.
- Verified the recursive Git tree returned `truncated=false`; the inventory includes `app/voice_contracts.py` and `tests/test_voice_contracts.py`.
- Reconciled README, state, tasks, architecture, testing, changelog, and interaction notes against code and GitHub Actions run #135 (47 tests passed). Flagged room-type modeling as an unmet first-prototype acceptance criterion. No provider, paid service, external API schema, or privacy policy was selected.
- Prompt cadence reset to 0/4.

## Room-type fixture implementation — 2026-10-28
- Added two fictional room options to each of the three demo properties, with ID, name, maximum guest count, amenities, illustrative nightly INR price, and strict `demo_only=True` marking.
- Added a validated `RoomTypeSummary` schema and exposed room options through property list/detail responses.
- GitHub Actions run #156 on commit `7763dc4fe5ff3b4002f886d312e38adbd33c1521` passed all 49 tests. One upstream Starlette/httpx TestClient deprecation warning remains.
- This is fixture data only; no live availability, real quote, or booking capability was added.

## Next action
Continue safe booking failure/retry coverage and consider whether mock availability should accept a room type (without implying live inventory). Room types are not yet linked to the simulated availability endpoint. The voice/session contract exists but is not wired to a real adapter. Preliminary provider research is documented; obtain concrete answers about sandbox access, Indian inbound-number eligibility, transfer support, and cost before any signup. Price-change behavior and true uncertain-outcome recovery remain blocked on the authoritative quote/booking API contract. Ask the user before any consequential provider, privacy, budget, or architecture choice.
