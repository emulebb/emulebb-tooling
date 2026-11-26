---
id: RUST-CI-056
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/388
title: Measure aMule-inspired Kad republish seed reuse
status: OPEN
priority: Minor
category: ci
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/388. This local document owns the durable engineering specification and evidence.

# RUST-CI-056 - Measure aMule-inspired Kad republish seed reuse

Measure lookup traffic, acknowledgements, and stale fallback with a bounded prior-acknowledger cache. Use stock traffic and reply shapes with current aMule as the optimization comparator.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
