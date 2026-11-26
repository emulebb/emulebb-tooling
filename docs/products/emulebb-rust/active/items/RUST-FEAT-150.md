---
id: RUST-FEAT-150
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/378
title: Learn eligible eD2K requesters as passive sources
status: OPEN
priority: Minor
category: feature
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/378. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-150 - Learn eligible eD2K requesters as passive sources

Compare multipart request admission with both oracles. Admit a useful requester via the current source owner once, preserving limits and avoiding complete, single-part and full downloads.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
