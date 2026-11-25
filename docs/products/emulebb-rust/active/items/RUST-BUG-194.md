---
id: RUST-BUG-194
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/380
title: Retain Kad publisher filename votes in keyword search
status: OPEN
priority: Minor
category: bug
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/380. This local document owns the durable engineering specification and evidence.

# RUST-BUG-194 - Retain Kad publisher filename votes in keyword search

Preserve filename variants by publisher and use the leading filename for matching and replies. Verify refresh, expiry and restore. Download-name selection remains with #87.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
