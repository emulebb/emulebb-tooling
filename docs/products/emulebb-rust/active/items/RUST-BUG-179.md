---
id: RUST-BUG-179
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/281
title: Handle malformed transfer-event frames predictably
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/281. This local document owns the durable engineering specification and evidence.

# RUST-BUG-179 - Handle malformed transfer-event frames predictably

## Summary

One malformed frame terminates the stream and outer UI reconnects. Add explicit per-frame/stream failure behavior with a regression; no claim of security compromise.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: webui.

## Current Findings

confirmed-static parse throw; outer retry limits impact

- `repos/emulebb-rust/webui/src/api.ts:1083`
- `repos/emulebb-rust/webui/src/api.ts:1137`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_webui.md` section 3.2

## Acceptance Criteria

- [ ] Malformed/truncated SSE data produces controlled reconnect or skip behavior, with no unhandled rejection or endless failure loop.
- [ ] Valid following events and cancellation retain expected semantics.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.
