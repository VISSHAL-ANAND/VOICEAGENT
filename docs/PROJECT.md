# Project Scope and Requirements

## Problem
A multi-property homestay/hotel company wants an AI receptionist to answer incoming phone calls, answer questions from verified data, and manage reservations. A separate developer owns the existing property-management application and expects to provide an API and JSON data. The exact contract is not yet available.

## Users
- Guests calling to ask questions or make bookings.
- Managers/staff receiving escalated calls and handling exceptional requests.
- Company operators monitoring call outcomes and booking reliability.

## Confirmed user decisions
- Backend: Python + FastAPI.
- Booking goal: AI should create confirmed reservations through the existing system.
- Escalation: if the guest asks for the manager, connect the manager into the active call when supported.
- Languages: Tamil, Hindi, English, Kannada, Telugu.
- Guest access: virtual phone number.
- Initial development budget: ₹0; client may pay after the prototype.
- Property integration: API plus JSON data expected; exact schema and API contract pending.

## Functional requirements
1. Answer incoming calls through an approved telephony provider.
2. Converse naturally and support the five target languages, subject to measured provider capability.
3. Identify the caller's intent and collect only the information needed for the task.
4. Search multiple properties and retrieve current property details.
5. Check availability for the full date range and guest count.
6. Retrieve/calculate prices using authoritative rules.
7. Read back key reservation details and obtain guest confirmation.
8. Create reservations through the existing application's API.
9. Verify the result and provide a booking reference only when returned by the authoritative system.
10. Transfer the active call to a manager on request.
11. Handle unavailable managers and failed transfers with a truthful fallback.
12. Record useful call/booking outcomes with appropriate privacy controls.
13. Escalate unsupported, ambiguous, or high-risk cases.

## Non-functional requirements
- Booking correctness and duplicate prevention.
- Low conversational latency; target to be set after measurement.
- Secure authentication, authorization, and tenant/property isolation.
- Resilience to API failures and uncertain booking outcomes.
- Observable, auditable operations without unnecessary sensitive logging.
- Clear provider costs and operational limits before production.
- Testability with mocks and synthetic data at ₹0 during early development.

## Out of scope for the first milestone
- Replacing the existing property-management application.
- Treating a static JSON export as live authoritative availability.
- Taking or storing payment-card data.
- Claiming production phone connectivity before provider integration is tested.
- Unapproved paid services or production deployment. A limited mock-only remote test deployment on Render Free has been approved and deployed; it does not authorize paid upgrades or production use.

## Acceptance criteria for the first local prototype
- A repeatable local run path is documented.
- Synthetic fixtures now support three fictional properties with two demo room types each. Room records include capacity, amenities, and illustrative nightly prices; they are demo data, not actual inventory, live quotes, or availability.
- Booking input validation and simulated capacity logic are covered by tests. Room-specific demo checks validate property/room association and maximum guest count; selected-room booking requests repeat that validation and include the room in idempotency comparison. They do not establish live availability, authoritative pricing, or a real reservation.
- Booking state clearly distinguishes pending, failed, and confirmed.
- Duplicate and timeout scenarios have explicit handling/tests.
- A simulated manager-handoff flow handles success and failure without claiming a real transfer.
- The five languages have a documented evaluation plan; unsupported quality is not assumed.
- Documentation states which services are mocked and which have been verified.
