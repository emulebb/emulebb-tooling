---
id: RUST-BUG-187
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/370
title: Advance Kad bootstrap candidates across retries
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/370. This local document owns the durable engineering specification and evidence.

# RUST-BUG-187 - Advance Kad bootstrap candidates across retries

Keep bounded maintenance bootstrap rounds and advance across configured and restored endpoints after failed rounds. Preserve explicit single-endpoint bootstrap and no-seed behavior. Prove that a healthy eleventh endpoint can be reached after ten silent endpoints, and cover exhaustion and a changed candidate list.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
