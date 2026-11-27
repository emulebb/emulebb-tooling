---
id: RUST-FEAT-155
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/387
title: Retain bounded alternate eD2K routes for one known peer
status: OPEN
priority: Minor
category: feature
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/387. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-155 - Retain bounded alternate eD2K routes for one known peer

Prove a stock-compatible IPv4 case after #372 where a known peer is independently learned through two usable routes and the second works after the first fails. Evaluate current aMule and reuse existing route diagnostics.

For background server callbacks, settle an untagged refusal immediately when
exactly one outstanding request owns it in the connected server generation.
For ambiguous refusals, retain each request's own deadline. Cover both
download acquisition and upload promotion, including one and two outstanding
requests and reconnect while a refusal is pending.
[aMule comparison](https://github.com/amule-org/amule/pull/2617)

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](RUST-CI-031.md).
