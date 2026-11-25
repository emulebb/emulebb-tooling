---
id: RUST-BUG-189
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/372
title: Preserve eD2K SX2 hybrid IDs and callback routes
status: OPEN
priority: Major
category: bug
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/372. This local document owns the durable engineering specification and evidence.

# RUST-BUG-189 - Preserve eD2K SX2 hybrid IDs and callback routes

Preserve versioned HighID and LowID wire identity and the source server tuple through intake and response. Prove a valid hybrid .0 endpoint, callback eligibility, and SX2 v2/v4 framing.

Deduplicate directly reachable peers by endpoint and LowIDs by server
endpoint plus client ID. Carry the route through durable reads and
preparation. LowIDs use existing callback admission and never become direct
dials. Classic stock eMule and aMule replies omit genuine LowIDs.
Preserve the known server tuple of offered HighIDs, useful-part selection,
and requester exclusion in egress. Use the distinct v4 hybrid encoding
for a directly reachable address ending in .0.

After a metadata-only probe hands off its live socket, send deferred SX2
inside the negotiated legacy multipacket for peers without file identifiers.
aMule 3.0.1 reads the three-byte SX2 prefix but checks the original standalone
payload against the SX1 length, so it disconnects before the hashset exchange.
Stock eMule and current aMule accept the embedded request. Current aMule also
accepts the standalone request after amule-org commit `b99d8c2d1`.
Verify the standard and extended legacy envelopes and retained standalone
behavior without restarting the connection or repeating filename and status
requests.

[RUST-BUG-197](RUST-BUG-197.md) tracks source replies from the upload
queue for complete library shares. [RUST-CI-058](RUST-CI-058.md) tracks
the negotiated tagged source extension.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
