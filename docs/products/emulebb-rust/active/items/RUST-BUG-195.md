---
id: RUST-BUG-195
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/381
title: Bound automatic eD2K TCP search continuation
status: OPEN
priority: Minor
category: bug
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/381. This local document owns the durable engineering specification and evidence.

# RUST-BUG-195 - Bound automatic eD2K TCP search continuation

Use stock's maximum of five More requests as a bounded automatic Rust limit. Share the limit across session paths and preserve collected pages. Cover deadline, cancellation and early terminal pages.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
