---
id: RUST-BUG-193
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/379
title: Apply Kad publisher trust before keyword pagination
status: OPEN
priority: Minor
category: bug
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/379. This local document owns the durable engineering specification and evidence.

# RUST-BUG-193 - Apply Kad publisher trust before keyword pagination

Return matching entries with trust at least one before lower-trust entries, then apply the offset and limit in restrictive and unrestricted search. Preserve restrictive work bounds from #188.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
