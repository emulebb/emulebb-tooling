---
id: RUST-BUG-137
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/186
title: Decode legacy eD2K strings with negotiated stock semantics
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, protocol, interoperability, encoding]
milestone: rust-v0.1.0-beta.3
created: 2026-10-30
source: 2026-10-30 stock/current-aMule/Rust protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/186. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-137 - Decode legacy eD2K strings with negotiated stock semantics

## Summary

Replace lossy UTF-8 handling of legacy eD2K strings with the negotiated
stock/community eMule Unicode-or-codepage contract. Encoding must follow the
negotiated peer or server capability rather than always emitting UTF-8.

## Intended Shape

- Centralize negotiated eD2K text decode and encode policy at the packet seam.
- Preserve valid UTF-8 for Unicode-capable sessions.
- Use the stock-compatible legacy codepage path when Unicode is not negotiated.
- Reject or represent malformed input according to the owning packet contract;
  do not silently replace bytes before protocol logic sees them.

## Acceptance Criteria

- [ ] Legacy non-UTF-8 text decodes through the stock-compatible codepage path.
- [ ] Unicode-capable sessions retain UTF-8 behavior.
- [ ] Outbound encoding follows negotiated capability and preserves stock packet shapes.
- [ ] Deterministic vectors cover Unicode, legacy bytes, malformed input, and round trips.
- [ ] Stock and current-aMule interoperability evidence is retained.

## Validation

- Focused eD2K codec and packet tests.
- Stock/current-aMule packet or deterministic interop witnesses.
