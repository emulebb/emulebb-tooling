---
id: RUST-BUG-190
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/373
title: Enforce stock eD2K large-file capabilities
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/373. This local document owns the durable engineering specification and evidence.

# RUST-BUG-190 - Enforce stock eD2K large-file capabilities

Use the stock legacy maximum of 4,290,048,000 bytes where file capability governs peer metadata, server offers, and TCP or UDP source requests. Verify the boundary and next byte on capable versus legacy paths.

- Keep the legacy boundary separate from block offsets and hashset geometry.
- A capable TCP server receives the extended source-request size at boundary
  plus one. A capable offer recipient receives the high-size tag even when
  its value is zero. Keep incompatible targets out of source cooldown claims.
- The UDP large-file flag governs eligibility. The sized-request flag chooses
  the record shape independently.
- Follow stock for standalone filename and status responses. Both oracles
  gate multipacket metadata on the peer capability.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
