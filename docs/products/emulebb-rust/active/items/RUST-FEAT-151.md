---
id: RUST-FEAT-151
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/382
title: Apply bounded Smart ID to automatic eD2K selection
status: OPEN
priority: Minor
category: feature
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/382. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-151 - Apply bounded Smart ID to automatic eD2K selection

After a previous HighID, prefer a bounded number of alternate attempts before allowing a LowID winner. Preserve eventual acceptance and stock's explicit manual-server behavior.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
