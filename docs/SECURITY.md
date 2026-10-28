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
- **Not production-ready:** the limiter is in-memory, per-process, resets on restart, and cannot protect across workers. The app does not itself provide HTTPS/TLS, distributed/edge rate limiting, brute-force detection, monitoring/alerting, platform access restrictions, or deployment verification. Use a trusted hosting platform for TLS and edge controls; do not trust forwarded headers unless the proxy path is explicitly verified. The in-memory booking state is not production persistence. The user approved and deployed a limited mock-only Render Free test. Render logs show startup succeeded and unauthenticated GET / received 401; the health route and valid-token API access are not yet verified. The service's health-check setting is blank and auto-deploy is enabled; correct both in the dashboard. Do not use real guest data or real bookings. Do not use real guest data or real bookings.


## Render deployment verification — 2026-10-28
Render reports `voiceagent-remote-demo` is live on the Free plan. Startup logs show the application started successfully, and an unauthenticated `GET /` received 401. This supports that the bearer-token gate is active, but does not verify correct-token access or the health route. The web fetch tool could not independently retrieve the public endpoint. The actual Render service has an empty health-check path and automatic deployment enabled; change the health-check path to `/healthz` and disable automatic deployments in the dashboard. Never share the bearer token. This remains a public mock-only test and is not approved for real guest data or production bookings.


## Secret-safe remote smoke test
- Added manual-only workflow `.github/workflows/remote-smoke.yml` to check `/healthz` (200 and mock mode), unauthenticated API rejection (401), invalid-token rejection (401), and valid-token access (200 with the expected response shape).
- It reads `VOICEAGENT_API_TOKEN` only from GitHub Actions Secrets, validates the expected HTTPS host, and prints status-only results without request headers, tokens, or response bodies.
- **Setup is still required:** the repository owner must add the Render token privately as the repository Actions secret `VOICEAGENT_API_TOKEN`, then manually run **Actions → Remote demo smoke test → Run workflow**. Do not share the token with the assistant.
- The workflow tests the live mock demo; it does not prove production readiness, distributed rate limiting, tenant isolation, or real booking/telephony behavior.
