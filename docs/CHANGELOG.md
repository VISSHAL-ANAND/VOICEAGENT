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

- Added `python-dotenv` support so the app loads a local `.env` file, and documented copying `.env.example` during setup.
- GitHub Actions run #50 passed all 26 tests after the configuration update.

- Added provider-neutral internal property/availability/booking contracts and an adapter protocol; these do not assume the external management API schema.
- Added tests for date validation, explicit guest confirmation, and authoritative booking-confirmation invariants. CI verification is pending.

- Provider-neutral contract tests passed in GitHub Actions run #59: 31 tests passed across the current repository test suite.


## 2026-10-27 — Fourth-prompt documentation audit
- Read all 12 Markdown files from `main` and checked them against the repository tree, application modules, tests, and GitHub Actions evidence.
- Corrected stale architecture/testing status and updated the README, state, and task evidence to latest observed successful CI run #73 (`40749a317b993f6f7ad0dffac563439aacc9b352`): 31 tests passed, one Starlette/httpx deprecation warning.
- Marked documentation inventory and completeness review tasks complete. No provider, schema, hosting, privacy, or paid-service decision was invented.


## 2026-10-27 — Booking simulation concurrency hardening
- Added a process-local lock around idempotency lookup, payload conflict validation, and request insertion.
- Added a regression test for 40 concurrent requests with the same idempotency key across 12 threads.
- GitHub Actions run #82 passed all 32 tests, including the concurrency regression. This is not durable or multi-process idempotency and does not replace authoritative booking-system controls.


- Added tests that unknown-property booking requests return 404 and short idempotency keys return 422. GitHub Actions run #95 passed all 34 tests.


## 2026-10-28 — Booking failure/retry edge cases
- Added a regression test that an unknown-property request returns 404 without poisoning a later valid request using the same idempotency key.
- Added a contract regression test that `status="confirmed"` is rejected when the booking reference is missing, even if `authoritative=True`.
- GitHub Actions run #107 on commit `7f29bfd41c61cf793f625794a4c6932ac24e30e0` passed all 36 tests, including both new edge-case regressions. One Starlette/httpx deprecation warning remains.


## 2026-10-28 — Provider research and booking regression coverage
- Added `docs/VOICE_PROVIDER_RESEARCH.md` with a preliminary comparison based on official public information for Exotel AgentStream, Nia Voice, Vakyam AI, and Twilio. No vendor selected or service activated.
- Added two booking simulation tests for invalid guest-count retry and preservation of the original result after conflicting idempotency-key reuse. GitHub Actions run #118 on commit `dbed4d974af3700541de4755b58826fb31e19621` passed all 38 tests.


## 2026-10-28 — Provider-neutral voice session boundary
- Added `app/voice_contracts.py` with normalized session lifecycle/transcript/error events and a `VoiceSessionPort` protocol.
- Added tests for the five supported language tags, event-kind parsing, unexpected-field rejection, blank transcript rejection, and normalized error codes.
- The boundary deliberately does not define audio codecs, transport framing, vendor behavior, or telephony integration. GitHub Actions verification is pending; no real voice provider or paid service was activated.

- Follow-up verification: GitHub Actions run #135 on commit `36127058bf34388829e3e46b8ba5c8a35cfe4870` passed all 47 tests, including the new voice-session contract tests. One upstream Starlette/httpx deprecation warning remains.


## 2026-10-28 — Synthetic room-type fixture model
- Added two fictional room options for each demo property, with maximum guest capacity, amenities, and sample INR nightly prices.
- Added `RoomTypeSummary` validation and exposed room types through property list/detail endpoints.
- Added API tests for room fixture shape and demo-only labeling. No real inventory, quote, or availability behavior was introduced.

- Verification: GitHub Actions run #156 on commit `7763dc4fe5ff3b4002f886d312e38adbd33c1521` passed all 49 tests. One upstream Starlette/httpx deprecation warning remains.


## 2026-10-28 — Room-specific demo capacity guardrails
- Added optional `room_type_id` to the demo availability endpoint. Selected room IDs are checked against the requested property's own fixture; unknown or cross-property room IDs return 404.
- Added a room-capacity-only result distinct from property-level simulated capacity. The response names the room and maximum guest count, and explicitly says that dates, inventory, prices, and real availability are not checked.
- Added regression tests for suitable/over-capacity groups, unknown and cross-property room IDs, blank IDs, and backward compatibility. GitHub Actions run #179 on commit `d83d9fee53e378112c2c3eb3bc84107dfac8c041` passed all 55 tests (one upstream deprecation warning); no live inventory or booking behavior was introduced.

## 2026-10-28 — Selected-room booking-request guardrails
- Added optional room selection to the demo booking-request schema and response. The simulator validates the selected room against the requested property and its declared capacity, but always returns `simulated_not_reserved`.
- Included room selection in idempotency comparison; invalid room selections are not stored, and a different room under an existing key conflicts with 409.
- Tightened availability response schema validation so room metadata must be complete and consistent with the status. GitHub Actions run #198 on commit `40daa12ba8975b8c575441b3d2775166a8187042` passed all 62 tests (one upstream deprecation warning).

## 2026-10-28 — Stay-detail consistency and strict input validation
- Added a constrained `capacity_status` separate from the invariant `simulated_not_reserved` booking-request status; response includes the property, dates, guest count, and selected room used by the simulation.
- Booking and simulated handoff request schemas now reject unexpected JSON fields and normalize surrounding whitespace before validation. Added regressions for stay-detail consistency, over-capacity status preservation, unexpected fields, and whitespace-only idempotency keys.
- An intermediate CI run exposed that the new response field was not yet wired into the simulator; the simulator was corrected, and GitHub Actions run #216 passed all 66 tests (one upstream deprecation warning).


## 2026-10-28 — Initial remote-test authentication gate
- Added `VOICEAGENT_EXPOSURE=local|remote` configuration. Remote mode requires a non-placeholder API token of at least 32 characters and rejects invalid configuration at startup.
- Added Bearer-token checks to remote API routes (except `/healthz`), disabled interactive docs/OpenAPI routes when remote mode is active, and excluded the token from settings repr.
- Added config and API security tests. GitHub Actions verification is pending; this is not a full internet-exposure approval. HTTPS, rate limits, request-size limits, monitoring, and deployment review remain open.
- Verification/fix: an initial run failed because the placeholder test value was shorter than the minimum-token check; the revised test then revealed the guard did not reject a longer `replace-me...` placeholder. The guard now rejects the placeholder prefix, and GitHub Actions run #243 on commit `f207f1969cc1cfdd969718d8851b842fec8efcd4` passed all 75 tests. One upstream Starlette/httpx deprecation warning remains.


## 2026-10-28 — Request body size cap
- Added ASGI middleware to reject HTTP request bodies over 65,536 bytes with HTTP 413, including bodies delivered in multiple chunks. This is an application-level guard; reverse-proxy/server limits and rate limiting remain necessary.
- Added tests for over-limit and exact-limit bodies. GitHub Actions run #254 on commit `cb53358b0f7075827b6780bb02da9c4be7ef1191` passed all 77 tests (one upstream Starlette/httpx TestClient deprecation warning).


## 2026-10-28 — Remote request rate limiting
- Added a configurable in-memory sliding-window request limit for remote mode (default 60 requests per client IP per minute), with 429 and `Retry-After` responses.
- Added validated `VOICEAGENT_RATE_LIMIT_PER_MINUTE` configuration, bounded client tracking, and tests for enforcement and forwarded-header spoofing.
- GitHub Actions run #271 on commit `c24eb4c011a58a5a2d1e23b36a07c3a5d5c3e286` passed all 85 tests.
- Limitation: in-process limiter only; public deployment still requires trusted edge rate limiting, HTTPS/TLS, monitoring, host restrictions, and review.


## 2026-10-28 — Remote response security headers
- Added conservative security headers to responses, a restrictive CSP in remote mode, and conditional HSTS only when the ASGI request scheme is HTTPS.
- Added regression coverage for expected headers and HTTPS-only HSTS behavior. GitHub Actions run #282 passed all 87 tests.
- These application headers do not configure or prove HTTPS at the host/proxy layer.


## 2026-10-28 — Render Free remote-test blueprint
- User explicitly approved Render Free for a mock-only remote test; no paid plan or production deployment was approved.
- Added `render.yaml` for a Singapore-region Free web service, `/healthz` health check, disabled auto-deploy, remote bearer-token mode, and a Render-generated 256-bit bearer token.
- The connected direct service-creation action was blocked by safety checks. No service or public URL was created; the Blueprint must be created from the Render Dashboard; the token is generated and stored by Render.
- Full Markdown audit completed across all 13 Markdown files; recursive tree returned `truncated=false`. Corrected stale test-count and remote-hosting status. Latest verified application CI remains run #282 (87 passed).


## 2026-10-28 — Render Free remote-test blueprint
- User explicitly approved Render Free for a mock-only remote test; no paid plan or production deployment was approved.
- Added `render.yaml` for a Singapore-region Free web service, `/healthz` health check, disabled auto-deploy, remote bearer-token mode, and a `sync: false` secret prompt.
- The connected direct service-creation action was blocked by safety checks, so the user manually created the service in the Render Dashboard. The actual service settings differ from the Blueprint: health-check path is blank and auto-deploy is enabled.
- Full Markdown audit completed across all 13 Markdown files; recursive tree returned `truncated=false`. Corrected stale test-count and remote-hosting status. Latest verified application CI remains run #282 (87 passed).


## 2026-10-28 — Render Free mock deployment
- User deployed `voiceagent-remote-demo` from `VISSHAL-ANAND/VOICEAGENT` on Render Free in Singapore.
- Render reports build/deploy succeeded and application startup completed. Logs show unauthenticated `GET /` returns 401.
- Follow-up verification found actual service settings differ from intended Blueprint: health-check path is blank and auto-deploy is enabled. Dashboard correction and health/authenticated-route checks remain pending.
