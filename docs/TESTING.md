# Testing and Verification Strategy

## Current status
The local FastAPI prototype and its tests are verified by GitHub Actions. The latest verified application-test run is #156 on commit `7763dc4fe5ff3b4002f886d312e38adbd33c1521`: 49 tests passed with one Starlette/httpx deprecation warning. Real API, voice-provider adapter, telephony, persistence, production concurrency across workers, and production behavior remain unverified. Never report tests as passing unless executed.

## Test layers
1. **Unit tests:** date/occupancy validation, pricing rules, booking state transitions, language/session state, redaction.
2. **Contract tests:** internal models and adapters against documented external API schemas.
3. **Integration tests:** mocked property API, booking API, voice adapter, and telephony adapter.
4. **Workflow tests:** end-to-end booking and manager escalation.
5. **Language evaluation:** representative audio/utterances in Tamil, Hindi, English, Kannada, and Telugu.
6. **Operational/security tests:** timeouts, retries, authentication, authorization, redaction, rate limits, and recovery.

## Mandatory booking scenarios
- Valid booking with authoritative confirmation.
- Invalid date range, past date, ambiguous date, and timezone boundary.
- Capacity exceeded or unavailable property/room.
- Price/tax/fee changes before final confirmation.
- Guest corrects dates or occupancy.
- Guest declines confirmation.
- Concurrent attempts for the last room.
- Duplicate tool call or repeated HTTP request.
- API error before reservation creation.
- Timeout where reservation outcome is unknown.
- Successful result without a valid booking reference.
- Cancellation/modification request outside supported rules.

## Voice and call scenarios
- Each target language individually and language switching.
- Names, locations, dates, phone numbers, and currency amounts.
- Background noise, unclear speech, caller interruption, silence, and repeated clarification.
- Guest asks for a manager.
- Manager answers, is busy, does not answer, or transfer fails.
- Voice provider or telephony connection drops mid-call.
- Guest requests a language not supported by the current session.

## Test data
Use synthetic data only. Never use real guest data or production credentials in automated tests. Mocked success does not prove a real provider integration works.

## Reporting
For each meaningful change, record the exact commands executed, pass/fail outcomes, failures, and environment limitations. Keep performance and language claims tied to measurements.

## Current automated coverage
- Health response and local-mock mode.
- Synthetic property list, demo-only marker, case-insensitive city filter, unknown-property 404, and invalid blank city.
- Demo availability explicitly labels itself as not live inventory.
- Demo booking requests never claim reservation, repeat idempotency keys return the same simulation ID, conflicting payloads with the same key return 409, over-capacity requests remain unreserved, and invalid date order returns 422.
- Regression test: an unknown-property request returns 404 and does not poison a subsequent valid retry using the same idempotency key; passed in run #107.
- GitHub Actions run #107 passed dependency installation and all 36 pytest tests on commit `7f29bfd41c61cf793f625794a4c6932ac24e30e0`. The new retry-after-rejection and confirmed-without-reference tests passed.
- Handoff tests cover answered, busy, no-answer, failure, and invalid outcomes while asserting that no real transfer is claimed.
- Configuration tests verify local-mock defaults, log-level normalization, and rejection of production mode or invalid log levels.
- CI reports one upstream Starlette/httpx TestClient deprecation warning.
- The tests validate only the local simulation. They do not validate a real booking API, database durability, concurrency, voice quality, telephony, or production deployment.

## Provider-neutral voice session contract tests — verified in run #135
- Supported language tags are restricted to Tamil, Hindi, English, Kannada, and Telugu.
- Session events are parsed by their normalized `kind`; unknown extra fields are rejected.
- Blank-only transcripts and unrecognized/raw provider error strings are rejected at the boundary.
- Session end reasons and error codes use normalized safe values. These are schema/unit tests, not evidence of an actual provider connection or speech quality.

## Provider-neutral contract tests
- Reversed stay dates are rejected.
- Booking commands require explicit guest confirmation.
- A booking result cannot claim `confirmed` without an authoritative flag and booking reference. A new test explicitly checks the missing-reference case even when `authoritative=True`; passed in run #107.
- Pending outcomes remain distinct from confirmed outcomes.
- CI for the contract module passed in run #59.


## Concurrency regression test
- A direct concurrent-call test sends 40 same-idempotency-key requests across 12 threads and expects one simulated request ID.
- The implementation uses a process-local lock only. This test does not prove multi-process safety, durable idempotency, database transaction correctness, or real booking behavior.


## Additional booking validation coverage
- Booking requests for unknown properties return 404 without recording a request.
- Idempotency keys shorter than the schema's minimum length are rejected with 422.
- Both cases passed in GitHub Actions run #95.


## Latest idempotency regression tests — passed in CI run #118
- Invalid guest-count request followed by a valid retry with the same idempotency key should succeed after the invalid request returns 422.
- A conflicting reuse of an idempotency key should return 409 without changing the original result; replaying the original payload should return the original request ID and guest count.
- These are local simulation tests only; passing them does not establish durable or cross-process idempotency.


## Synthetic room-type fixture tests — passed in CI run #156 (49 tests total)
- Every property response should include room options with a non-empty ID/name, maximum guest count in the supported range, amenities, non-negative sample nightly price, and `demo_only=True`.
- Property detail tests verify expected demo room options; unknown property lookup must still return 404.
- These tests validate fixture shape only. They do not prove room-specific availability, current pricing, or booking behavior.


## Synthetic room-type fixture tests — passed in CI run #156 (49 tests total)
- Every property response includes room options with a non-empty ID/name, maximum guest count in the supported range, amenities, non-negative sample nightly price, and `demo_only=True`.
- Property detail tests verify expected demo room options; unknown property lookup returns 404.
- These tests validate fixture shape only. They do not prove room-specific availability, current pricing, or booking behavior.

## Room-specific demo capacity checks — passed in CI run #179 (55 tests total)
- A selected room type must belong to the requested property; unknown or cross-property room IDs return 404.
- Guests at/below the selected room's maximum capacity return `simulated_room_capacity_suitable`; larger groups return `simulated_room_capacity_exceeded`.
- Blank `room_type_id` is rejected; omitting it preserves the existing property-level response shape and status behavior.
- Every selected-room response carries the room identity/capacity and a warning that this is only a synthetic capacity check—not date-based inventory, price, or availability. These regressions passed in run #179 on commit `d83d9fee53e378112c2c3eb3bc84107dfac8c041`.

## Selected-room booking-request guardrails — passed in CI run #198 (62 tests total)
- Valid room selections are echoed by ID/name while status remains `simulated_not_reserved`.
- Guest counts above the selected room's capacity must not produce a reservation; the response must explicitly state that no room was reserved.
- Unknown or cross-property room selections must fail without storing the idempotency key; a corrected request may then use that key.
- Reusing an idempotency key with a different room must return 409, while replaying the original room selection returns the original request ID.
- Strict response-schema tests reject partial room metadata and room-capacity statuses without room metadata. All selected-room booking and schema guardrail tests passed in run #198 on commit `40daa12ba8975b8c575441b3d2775166a8187042`.
