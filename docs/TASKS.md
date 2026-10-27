# Tasks and Acceptance Criteria

Statuses: **TODO**, **BLOCKED**, **IN PROGRESS**, **DONE**. Mark a task DONE only when its acceptance criteria are verified.

## P0 — Baseline
- [ ] **T-001: Establish documentation baseline** — repository contains governing rules, project scope, architecture, state, tasks, decisions, security, testing, changelog, and interaction log.
  - Acceptance: each document exists, is non-duplicative, and describes verified facts versus proposals accurately.
- [ ] **T-002: Inspect repository/Git state** — verify default branch, tree, history, and clean/working state after baseline creation.
  - Acceptance: record actual outputs; do not infer local working-tree status from GitHub alone.

## P1 — Local backend
- [ ] **T-010: Scaffold FastAPI application** — health endpoint, configuration, typed schemas, error handling, and documented local setup.
  - Acceptance: app starts locally and health test passes.
- [ ] **T-011: Add synthetic multi-property fixtures** — fictional properties/rooms with no real guest information.
  - Acceptance: schema validation and multiple-property lookup tests pass.
- [ ] **T-012: Define internal property/booking contracts** — provider-neutral interfaces and explicit unknowns.
  - Acceptance: contract tests cover valid and invalid responses; no fabricated external schema.
- [ ] **T-013: Implement booking workflow with mocks** — availability, pricing, confirmation, and explicit booking states.
  - Acceptance: tests cover unavailable rooms, invalid dates/occupancy, price changes, duplicate requests, concurrency, and uncertain outcomes.
- [ ] **T-014: Implement simulated manager handoff** — interface and success/busy/failure outcomes.
  - Acceptance: tests pass and all local simulation is clearly labelled.

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
Before each task, inspect relevant code/docs and Git status. Update this list and `docs/STATE.md` as work changes. Every five user prompts during substantial work, reconcile and save a checkpoint when access permits.
