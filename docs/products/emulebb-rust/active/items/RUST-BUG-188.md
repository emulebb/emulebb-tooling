---
id: RUST-BUG-188
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/371
title: Honor negotiated eD2K extended filename requests
status: OPEN
priority: Major
category: bug
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/371. This local document owns the durable engineering specification and evidence.

# RUST-BUG-188 - Honor negotiated eD2K extended filename requests

Match stock v0 hash-only, v1 part status, and v2 complete-source count. Cover standalone and all supported multipacket forms through both ordinary peer sessions and source probes.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
