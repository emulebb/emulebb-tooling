---
id: RUST-FEAT-149
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/377
title: Add opt-in IPv6 peer TCP through eD2K server discovery
status: OPEN
priority: Major
category: feature
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/377. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-149 - Add opt-in IPv6 peer TCP through eD2K server discovery

Post-Beta 3. Follow amule-org aMule and eD2K-server's negotiated source extension over IPv4 server TCP. Cover address verification and withdrawal, LowID IPv6 discovery, and stock IPv4 fallback. Keep native Kad and server transport IPv6 as separate follow-ups.

Use amule-org aMule `c5989ec4a` and eD2K-server `9a9c0824` for
the shared IPv6 source discovery contract. The current IPv4 behavior
remains the stock compatibility baseline.

The server additions in `084cc74` and `9a9c0824` offer a separately
negotiated same-server IPv6 callback to verified LowID requesters and
opted-in targets. Current aMule implements address update `0x63` and
lacks the new request and opt-in exchange. Qualify the common discovery
path first, then qualify callback refusal, withdrawal, and fallback
against the server extension. Keep both checks post-Beta 3.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
