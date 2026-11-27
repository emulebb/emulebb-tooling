---
id: RUST-BUG-188
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/371
title: Honor negotiated eD2K extended filename requests
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/371. This local document owns the durable engineering specification and evidence.

# RUST-BUG-188 - Honor negotiated eD2K extended filename requests

Match stock v0 hash-only, v1 part status, and v2 complete-source count. Cover standalone and all supported multipacket forms through both ordinary peer sessions and source probes.

The negotiated version follows the physical connection through callback
handoff and file switches. A legacy eMule INFO without an overriding tag
preserves the value already learned from HELLO. Honor the stock v2 count
after the zero part-count sentinel. Verify exact bytes and the boundary of
the next sub-opcode for each negotiated version.

Stock eMule and aMule readers use the declared eD2K part count for validation
and the real data part count for bitmap width. At an exact multiple of eight
data parts, the virtual EOF bit alone would need another byte. Omit that
byte from outgoing filename requests so the complete-source count and next
sub-opcode stay aligned. Keep decoding the wider bitmap used by historical
senders. Use length for standalone requests and full suffix framing for
multipackets. Prefer the native reader width when both interpretations are
valid. Normal file-status replies use their existing bitmap layout.

Qualify the boundary with a 77,824,000-byte transfer from each native client
and check the probe's filename bytes and matching metadata response. The
stock receiver rejects the misaligned sub-opcode. aMule can accept that
frame while reading the wrong complete-source count.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
