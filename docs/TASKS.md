# Tasks and Acceptance Criteria

Statuses: **TODO**, **BLOCKED**, **IN PROGRESS**, **DONE**. Mark a task DONE only when its acceptance criteria are verified.

## P0 — Documentation baseline
- [x] **T-001: Establish initial documentation baseline** — governing rules, identity charter, project scope, architecture, state, tasks, decisions, security, testing, changelog, and interaction log exist.
  - Evidence: all eleven original files were verified in the GitHub tree; `SOUL.md` was subsequently created successfully.
- [ ] **T-002: Verify complete documentation set** — read back the final tree and key Markdown files after the SOUL addition and cross-reference updates.
  - Acceptance: all twelve expected Markdown files are present; links and file inventory agree; state/changelog/log reflect evidence.
- [ ] **T-003: Review documentation completeness** — identify any project-specific gaps without adding speculative or empty documents.
  - Acceptance: requirements, architecture, decisions, security, testing, state, tasks, changelog, handoff, and agent identity are consistent.

## P1 — Local backend
- [ ] **T-010: Scaffold FastAPI application** — IN PROGRESS. Minimal FastAPI health and typed response schemas are committed; configuration and runtime verification remain.
  - Acceptance: app starts and health test passes in a verified CI run.
- [ ] **T-011: Add synthetic multi-property fixtures** — IN PROGRESS. Three fictional properties and list/detail endpoints are committed; meaningful tests exist but have not run in CI.
  - Acceptance: schema validation and property lookup tests pass in a verified CI run.
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
Before each task, inspect relevant code/docs and Git status. Read `AGENTS.md` and `SOUL.md` before agent-related work. Update this list and `docs/STATE.md` as work changes. Follow the fourth-prompt full Markdown audit rule in `AGENTS.md`. After each project work unit, update affected documents and record verified progress.
