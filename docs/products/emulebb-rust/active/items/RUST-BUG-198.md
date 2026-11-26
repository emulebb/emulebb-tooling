---
id: RUST-BUG-198
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/392
title: Preserve Kad keyword load deferrals across restarts
status: OPEN
priority: Major
category: bug
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/392. This local document owns the durable engineering specification and evidence.

# RUST-BUG-198 - Preserve Kad keyword load deferrals across restarts

Stock eMule `ac3d52e` (`Search.cpp:158`, `Indexed.cpp:104,846,923`)
and amule-org aMule `c5989ec4a` (`Search.cpp:262`, `Indexed.cpp:215,425,1259`)
save and restore the keyword target ID and wall-clock expiry after a
high-load keyword store response. Rust keeps keyword-wide deadlines in memory
in `crates/emulebb-core/src/kad_publish_schedule.rs` and restores per-file
publication timestamps at startup. A newly shared file can publish a deferred
keyword early after a restart.

Persist and restore bounded, unexpired deadlines keyed by the canonical Kad
keyword target. In a deterministic clock and restart fixture, a load-100
response must defer the keyword for seven days, including for a newly shared
file. An unrelated target can publish while the deadline is active. Verify
expiry permits publication and expired entries stay expired after restart.

This is a parallel Client follow-up outside the Beta 3 release gate.
[RUST-CI-056](RUST-CI-056.md) covers reusing recent Kad contacts for lookups.
