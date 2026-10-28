# Security and Privacy Baseline

This document defines minimum requirements; it is not a completed security audit or legal opinion.

## Assets
- Guest contact and booking details.
- Property inventory, pricing, and management API credentials.
- Call audio, transcripts, call metadata, and audit events.
- Manager contact/routing configuration.
- Application secrets and deployment configuration.

## Threats and controls
- **Unauthorized booking/data access:** authenticate external API requests, enforce least privilege, scope every operation to the correct company/property, and never trust caller-provided booking IDs alone.
- **Prompt injection or malicious callers:** treat speech and retrieved data as untrusted; model instructions cannot bypass backend authorization or validation.
- **Incorrect/duplicate reservations:** validate on the server, recheck availability, use idempotency/concurrency controls supported by the source system, and handle unknown outcomes safely.
- **Secret leakage:** no secrets in source, frontend bundles, examples, commits, or logs; use environment configuration and approved secret storage.
- **Sensitive logging:** redact credentials and minimize guest phone numbers, names, transcripts, and booking details in logs.
- **Abuse/cost exhaustion:** apply appropriate authentication, request limits, timeouts, quotas, and monitoring.
- **Cross-tenant access:** enforce tenant/property boundaries at every API operation.
- **Retention exposure:** define access, retention, deletion, and backup policies for audio/transcripts before production.

## Data minimization
Collect only details needed for the requested service. Do not collect or store payment-card data. Use synthetic fictional data in development. Do not upload real guest data to third-party AI services until the client has approved the data flow and applicable requirements have been reviewed.

## Recording and compliance
Before launch, decide whether calls are recorded or transcribed, provide required notices/consent, restrict access, define retention/deletion, and review applicable Indian privacy and telecommunications requirements with the client/legal adviser. Requirements depend on actual deployment and processing choices.

## Incident response
Document a way to rotate exposed credentials, disable compromised integrations, investigate audit events, notify responsible operators, and recover service. Do not place secrets in incident reports.

## Required pre-production checks
- Authentication and authorization tests.
- Tenant/property isolation tests.
- Input and external response validation.
- Redaction checks for logs.
- Rate limiting and timeout behavior.
- Booking idempotency and unknown-outcome handling.
- Retention and access-control review.
- Dependency and configuration review.

No security control should be marked complete until implementation and verification evidence exist.

## Current prototype guardrails
- `app/config.py` accepts only `VOICEAGENT_MODE=local-mock`; it rejects production/live modes because no authoritative API or telephony integration is configured.
- `LOG_LEVEL` is validated against standard Python levels. The current app configures standard logging but does not log guest content, phone numbers, credentials, or booking payloads.
- Booking and simulated handoff request schemas reject unexpected fields; required strings are whitespace-normalized before validation. Booking responses use a constrained status and carry the capacity result separately from the non-reservation status.
- Regression tests verify unexpected booking fields and whitespace-only idempotency keys are rejected, and verify that selected room, dates, and guest count are preserved in the simulated result.
- These checks are development guardrails, not a substitute for deployment secrets management, authentication, authorization, tenant isolation, rate limiting, request/body-size limits, CSRF protections where applicable, durable idempotency, or production review. The prototype must not be exposed as a public guest-facing service.


## Remote-test access control — initial implementation

- `VOICEAGENT_EXPOSURE` defaults to `local` and accepts only `local` or `remote`. Remote mode requires a non-placeholder `VOICEAGENT_API_TOKEN` of at least 32 characters; the token is excluded from settings' `repr`.
- In remote mode, API routes require an exact Bearer token and compare it using a constant-time comparison. Missing or invalid credentials receive 401 with a Bearer challenge. `/healthz` remains unauthenticated and must not expose sensitive information. Interactive docs, ReDoc, and OpenAPI routes are disabled.
- The app enforces a 65,536-byte (64 KiB) request-body cap and, in remote mode, an in-process sliding-window limiter defaulting to 60 requests per client IP per minute. It returns 429 and `Retry-After` when the limit is exceeded. Configuration is validated through `VOICEAGENT_RATE_LIMIT_PER_MINUTE` (1–10,000). Tests verify the limit, response headers, and that caller-supplied `X-Forwarded-For` does not change the key.
- Responses add `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `Cross-Origin-Resource-Policy`, and `Cache-Control: no-store`. Remote mode also sets a restrictive JSON/API-oriented Content Security Policy. HSTS is emitted only when the ASGI request scheme is HTTPS; this does not configure TLS at the hosting layer.
- GitHub Actions run #282 on commit `47653c39183d5f943aea3d502ab8b0ac21c73e52` passed all 87 tests. One upstream Starlette/httpx TestClient deprecation warning remains.
- **Not production-ready:** the limiter is in-memory, per-process, resets on restart, and cannot protect across workers. The app does not itself provide HTTPS/TLS, distributed/edge rate limiting, brute-force detection, monitoring/alerting, platform access restrictions, or deployment verification. Use a trusted hosting platform for TLS and edge controls; do not trust forwarded headers unless the proxy path is explicitly verified. The in-memory booking state is not production persistence. The user approved a limited mock-only Render Free test, but the service has not been created/deployed; verify the actual deployment before sharing its URL. Do not use real guest data or real bookings.
