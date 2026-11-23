---
id: RUST-FEAT-038
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/27
title: Add current-aMule-style endgame source takeover
status: DONE
priority: Minor
category: feature
labels: [rust, ed2k, download, scheduling, performance]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against current aMule 3.1
---

# RUST-FEAT-038 - Add current-aMule-style endgame source takeover

The foundation delivered bounded final-block takeover and redundant socket drain. Loopback evidence covers both winners, exact payload, accounting and closure without reconnect.

Delivered in [Rust PR #349](https://github.com/emulebb/emulebb-rust/pull/349) at [`7c0e5fbe`](https://github.com/emulebb/emulebb-rust/commit/7c0e5fbee9adb9fcbcdbb21918e1be42268a6bff). [Owning issue #27](https://github.com/emulebb/emulebb-rust/issues/27)

## Proof

- [Full pre-cutover record](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-FEAT-038.md)
- [Rust validation checks](https://github.com/emulebb/emulebb-rust/pull/349/checks)
- [Endgame implementation and evidence](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-FEAT-038.md#evidence)
- [Real-peer contention checkpoint](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-REF-016.md#real-peer-endgame-contention-checkpoint-2026-11-21)

## Remaining work

- [RUST-CI-054 - Qualify final-block takeover latency and aMule interoperation](https://github.com/emulebb/emulebb-rust/issues/353)
