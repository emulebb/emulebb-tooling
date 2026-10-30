---
id: RUST-FEAT-055
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/192
title: Register bounded automatic Kad search widening
status: OPEN
priority: Major
category: feature
labels: [rust, kad, search, protocol-extension, interoperability]
milestone: rust-v0.1.0-beta.3
created: 2026-10-30
source: 2026-10-30 Beta 3 Kad scope decision
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/192. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-055 - Register bounded automatic Kad search widening

## Summary

Retain automatic `KADEMLIA_FIND_VALUE_MORE` widening as the default for
user-facing keyword, source, and notes searches. This is the headless
equivalent of exhausting current aMule's bounded user-triggered More Results
action while preserving stock-compatible packet shapes.

## Intended Shape

- Reask at most four distinct closest eligible responders after ordinary convergence.
- Share the normal traversal concurrency, deadline, cancellation, correlation, and deduplication controls.
- Keep maintenance, publish, node, buddy, and stalled-lookup recovery on stock recovery-only policy.
- Record wider requests and their incremental contacts and results.
- Register the default-on extension and its stock fallback contract.

## Acceptance Criteria

- [ ] Public value searches retain bounded automatic widening by default.
- [ ] No wider request is duplicated or sent after deadline or cancellation.
- [ ] Non-user-facing traversals retain recovery-only behavior.
- [ ] Diagnostics expose widening cost and yield.
- [ ] The extension registry documents compatibility, policy, and bounds.

## Validation

- Traversal state-machine tests for four-reask, distinct-peer, deadline, cancellation, and deduplication behavior.
- Stock packet-shape goldens and current-aMule comparison evidence.
