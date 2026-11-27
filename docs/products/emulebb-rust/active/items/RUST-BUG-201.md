---
id: RUST-BUG-201
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/402
title: Use inbound Kad TCP evidence for direct callback eligibility
status: OPEN
priority: Major
category: bug
labels: [rust, bug, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-27
source: Stock and aMule comparison for Beta 3 readiness
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/402. This local document owns the durable engineering specification and evidence.

# RUST-BUG-201 - Use inbound Kad TCP evidence for direct callback eligibility

## Summary

Only an accepted inbound TCP socket establishes reachability. Keep connection origin across an established session's role changes. Use the Kad TCP verdict for direct UDP callback ingress and HELLO advertisement while Kad is running. The advertisement additionally requires verified open UDP. Prove stopped Kad, accepted inbound proof, rejected daemon-dialed proof, and both server/Kad disagreement directions.

[Reference](https://github.com/amule-org/amule/pull/2634)

## Validation

Retain deterministic package-level evidence under [RUST-CI-031](RUST-CI-031.md).
