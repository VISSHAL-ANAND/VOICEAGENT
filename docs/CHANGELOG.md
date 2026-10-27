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
- Added regression tests for suitable/over-capacity groups, unknown and cross-property room IDs, blank IDs, and backward compatibility. CI verification is pending; no live inventory or booking behavior was introduced.
