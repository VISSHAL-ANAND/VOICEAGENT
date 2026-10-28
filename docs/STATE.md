# Current State

## Verified checkpoint — 2026-10-28
- Repository: `VISSHAL-ANAND/VOICEAGENT`; branch: `main`.
- FastAPI app: `app/main.py`; typed schemas: `app/schemas.py`; synthetic property catalog: `app/catalog.py`.
- Endpoints implemented:
  - `GET /healthz`
  - `GET /api/v1/properties` with optional city filter; responses include fictional room types and demo prices
  - `GET /api/v1/properties/{property_id}` with fictional room type details
  - `GET /api/v1/demo/availability` — deterministic synthetic property-level capacity; optional `room_type_id` checks the selected fictional room's maximum guest count only
  - `POST /api/v1/demo/booking-requests` — idempotent in-memory simulation only; optional room selection is validated against property and room capacity, but never reserves a room
  - `POST /api/v1/demo/manager-handoff` — simulated answered/busy/no-answer/failure outcomes only
- Demo booking requests always return `simulated_not_reserved`; no real room is held, booked, or confirmed.
- Automated tests cover health, property listing/filtering/detail/404, demo availability, explicit non-reservation, idempotency, conflicting idempotency-key reuse, capacity failure, invalid date order, unknown-property availability, guest/date validation, retry after a rejected unknown-property request, booking-result invariants, and manager handoff outcomes.
- GitHub Actions workflow `.github/workflows/tests.yml` is active. Run #282 on commit `47653c39183d5f943aea3d502ab8b0ac21c73e52` passed all 87 tests, including selected-room stay-detail consistency, strict request-field validation, remote bearer-token checks, remote configuration validation, request-body size enforcement, rate-limit behavior, and security response headers. One upstream Starlette/httpx TestClient deprecation warning remains.
- This is still a mock-only prototype. No real property API, live availability, actual booking, voice-provider adapter/audio transport, phone number, manager transfer, or deployment is implemented or verified.
- Initial remote-test gate is now implemented in `app/config.py` and `app/main.py`: remote exposure requires a configured 32+ character non-placeholder bearer token; API routes except `/healthz` require it; interactive docs/OpenAPI are disabled when remote mode is active. `app/security.py` also rejects request bodies above 65,536 bytes, and remote mode has an in-process per-IP sliding-window limit (default 60 requests/minute). CI run #282 passed all 87 tests (one upstream deprecation warning). The limiter is process-local and not sufficient by itself to expose the app publicly. Conservative response headers are tested; HSTS is only emitted for HTTPS requests and does not establish host-level TLS.
- Room-specific demo capacity support is committed on `main`: selected room IDs must belong to the property, group size is checked against the room's maximum guest count, and the response distinguishes capacity suitability from real availability. Room-specific capacity, selected-room booking-request, and strict response-schema tests passed in GitHub Actions run #198 (62 tests total; one upstream Starlette/httpx TestClient deprecation warning).

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
Update affected Markdown after each project work unit. On the fourth user prompt in a cycle, audit every Markdown file against repository evidence, correct discrepancies, and verify the final tree. The full audit recorded below was completed after the user approved Render Free remote testing; cadence resets to 0/4. Cross-session counting may be imperfect.

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
Create the Render service from the checked-in Blueprint in the Render Dashboard; it generates and stores the bearer token automatically. Deploy only the Free plan. The connected deployment action did not create a service. After deployment, verify HTTPS, `/healthz`, 401 for missing/wrong tokens, successful authenticated API access, rate-limit responses, and logs before sharing the URL. Do not add a payment method or upgrade without approval. Real API integration remains blocked on the other developer's sanitized schema/authentication contract; production readiness still requires tenant isolation, durable idempotency, privacy policy, and review. The voice/session contract exists but is not wired to a real adapter. Provider research remains preliminary; no voice/telephony provider or paid number is selected. Price-change behavior and uncertain booking outcome recovery remain blocked on the authoritative API contract. Ask before any further consequential provider, privacy, budget, or architecture choice.


## Remote rate limiting — 2026-10-28
- Added a bounded in-memory sliding-window rate limiter that is active only in `VOICEAGENT_EXPOSURE=remote`; default is 60 requests per client IP per minute and can be configured from 1 to 10,000.
- The limiter covers health and API routes, emits HTTP 429 with `Retry-After`, bounds remembered client keys, and intentionally ignores untrusted `X-Forwarded-For` values. Added tests for enforcement, headers, forwarded-header spoofing, and configuration validation.
- GitHub Actions run #271 on commit `c24eb4c011a58a5a2d1e23b36a07c3a5d5c3e286` passed all 85 tests.
- Limitation: limiter state is local to one process and resets on restart; it is not a substitute for distributed/edge rate limiting, HTTPS, monitoring, or deployment review. No host selected and no deployment performed.


## Remote response security headers — 2026-10-28
- Added conservative response headers: content-type sniffing disabled, framing denied, referrer minimized, browser permissions restricted, cross-origin resource policy set to same-origin, and caching disabled. Remote mode adds a restrictive Content Security Policy.
- HSTS is only emitted when the ASGI request scheme is HTTPS; this is not a TLS deployment and does not verify proxy configuration.
- GitHub Actions run #282 on commit `47653c39183d5f943aea3d502ab8b0ac21c73e52` passed all 87 tests, including the new response-header assertions.


## Fourth-prompt full Markdown audit — 2026-10-28 (remote-host approval)
- Read all 13 Markdown files on `main` and checked the repository's recursive tree; `truncated=false`.
- Reconciled stale test-status references to the latest verified application run #282: 87 tests passed with one upstream Starlette/httpx deprecation warning.
- Corrected duplicate/stale remote-security descriptions in `docs/ARCHITECTURE.md`, stale testing status, and host-selection state.
- User approved Render Free for a mock-only remote test. Added a `render.yaml` Blueprint with Free plan, Singapore region, health check, disabled auto-deploy, and a Render-generated 256-bit bearer token.
- Direct service creation was blocked by the connected action's safety checks; no service was created, no public URL exists, and no paid resource was activated.
- Cadence reset to 0/4. Next step is dashboard Blueprint creation, deployment, private token retrieval only if needed, and post-deploy security verification.


## Fourth-prompt full Markdown audit — 2026-10-28 (remote-host approval)
- Read all 13 Markdown files on `main` and checked the repository's recursive tree; `truncated=false`.
- Reconciled stale test-status references to the latest verified application run #282: 87 tests passed with one upstream Starlette/httpx deprecation warning.
- Corrected duplicate/stale remote-security descriptions in `docs/ARCHITECTURE.md`, stale testing status, and host-selection state.
- User approved Render Free for a mock-only remote test. Added a `render.yaml` Blueprint with Free plan, Singapore region, health check, disabled auto-deploy, and a secret prompt for the bearer token.
- Direct service creation was blocked by the connected action's safety checks; no service was created, no public URL exists, and no paid resource was activated.
- Cadence reset to 0/4. Next step is dashboard Blueprint creation, secret entry, deployment, and post-deploy security verification.


## Render deployment verification — 2026-10-28
- Render account confirms service `voiceagent-remote-demo` is deployed and `LIVE` at `https://voiceagent-remote-demo.onrender.com`, Free plan, Singapore, branch `main`. Render reports build and deploy succeeded; logs show FastAPI startup completed.
- Render's service logs show unauthenticated `GET /` returned `401 Unauthorized`, consistent with the remote bearer-token gate. The public `/healthz` response and authenticated API behavior are not yet independently verified; the web fetch tool could not access the service URL.
- Important dashboard mismatch: the created service has an empty health-check path and automatic deploys enabled. Intended settings are health check `/healthz` and automatic deploys OFF. The checked-in `render.yaml` has those intended values, but the manually created service did not inherit them.
- Next: user must change health check path to `/healthz` and disable auto-deploy in Render Dashboard. Then verify `/healthz`, missing-token 401, valid-token API access without sharing the token, and logs. Keep the service Free and mock-only. No real guest data, bookings, telephony, or manager transfer.
