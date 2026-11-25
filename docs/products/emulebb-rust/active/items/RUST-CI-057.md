---
id: RUST-CI-057
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/389
title: Assess negotiated eD2K LowID rendezvous
status: OPEN
priority: Minor
category: ci
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/389. This local document owns the durable engineering specification and evidence.

# RUST-CI-057 - Assess negotiated eD2K LowID rendezvous

Compare ordinary server callback, Kad buddy, and direct reask with the
optional same-server and cross-server IPv4 rendezvous for LowID pairs.
Measure peer reachability, fallback, and transport complexity before an
implementation decision.

Stock eMule `ac3d52e` is the baseline. amule-org aMule `c5989ec4a`
gates server coordination behind experimental
`ENABLE_NATT_SERVER_COORDINATION` and requires uTP. eD2K-server
`9a9c0824` exposes same-server and cross-server support.

This post-Beta 3 assessment follows stock route preservation
[RUST-BUG-189](RUST-BUG-189.md). Its acceptance is independent of
[IPv6 peer discovery](RUST-FEAT-149.md). Record revision-pinned fixtures
and the interoperability matrix under [RUST-CI-031](RUST-CI-031.md)
and [RUST-CI-006](RUST-CI-006.md).
