---
id: RUST-FEAT-153
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/385
title: Qualify Kad-buddy callback for queued LowID upload promotion
status: OPEN
priority: Minor
category: feature
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/385. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-153 - Qualify Kad-buddy callback for queued LowID upload promotion

Compare current aMule's callback route with stock and Rust. Measure whether a valid buddy-only peer can claim its queued turn without blocking other peers after a failed callback.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
