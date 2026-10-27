# Architecture — Initial Design

## Status
Proposed architecture only. The repository currently has no verified application implementation. Revise this document after the property API contract and provider research are available.

## Components
1. **Telephony adapter** — receives inbound call events, streams audio if supported, and performs live transfers.
2. **Voice/session adapter** — connects a realtime voice model to the conversation orchestrator; isolates vendor-specific protocol.
3. **Conversation orchestrator** — maintains session state, asks clarifying questions, and requests allowed backend operations.
4. **Property API adapter** — authenticates to the existing application, validates responses, and maps external schemas into internal typed models.
5. **Booking service** — deterministic validation and state transitions for availability, pricing, reservation creation, and result verification.
6. **Manager handoff service** — initiates and tracks transfer outcomes and fallback paths.
7. **Persistence/audit layer** — stores only necessary operational records, with retention and access controls.
8. **Observability** — structured redacted logs, metrics, tracing, and actionable errors.

## Trust boundaries
- Phone audio/transcripts are untrusted input.
- The voice model is not an authorization boundary and cannot directly mutate booking data.
- External API responses are untrusted until validated.
- Secrets remain server-side.
- All reservation mutations pass through backend validation and the authoritative booking API.
- Guest and property data must be scoped to the correct company/tenant.

## Booking flow
1. Collect location/property preference, check-in/out dates, and occupancy.
2. Validate and normalize inputs and time zone/date semantics.
3. Search the authoritative API.
4. Present only returned options and verified prices.
5. Confirm the selected property, room, dates, guest count, and price with the guest.
6. Recheck availability and create the reservation using supported idempotency/concurrency controls.
7. Verify the API result and persist a redacted audit event.
8. Tell the guest the confirmed result only when the API confirms it.

## Handoff flow
1. Detect an explicit manager request or escalation condition.
2. Tell the caller the system will attempt a transfer.
3. Ask the telephony provider to transfer the active call.
4. Track the result.
5. If busy/unanswered/failed, offer the approved fallback and record the outcome.
A mocked local handoff must be labelled as simulated and must not imply a real phone transfer.

## Deployment shape
Local development and mocked dependencies first. Production deployment, persistent WebSocket/audio support, regional latency, provider availability in India, privacy requirements, and total cost must be evaluated before selecting hosting/telephony vendors.

## Open architecture questions
- Property API schema, auth, rate limits, and booking semantics.
- Voice model's five-language quality, latency, and cost.
- Indian virtual-number availability and manager-transfer support.
- Need for PostgreSQL/Supabase versus simpler local persistence during prototype.
- Recording/transcription policy and retention requirements.

## Implemented local prototype checkpoint
- `app/main.py` exposes health, synthetic property list/detail, demo availability, and demo booking-request endpoints.
- `app/catalog.py` contains three fictional properties. The data is not connected to any property-management system.
- `app/booking_simulator.py` applies fixed demo capacity limits and stores idempotency results in process memory. Every request returns `simulated_not_reserved`; it does not create a reservation.
- These components are scaffolding only. The real property API adapter and booking transaction boundary remain blocked on the external API contract. The in-memory simulation is not concurrency-safe or durable and must not be used for production.
