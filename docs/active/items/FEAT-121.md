---
id: FEAT-121
workflow: local
github_issue:
title: STUN UDP egress gate for the VPN guard (eMuleBB, emulebb-rust, libtorrent)
status: OPEN
priority: Major
category: feature
labels: [vpn-guard, networking, stun, egress, security]
milestone: 0.8.x
created: 2026-06-14
source: operator request - the VPN guard's egress public-IP check only covered TCP/HTTP, leaving the UDP data-plane egress unverified
---
# FEAT-121 - STUN UDP egress gate for the VPN guard

## Summary

The VPN guard verifies that the client's egress public IP falls inside the
operator's allow-listed CIDRs before P2P networking is permitted. Until now that
check ran only over **TCP/HTTP** (`PublicIpProbe`), which cannot prove the
**UDP** data-plane egress (eD2k KAD / source reask) leaves through the bound
VPN/tunnel interface.

Add an RFC 5389 **STUN Binding** probe that reports the reflexive (public)
address as observed over UDP, egress-pinned to the same interface as the P2P
sockets (`IP_UNICAST_IF`). Wire it into the VPN guard as the **primary gate**:
STUN must report an allowed IP first, then the existing HTTP probe **confirms**
the TCP path. Either check failing fails the guard closed (the existing
pause-all-P2P path).

Implemented consistently across all three clients that bind to the VPN:
eMuleBB (C++/MFC), emulebb-rust (eD2k), and the qBittorrentBB libtorrent fork.

## Behavior

- **Sequential gate**: STUN (UDP) gate -> on allowed IP -> HTTP (TCP) confirmer
  -> on allowed IP -> guard approved. Any failure / out-of-range IP fails closed.
- **Egress pinning**: each probe socket is bound to the active bind address and
  `IP_UNICAST_IF`-pinned to the tunnel interface, so the reflexive address is the
  real UDP egress.
- **Source filtering**: each probe `connect()`s to its STUN server so the kernel
  drops datagrams from any other source (no spoofed Binding responses).
- **Resilience by fan-out**: a fixed set of public STUN servers is raced
  concurrently; the first valid reflexive address wins; the probe fails only when
  every server fails. No per-socket retransmits. When one server wins the others
  are cancelled (rust/libtorrent) or self-terminate at their bounded timeout
  (eMuleBB threads).
- **IPv4 gate** only for now.

## Shared design across the three implementations

- Identical codec (build request / parse `XOR-MAPPED-ADDRESS` + legacy
  `MAPPED-ADDRESS`), verified against canonical byte vectors.
- Same built-in server list (Google 19302, Cloudflare/Nextcloud 3478), kept in
  sync by hand: `StunProbeSeams::GetStunIpv4ProbeServers` (eMuleBB),
  `DEFAULT_STUN_SERVERS` (rust), `default_servers[]` (libtorrent).
- Same per-server probe: resolve (DNS ok) -> bind + egress-pin -> connect ->
  single send -> bounded recv -> parse.

## Constraints

- The exe must be on the hide.me split-tunnel whitelist for its UDP traffic to
  egress through the tunnel; coordinated by `emule_test_harness.hideme_split_tunnel`.
- Preserve the existing VPN-guard fail-closed semantics; no change to the
  allow-list CIDR matching (`VpnGuardSeams::IsPublicIpv4Allowed`).
- Minimum drift; the HTTP probe path is unchanged apart from now running as the
  confirmer behind the STUN gate.

## Acceptance Criteria

- [x] STUN probe egress-pinned to the tunnel, source-filtered via `connect()`.
- [x] VPN guard gates on STUN then confirms with HTTP; both fail closed.
- [x] Multi-server race, single send, no retransmit, in all three clients.
- [x] Codec verified against canonical vectors (eMuleBB) + unit tests (rust).
- [x] Live-verified on eMuleBB over the hide.me tunnel (gate + confirm pass).
- [x] Debug, Release, and diagnostics Release x64 app builds pass before commit.
- [ ] libtorrent change compiled in a qBittorrentBB build (deferred: built on next
      qBittorrentBB build).

## Release Note

VPN-egress hardening. New feature; under the active 0.7.3 release freeze it
targets the 0.8.x line. The libtorrent-side probe is unwired (primitive only)
until STUN is integrated into qBittorrentBB.
