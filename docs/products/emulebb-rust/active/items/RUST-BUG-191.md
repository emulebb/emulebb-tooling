---
id: RUST-BUG-191
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/374
title: Return stock eD2K metadata replies for partial and unknown files
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/374. This local document owns the durable engineering specification and evidence.

# RUST-BUG-191 - Return stock eD2K metadata replies for partial and unknown files

Return a sized all-zero standalone availability bitmap for known incomplete multipart files. Preserve the separate payload-serving gate. Match the stock filename and status sequence for unknown files.

For standalone filename requests and classic, EXT, and EXT2 multipackets,
stock eMule admits a queued download once it has received one part's worth of
bytes in aggregate. Include sparse blocks and exact contiguous progress in
that total. aMule's fallback instead compares the total file size with one
part. Retain the stock behavior and keep upload admission and payload reads
gated on verified parts.

The deterministic TCP fixture must cross from one byte below one part to
exactly one part across two incomplete parts. Below the boundary, expect
standalone filename silence and a file-not-found multipacket reply. At the
boundary, expect a standalone filename answer and a zero availability bitmap
in all multipacket forms. Standalone status keeps the two-part zero bitmap at
both points. The file remains ineligible for upload.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
