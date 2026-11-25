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
dials. Preserve useful-part selection and requester exclusion in egress.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
