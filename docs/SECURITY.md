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
- `VOICEAGENT_EXPOSURE` defaults to `local` and accepts only `local` or `remote`. Remote mode requires `VOICEAGENT_API_TOKEN` to be configured with at least 32 characters; placeholder values are rejected. The token field is excluded from settings' `repr` to reduce accidental disclosure.
- In remote mode, API routes require an exact Bearer token and compare it using a constant-time comparison. Missing or invalid credentials receive 401 with a Bearer challenge. `/healthz` remains unauthenticated for basic health checks; do not put sensitive information in that response.
- Interactive docs, ReDoc, and OpenAPI routes are disabled when the app is initialized in remote mode. Local mode preserves current developer behavior.
- GitHub Actions run #243 on commit `f207f1969cc1cfdd969718d8851b842fec8efcd4` passed all 75 tests, including missing/invalid/valid credentials, health access, local compatibility, weak/placeholder tokens, invalid exposure values, and token repr redaction.
- **Not production-ready:** this control depends on the deployment explicitly setting `VOICEAGENT_EXPOSURE=remote`. HTTPS/TLS termination, rate limiting, brute-force/abuse controls, monitoring, platform access restrictions, security headers, and deployment-level verification are not yet implemented or verified. The application now enforces a 65,536-byte (64 KiB) request-body cap, including chunked bodies, but this does not replace reverse-proxy limits. The in-memory demo booking state is not safe for production. Do not deploy publicly until those gaps are addressed.

## Remote-test access control — initial implementation
- `VOICEAGENT_EXPOSURE` defaults to `local` and accepts only `local` or `remote`. Remote mode requires `VOICEAGENT_API_TOKEN` to be configured with at least 32 characters; placeholder values are rejected. The token field is excluded from settings' `repr` to reduce accidental disclosure.
- In remote mode, API routes require an exact Bearer token and compare it using a constant-time comparison. Missing or invalid credentials receive 401 with a Bearer challenge. `/healthz` remains unauthenticated for basic health checks; do not put sensitive information in that response.
- Interactive docs, ReDoc, and OpenAPI routes are disabled when the app is initialized in remote mode. Local mode preserves current developer behavior.
- Tests cover missing/invalid/valid credentials, health access, local compatibility, weak/placeholder tokens, invalid exposure values, token repr redaction, and request bodies over the 64 KiB cap. GitHub Actions run #254 on commit `cb53358b0f7075827b6780bb02da9c4be7ef1191` passed all 77 tests.
- **Not production-ready:** this control depends on the deployment explicitly setting `VOICEAGENT_EXPOSURE=remote`. HTTPS/TLS termination, request/body-size limits, rate limiting, brute-force/abuse controls, monitoring, platform access restrictions, security headers, and deployment-level verification are not yet implemented or verified. The in-memory demo booking state is not safe for production. Do not deploy publicly until those gaps are addressed.