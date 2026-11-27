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

Start after Beta 3 certification. Keep IPv6 peer TCP opt-in and preserve the
stock IPv4 fallback. Discover IPv6 endpoints over IPv4 eD2K server sessions and,
in a separate increment, over IPv4 Kad. Native IPv6 server and Kad transports
are separate work.

## Reference revisions

Use maintained amule-org aMule
[`23e4954d7dbdb8c5fff8414f65bec4f04313a3a8`](https://github.com/amule-org/amule/tree/23e4954d7dbdb8c5fff8414f65bec4f04313a3a8)
and eD2K-server `v0.9.89` at
[`57e425bdcd3c7f43795daed95413a1c8048bea0d`](https://github.com/andrey23127/ed2k-server/tree/57e425bdcd3c7f43795daed95413a1c8048bea0d).
Build from the pinned sources and retain the executable digests with the test
receipts. Use stock eMule for the IPv4 compatibility comparison.

## eD2K server discovery

Follow negotiated source records, address update `0x63`, and the server
dial-back verdict on the existing IPv4 connection. Require a real LowID
source discovered through the IPv6 sentinel, a direct IPv6 TCP HELLO, and a
hash-verified file with competing discovery paths disabled.

Use deterministic tests for default-off and legacy frames, mixed clear and
obfuscated source records, self-source rejection, failed reachability proof,
renumbering, withdrawal, in-flight reply parsing, and reconnect reset. Verify
IPv4 transfer and the stock HighID callback path after an IPv6 address is
withdrawn. [aMule server protocol](https://github.com/amule-org/amule/blob/23e4954d7dbdb8c5fff8414f65bec4f04313a3a8/docs/IPv6_Server_Sources.md)

The server additions in `084cc74` and `9a9c0824` offer a separately negotiated
same-server IPv6 callback. Current aMule implements the address update. Qualify
common source discovery first and track callback opt-in and refusal as a separate
interoperability check.

## Kad discovery

Publish a keyed source type 7 with `ip6` when verified IPv6 is the sole usable
route. Send the publication and lookup over IPv4 Kad through a separate pinned
aMule storer. Require the storer to preserve `ip6` and the downloader to complete
direct IPv6 TCP HELLO and a hash-verified transfer with competing discovery
disabled. Exercise each client as an IPv6 source across the two discovery
fixtures.

Cover wrong keys, missing or unusable `ip6`, renumbering, withdrawal, and IPv4
fallback in deterministic tests. Check that NAT traversal hint bits leave IPv6
TCP selection and encryption handling intact. Buddy pointers and alternate
transports have separate acceptance.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
