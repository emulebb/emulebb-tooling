---
id: RUST-BUG-140
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/189
title: Preflight Kad counted vectors before allocation
status: DONE
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

- [x] Impossible counts fail before allocation.
- [x] Truncated and oversized vectors return structured decode errors.
- [x] Valid boundary packets decode unchanged.
- [x] Every remotely controlled counted-vector shape has focused coverage.

## Validation

- Kad protocol decode tests and malformed packet vectors.
- Existing packet round-trip and golden tests.

## Resolution

- Preflighted remotely controlled Kad vector counts against minimum encoded sizes before allocation.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-kad-proto`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`
