---
id: RUST-FEAT-062
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/233
title: Persist Kad routing state in SQLite and keep met files import-only
status: DONE
priority: Major
category: feature
labels: [rust, kad, sqlite, persistence, nodes-dat, server-met]
milestone: post-beta-polish
created: 2026-11-05
source: operator-approved profile continuity design 2026-11-05
---

# RUST-FEAT-062 - Persist Kad routing state in SQLite and keep met files import-only

SQLite owns the bounded Kad routing snapshot. The foundation retained node and contact identity across restart, ordered imports with the snapshot owner, and treated compatibility met files as read-only imports.

Delivered in [Rust PR #349](https://github.com/emulebb/emulebb-rust/pull/349) at [`7c0e5fbe`](https://github.com/emulebb/emulebb-rust/commit/7c0e5fbee9adb9fcbcdbb21918e1be42268a6bff). [Owning issue #233](https://github.com/emulebb/emulebb-rust/issues/233)

## Proof

- [Full pre-cutover record](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-FEAT-062.md)
- [Rust validation checks](https://github.com/emulebb/emulebb-rust/pull/349/checks)
- [Kad runtime checkpoint](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-FEAT-062.md#registered-kad-runtime-checkpoint-2026-11-16)
- [SQL fault, retry and reopen proof](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-REF-016.md#registered-category-checkpoint-2026-11-16)

## Remaining work

- [RUST-CI-055 - Qualify Kad checkpoint cadence and import-only lifecycle](https://github.com/emulebb/emulebb-rust/issues/354)
