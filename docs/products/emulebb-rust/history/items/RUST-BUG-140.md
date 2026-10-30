---
id: RUST-BUG-140
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/189
title: Preflight Kad counted vectors before allocation
status: OPEN
priority: Major
category: bug
labels: [rust, kad, protocol, decoding, resource-bounds]
milestone: rust-v0.1.0-beta.3
created: 2026-10-30
source: 2026-10-30 current-aMule hardening review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/189. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-140 - Preflight Kad counted vectors before allocation

## Summary

Validate remotely controlled Kad vector counts against the minimum remaining
packet size before allocation or iterative parsing.

## Intended Shape

- Derive the minimum encoded element size for each counted vector.
- Reject impossible counts before reserving capacity.
- Preserve structured decode errors and all valid boundary packets.
- Keep encoder overflow handling in `RUST-BUG-135` separate.

## Acceptance Criteria

- [ ] Impossible counts fail before allocation.
- [ ] Truncated and oversized vectors return structured decode errors.
- [ ] Valid boundary packets decode unchanged.
- [ ] Every remotely controlled counted-vector shape has focused coverage.

## Validation

- Kad protocol decode tests and malformed packet vectors.
- Existing packet round-trip and golden tests.
