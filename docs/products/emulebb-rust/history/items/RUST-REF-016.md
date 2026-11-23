---
id: RUST-REF-016
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/155
title: Move blocking SQLite work behind bounded async persistence
status: DONE
priority: Major
category: refactor
labels: [rust, tokio, sqlite, async, persistence, performance]
milestone: post-beta-polish
created: 2026-10-23
source: 2026-10-23 Rust async and portability audit
---

# RUST-REF-016 - Move blocking SQLite work behind bounded async persistence

The foundation delivered bounded persistence admission, retained commands, and bounded resource reads. The persisted owners settle admitted work across caller cancellation and drain at shutdown.

Delivered in [Rust PR #349](https://github.com/emulebb/emulebb-rust/pull/349) at [`7c0e5fbe`](https://github.com/emulebb/emulebb-rust/commit/7c0e5fbee9adb9fcbcdbb21918e1be42268a6bff). [Owning issue #155](https://github.com/emulebb/emulebb-rust/issues/155)

## Proof

- [Full pre-cutover record](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-REF-016.md)
- [Rust validation checks](https://github.com/emulebb/emulebb-rust/pull/349/checks)
- [Foundation review checkpoint](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-REF-016.md#local-foundation-review-checkpoint-2026-11-23)
- [Memory-pressure drain and readmission](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/active/items/RUST-REF-016.md#live-pressure-drain-and-readmission-proof)

## Remaining work

- [RUST-CI-052 - Qualify the Rust foundation under sustained mixed load](https://github.com/emulebb/emulebb-rust/issues/351)
- [RUST-CI-053 - Qualify live upload and REST during SQLite writer contention](https://github.com/emulebb/emulebb-rust/issues/352)
