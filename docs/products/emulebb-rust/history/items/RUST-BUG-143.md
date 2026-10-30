---
id: RUST-BUG-143
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/193
title: Align machine-readable client scope and HTTP defaults
status: OPEN
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

- [ ] `parity_model` requires stock-observable parity except registered omissions and extensions.
- [ ] `default_exposure` states loopback-first with explicit authenticated non-loopback configuration.
- [ ] Policy and documentation validation passes.
- [ ] This policy-only item does not change runtime listener behavior.

## Validation

- Rust policy validation and documentation checks.
- Direct comparison with `RELEASE-SCOPE.md` and the listener guidance.
