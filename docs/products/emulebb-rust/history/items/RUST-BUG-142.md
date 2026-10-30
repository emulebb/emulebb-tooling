---
id: RUST-BUG-142
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/191
title: Bound shared-directory watcher ingress before coalescing
status: OPEN
priority: Major
category: bug
labels: [rust, sharing, watcher, resource-bounds, reliability]
milestone: rust-v0.1.0-beta.3
created: 2026-10-30
source: 2026-10-30 bounded-ingress review of RUST-REF-010
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/191. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-142 - Bound shared-directory watcher ingress before coalescing

## Summary

Replace unbounded watcher ingress with bounded non-blocking admission that
collapses overflow into one authoritative reconcile requirement.

## Intended Shape

- Bound the callback-to-consumer queue without blocking the native watcher callback.
- Preserve final-intent path coalescing while recording one dirty generation on overflow.
- Schedule authoritative reconciliation after overflow and quiescence.
- Leave storage-domain scheduling, degraded-root REST state, periodic fallback,
  and cross-platform redesign in `RUST-REF-010`.

## Acceptance Criteria

- [ ] Event bursts cannot grow memory without bound.
- [ ] Overflow cannot lose eventual catalog authority.
- [ ] Rename and final-intent coalescing remain correct.
- [ ] Burst tests prove bounded queue depth and convergence.

## Validation

- Deterministic ingress saturation and overflow-collapse tests.
- Existing watcher action/coalescing and platform integration tests.
