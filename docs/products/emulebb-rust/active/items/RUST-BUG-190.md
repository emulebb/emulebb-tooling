---
id: RUST-BUG-190
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/373
title: Enforce stock eD2K large-file capabilities
status: OPEN
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

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
