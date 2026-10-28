# Architecture — Initial Design

## Status
The repository contains a CI-tested local FastAPI prototype. Synthetic property data, demo availability/booking requests, and manager handoff are implemented; they are explicitly simulations. The authoritative property API, voice model, telephony, persistence, and deployment remain unimplemented. Revise the production design only when verified API/provider evidence and user-approved decisions are available.

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
- `app/catalog.py` contains three fictional properties, each with two synthetic room types, maximum guest capacity, amenities, and sample INR nightly prices. These prices and room labels are demo fixtures only, not a quote, inventory count, or availability signal. The data is not connected to any property-management system.
- `app/booking_simulator.py` applies fixed demo capacity limits and stores idempotency results in process memory, protected by a process-local lock so concurrent duplicate requests in this one process reuse the same result. Every request returns `simulated_not_reserved`; it does not create a reservation. It is still neither durable nor safe across multiple worker processes.
- These components are scaffolding only. The real property API adapter and booking transaction boundary remain blocked on the external API contract. The in-memory simulation has only a process-local lock; it is not durable, does not coordinate across worker processes, and must not be used for production.

- `app/handoff_simulator.py` models answered, busy, no-answer, and failed manager handoff outcomes. The endpoint always marks itself as demo-only and `real_transfer: false`. A real telephony adapter and active-call transfer are not implemented.

- `app/config.py` validates `VOICEAGENT_MODE` and `LOG_LEVEL`, currently allowing only local-mock mode. Live mode is deliberately rejected until authoritative property API and telephony adapters exist.

## Synthetic room-type fixture model
- `app/schemas.py` defines `RoomTypeSummary` with a demo room type ID, display name, maximum guest count, amenities, sample nightly INR price, and a strict `demo_only=True` marker.
- Property list/detail responses include the room type records. These fixtures enable deterministic prototype work but must never be used as live inventory, a binding quote, or a promise of availability. Availability remains a separate mock endpoint and is not room-type-specific yet.

## Provider-neutral contract layer
- `app/contracts.py` defines internal stay-query, property-record, availability-result, booking-command, booking-result, and adapter protocol shapes.
- These are VoiceAgent's internal contracts only. They do not claim to describe the other developer's external JSON/API schema.
- The booking command requires explicit guest confirmation; a result cannot be marked `confirmed` unless it is authoritative and includes a booking reference.
- The concrete external adapter remains blocked on verified API documentation and authentication/booking semantics.


## Provider-neutral voice session boundary — 2026-10-28
- `app/voice_contracts.py` defines normalized typed events for session start, user transcript, assistant transcript, session end, and safe session errors, plus a `VoiceSessionPort` protocol.
- The contract supports language tags for Tamil (`ta`), Hindi (`hi`), English (`en`), Kannada (`kn`), and Telugu (`te`). Transcript text is required and blank-only transcripts are rejected. Unexpected fields are forbidden; error codes are normalized rather than carrying raw provider error text across the boundary.
- This is a domain-level session boundary, not an audio wire protocol. It intentionally specifies no codec, sample rate, WebSocket framing, vendor SDK, or telephony event shape. Concrete adapters and orchestrator integration remain unimplemented until provider choices are approved and verified.


## Room-specific demo capacity boundary — 2026-10-28
The optional `room_type_id` on `GET /api/v1/demo/availability` resolves only within the requested property's synthetic room list. Unknown and cross-property room IDs fail closed with 404; blank IDs are rejected by request validation. A selected-room response reports whether the guest count fits the fixture's `max_guests`, with `demo_only: true` and an explicit notice that dates, inventory, price, and actual availability are not checked. The old property-level simulated response remains available when `room_type_id` is omitted. This is not a reservation or a production inventory API.

The demo booking-request endpoint also accepts an optional room ID. It validates the room through the same property-scoped fixture lookup and checks its guest capacity before recording the in-memory simulation request. A suitable capacity still results only in `simulated_not_reserved`; `capacity_status` separately reports the mock capacity outcome. The response echoes the property, stay dates, guest count, and selected room so clients can verify which input was simulated. Room selection participates in idempotency payload comparison, so reusing a key with a different room is rejected. Booking request schemas reject unknown fields and strip surrounding whitespace before validation. This remains process-local mock behavior, not a booking guarantee.


## Remote test access boundary — initial implementation
`app/config.py` supports an explicit `VOICEAGENT_EXPOSURE=remote` setting that requires a 32-character-or-longer `VOICEAGENT_API_TOKEN`. In remote mode, all API routes except `/healthz` require a Bearer token, and interactive docs/OpenAPI routes are disabled at app initialization. The token is compared without ordinary string equality and excluded from settings repr. This is an initial access gate only, not a complete public deployment architecture; TLS, rate limiting, body-size limits, monitoring, and hosting configuration remain unresolved.

## Remote test access boundary — initial implementation
`app/config.py` supports an explicit `VOICEAGENT_EXPOSURE=remote` setting that requires a 32-character-or-longer `VOICEAGENT_API_TOKEN`. In remote mode, all API routes except `/healthz` require a Bearer token, and interactive docs/OpenAPI routes are disabled at app initialization. The token is compared without ordinary string equality and excluded from settings repr. This is an initial access gate only, not a complete public deployment architecture; TLS, rate limiting, body-size limits, monitoring, and hosting configuration remain unresolved.