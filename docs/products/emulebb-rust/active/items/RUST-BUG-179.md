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

Read-only revalidation on 2026-11-14 against `27d9b15e` confirmed that the
rejection is handled by the application: reconnect waits three seconds and
retains the last successfully delivered event ID. This is not an observed
unhandled rejection or tight reconnect loop. The parser still has no bound on
an unterminated frame, synthesizes an EOF terminator, and releases a failed
reader without cancelling its stream. Split UTF-8 is supported, while malformed
or truncated sequences use replacement characters. Define these boundaries in
the bounded follow-up rather than silently skipping malformed events without
replay semantics. This inspection ran no live campaign and made no source change.

- `repos/emulebb-rust/webui/src/api.ts:1083`
- `repos/emulebb-rust/webui/src/api.ts:1137`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_webui.md` section 3.2

## Acceptance Criteria

- [ ] Malformed/truncated SSE data produces controlled reconnect or skip behavior, with no unhandled rejection or endless failure loop.
- [ ] Valid following events and cancellation retain expected semantics.
- [ ] Unterminated frames have a bounded buffer; malformed JSON, UTF-8 and EOF behavior are deliberate, with controlled stream cancellation and preserved resume ID.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.
