---
id: RUST-FEAT-148
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/376
title: Serve and browse eD2K peer shared-file lists
status: OPEN
priority: Major
category: feature
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/376. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-148 - Serve and browse eD2K peer shared-file lists

Beta 3 requires bidirectional browsing against stock eMule and aMule. Serve flat and directory views with Everyone as the fresh-profile default, verified Friends, and Off. Make the existing REST and WebUI browse action fetch bounded peer results. Cover capability advertising, safe virtual directory names, and a 100,000-file catalog.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
