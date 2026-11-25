---
id: RUST-FEAT-152
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/383
title: Use validated MD4 part hashes from eD2K file links
status: OPEN
priority: Minor
category: feature
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/383. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-152 - Use validated MD4 part hashes from eD2K file links

Parse and verify the stock and aMule p= link field through the existing MD4 hashset verifier. Preserve peer hashset acquisition when a link hashset is unusable.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
