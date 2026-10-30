---
id: RUST-BUG-141
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/190
title: Converge OFFERFILES v1 negotiation with the documented contract
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, protocol, offerfiles, interoperability]
milestone: rust-v0.1.0-beta.3
created: 2026-10-30
source: 2026-10-30 current-aMule and ed2k-server contract review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/190. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-141 - Converge OFFERFILES v1 negotiation with the documented contract

## Summary

Align Rust OFFERFILES v1 negotiation with the current server contract and
current aMule behavior while preserving stock fallback on the same connection.

## Intended Shape

- Wait up to five seconds for the first post-login advertisement.
- Accept only the first complete valid policy snapshot.
- Treat missing, partial, duplicate, malformed, or wrongly typed negotiation as legacy.
- Enforce a 500 ms interval floor and retain the snapshot for the connection lifetime.
- Permit only safe tightening from an explicitly supported live policy update.

## Acceptance Criteria

- [ ] Absent or invalid negotiation selects stock publication on the same connection.
- [ ] A valid first snapshot remains authoritative for that connection.
- [ ] Reconnect starts a fresh negotiation and pacing state.
- [ ] Deterministic valid, absent, malformed, duplicate, late, reconnect, stock, and current-aMule cases pass.

## Validation

- Focused eD2K server-session and publication tests.
- Deterministic `ed2k-server` contract fixtures and current-aMule interoperability.
