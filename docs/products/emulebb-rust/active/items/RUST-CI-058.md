---
id: RUST-CI-058
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/391
title: Assess negotiated extended eD2K source exchange
status: OPEN
priority: Minor
category: ci
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule, amule-org aMule and eMuleAI protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/391. This local document owns the durable engineering specification and evidence.

# RUST-CI-058 - Assess negotiated extended eD2K source exchange

Compare the classic fixed-record SX2 from stock eMule `ac3d52e` with
the tagged records negotiated by amule-org aMule `c5989ec4a` and
eMuleAI `a2f05dc`. aMule's extended capability changes the meaning of
the SX2 version byte 1. Its skip-tags capability controls which
additional route tags are safe to send.

Measure whether validated relay or IPv6 route tags improve peer
reachability. Qualify both capability combinations, bounded unknown-tag
handling, and classic v2/v4 fallback. Keep one canonical route identity.
Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures.

This evidence item follows [classic route preservation](RUST-BUG-189.md),
[IPv6 peer discovery](RUST-FEAT-149.md) and
[alternate-route retention](RUST-FEAT-155.md).
