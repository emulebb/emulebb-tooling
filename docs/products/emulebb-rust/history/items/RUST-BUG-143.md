---
id: RUST-BUG-143
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/193
title: Align machine-readable client scope and HTTP defaults
status: DONE
priority: Major
category: bug
labels: [rust, policy, scope, http, documentation]
milestone: rust-v0.1.0-beta.3
created: 2026-10-30
source: 2026-10-30 release-scope and machine-policy reconciliation
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/193. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-143 - Align machine-readable client scope and HTTP defaults

## Summary

Align the machine-readable Rust client policy with the approved full
stock-observable parity scope and the implemented loopback-first listener model.

## Acceptance Criteria

- [x] `parity_model` requires stock-observable parity except registered omissions and extensions.
- [x] `default_exposure` states loopback-first with explicit authenticated non-loopback configuration.
- [x] Policy and documentation validation passes.
- [x] This policy-only item does not change runtime listener behavior.

## Validation

- Rust policy validation and documentation checks.
- Direct comparison with `RELEASE-SCOPE.md` and the listener guidance.

## Resolution

- Aligned machine policy and listener guidance on stock-observable parity and loopback-first authenticated exposure.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `python tools/rust_quality_gate.py policy`; documentation validation
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`
