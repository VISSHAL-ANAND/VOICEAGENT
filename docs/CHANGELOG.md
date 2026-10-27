# Changelog

Changes are recorded after they are actually made and verified.

## 2026-10-27
- Added `AGENTS.md` with project-wide engineering, security, testing, booking, voice, Git, documentation, and production rules.
- Added `SOUL.md` defining the receptionist's identity, communication style, truthfulness, booking boundaries, escalation, privacy, and failure behavior.
- Added `README.md` and project documentation for scope, architecture, decisions, security, testing, state, tasks, and handoffs.
- Verified the original eleven Markdown files in the GitHub recursive tree before adding `SOUL.md`; final verification of the complete twelve-file set is pending.
- No application code or external integration is claimed as implemented.

## 2026-10-27 — Backend scaffold
- Added typed response schemas and synthetic property fixtures for local-only development.
- Added FastAPI health, property-list, and property-detail endpoints.
- Added meaningful API tests and a GitHub Actions pytest workflow. The workflow is committed, but no run has been observed yet.
- No real booking or voice/telephony behavior is implemented.
