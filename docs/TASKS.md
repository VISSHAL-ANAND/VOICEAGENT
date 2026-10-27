# Tasks and Acceptance Criteria

Statuses: **TODO**, **BLOCKED**, **IN PROGRESS**, **DONE**. Mark a task DONE only when its acceptance criteria are verified.

## P0 — Documentation baseline
- [x] **T-001: Establish initial documentation baseline** — governing rules, identity charter, project scope, architecture, state, tasks, decisions, security, testing, changelog, and interaction log exist.
  - Evidence: all eleven original files were verified in the GitHub tree; `SOUL.md` was subsequently created successfully.
- [x] **T-002: Verify complete documentation set** — all twelve expected Markdown files were read during the fourth-prompt audit; recursive tree returned `truncated=false`.
  - Evidence: all twelve paths were fetched from `main`; current tree inventory and documentation links were reviewed. Audit record is in `docs/STATE.md` and `docs/INTERACTION_LOG.md`.
- [x] **T-003: Review documentation completeness** — reviewed all twelve Markdown files and reconciled stale architecture/testing/CI status.
  - Evidence: external property API contract, provider selection, privacy decisions, and production operations remain explicitly documented as blockers; no provider or paid service was selected without approval.

## P1 — Local backend
- [x] **T-010: Scaffold FastAPI application** — health endpoint, validated local-only configuration, typed schemas, safe 404 handling, and local setup instructions are committed.
  - Evidence: GitHub Actions run #105 passed dependency installation and all 34 pytest tests before the newest edge-case tests. CI verification for the newest tests is pending. One upstream TestClient/httpx deprecation warning remains.
- [x] **T-011: Add synthetic multi-property fixtures** — three fictional properties, typed schemas, and property list/detail endpoints are committed.
  - Evidence: GitHub Actions run #105 passed, including tests for demo-only records, city filtering, detail lookup, and unknown-property 404.
- [x] **T-012: Define internal property/booking contracts** — provider-neutral models and `PropertyManagementPort` exist in `app/contracts.py`; they are internal shapes, not the external API schema.
  - Evidence: GitHub Actions run #105 passed contract tests for date validation, guest confirmation, and authoritative booking-result invariants. A new test now covers an authoritative `confirmed` result missing its reference; CI verification is pending. External schema remains unknown until documentation is supplied.
- [ ] **T-013: Implement booking workflow with mocks** — IN PROGRESS. Added deterministic demo-capacity checks and an idempotent request simulation. It always returns `simulated_not_reserved` and never claims a real booking.
  - Remaining acceptance: continue failure/retry coverage and keep this simulation separate from the eventual authoritative API adapter. Added a test that an invalid unknown-property request does not poison a later valid retry with the same idempotency key. CI for the latest tests is pending. True uncertain-outcome recovery and price-change behavior need the authoritative booking/quote contract.
- [x] **T-014: Implement simulated manager handoff** — simulation supports answered, busy, no-answer, and failure outcomes; responses explicitly say no real call was transferred.
  - Evidence: GitHub Actions run #105 passed all 34 tests, including handoff outcome and invalid-input coverage. Real telephony transfer remains a separate production task.

## P1 — External contract discovery
- [ ] **T-020: Obtain property API materials** — sanitized JSON sample, schema, endpoints, auth, availability freshness, reservation semantics, idempotency, errors, tenant scoping.
  - Status: BLOCKED until materials are supplied.
- [ ] **T-021: Build property API adapter** — implement against the verified contract.
  - Acceptance: contract tests pass without exposing credentials or logging guest secrets.

## P2 — Voice and telephony research
- [ ] **T-030: Evaluate five-language voice capability** — Tamil, Hindi, English, Kannada, Telugu.
  - Acceptance: representative test set and scored results for recognition, pronunciation, language switching, numbers/dates, latency, and cost.
- [ ] **T-031: Evaluate inbound virtual-number providers** — verify India number eligibility, inbound calls, media streaming, transfer support, terms, and charges.
  - Acceptance: documented comparison based on current official provider information; no paid signup without approval.
- [ ] **T-032: Add voice adapter and browser/local prototype** — only after provider/API selection is justified.
  - Acceptance: interruptions, clarification, and tool invocation tested; mock and real modes clearly separated.

## P2 — Security and operations
- [ ] **T-040: Define data handling policy** — call recording, transcripts, retention, access, deletion, and applicable compliance review.
- [ ] **T-041: Add redacted structured logs and audit events** — no secrets or unnecessary personal data.
- [ ] **T-042: Define operational recovery** — timeouts, retries, unknown booking outcome, rate limiting, alerts, backup/recovery.

## P3 — Pilot and production
- [ ] **T-050: End-to-end pilot on one property** — client-approved test environment.
- [ ] **T-051: Validate manager live transfer** — answer, busy, no answer, transfer failure, and callback fallback.
- [ ] **T-052: Production readiness review** — security, privacy, provider costs, language accuracy, booking integrity, monitoring, support owner, and client approval.

## Work discipline
Before each task, inspect relevant code/docs and Git status. Read `AGENTS.md` and `SOUL.md` before agent-related work. Update this list and `docs/STATE.md` as work changes. Follow the fourth-prompt full Markdown audit rule in `AGENTS.md`. After each project work unit, update affected documents and record verified progress.
