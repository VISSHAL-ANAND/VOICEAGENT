# Testing and Verification Strategy

## Current status
No application code or tests have been verified at the initial documentation checkpoint. Commands will be added after the scaffold exists. Never report tests as passing unless executed.

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
- GitHub Actions run #39 passed dependency installation and all 26 pytest tests on commit `63dd66a21bf804340085f6119f256da838f62aa0`.
- Handoff tests cover answered, busy, no-answer, failure, and invalid outcomes while asserting that no real transfer is claimed.
- Configuration tests verify local-mock defaults, log-level normalization, and rejection of production mode or invalid log levels.
- CI reports one upstream Starlette/httpx TestClient deprecation warning.
- The tests validate only the local simulation. They do not validate a real booking API, database durability, concurrency, voice quality, telephony, or production deployment.
