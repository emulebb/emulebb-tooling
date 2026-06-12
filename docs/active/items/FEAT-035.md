---
id: FEAT-035
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/14
title: IPv6 dual-stack compatibility for current eD2K/Kad networking
status: OPEN
priority: Major
category: feature
labels: [ipv6, networking, dual-stack, kad, sockets, friends]
milestone: ~
created: 2026-04-20
source: eMuleAI release notes; eMule Qt announcement 2026-03-05; qBittorrent/libtorrent dual-stack DHT model
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/14. This local document is retained as an engineering spec/evidence record.

# FEAT-035 - IPv6 dual-stack compatibility for current eD2K/Kad networking

## Summary

Add real IPv6 support across the current eD2K/Kad networking stack instead of
remaining IPv4-only.

This is an explicit expansion feature, not a stock-preserving hardening task.
The goal is current-network dual-stack compatibility:

- IPv4 continues to work unchanged
- IPv6-capable peers can connect directly over IPv6
- addresses display, persist, copy, and log correctly across the app
- Kad/source paths can carry IPv6 endpoints only when the consumer path is
  end-to-end coherent

## Why Add It

Local and external signals point in the same direction:

- eMuleAI already ships an early IPv6 line
- eMule Qt publicly calls IPv6 one of the features the community has been asking for
- more users now sit behind CGNAT or IPv6-heavy consumer/mobile networks where IPv4-only
  behavior is increasingly limiting
- qBittorrent's libtorrent backend demonstrates the practical dual-stack DHT
  pattern: separate IPv4 and IPv6 DHT state, separate bootstrap vectors, and
  cross-family bootstrap help without pretending one address family is the
  other

## Intended Mainline Shape

- introduce a first-class peer/server address abstraction instead of assuming `uint32`
  IPv4 everywhere
- dual-stack listen/connect behavior for peer and server sockets
- IPv6-capable friend handling and clipboard/UI display
- Kad and source paths updated to carry IPv6 addresses safely on the current
  network only when the full consumer path can use them
- logging, tooltips, lists, and copy actions show bracketed IPv6 endpoints correctly
- settings and bind policy extended to cover IPv6 interfaces cleanly
- eMuleAI IPv6 metadata and tags treated as reference material only; no partial
  tag-only cherry-pick
- qBittorrent/libtorrent used as a design reference for state separation and
  bootstrap discipline, not as a wire-protocol template for eMule Kad

## Distinct IPv6 Kad Network

A separate IPv6-native Kad network is **not** part of this item. That design is
tracked as exploratory material in
[IDEA-IPV6-KAD-NETWORK](../../ideas/IDEA-IPV6-KAD-NETWORK.md).

The split is intentional:

- this item keeps the current public eMule network compatible
- the idea note can discuss separate IPv4/IPv6 routing tables, `nodes6`-style
  persistence, and bootstrap separation without implying release scope
- no distinct IPv6 Kad behavior is shipped or approved until promoted from an
  idea into an active item

## Scope Constraints

- keep IPv4 behavior fully intact
- prefer dual-stack over IPv6-only design
- defer any larger transport rewrite unless it is strictly required
- coordinate with `FEAT-032` and future traversal work rather than duplicating
  connectivity policy
- do not introduce mandatory new Kad tags, token semantics, opcode meanings, or
  packet shapes in this compatibility item
- do not change current Kad routing, publish, or search behavior in a way that
  old IPv4-only peers cannot satisfy
- do not describe IPv6 as a released 0.7.3 capability until active release
  evidence says it is shipped

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- Address abstraction:
  [`Address.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Address.h#L9),
  [`Address.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Address.cpp#L136).
- IPv6-related tags and mod metadata:
  [`Opcodes.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/Opcodes.h#L643).
- Client endpoint handling and capability flow:
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L1034),
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6128).
- IPv6 bind/display/resource integration touches are spread through the socket,
  list, and preferences code. Treat the eMuleAI tree as an implementation map,
  not as a single cherry-pick target.

## Protocol Change Notes

IPv6 support is easy to make incompatible if it is treated as a tag-only patch.
The eMuleAI implementation adds IPv6 metadata and private mod tags, but eMuleBB
must preserve stock peer behavior:

- IPv4 peers must continue to receive the same packet shapes and address
  semantics as before. IPv6 metadata must be omitted or ignored safely when the
  peer has not negotiated support.
- Any `TAG_IPV6`, serving-buddy IPv6, or miscellaneous IPv6-capability tag must
  be defined as optional, versioned, and ignorable. It cannot become mandatory
  Kad/source metadata on the public network.
- A custom IPv6 client-IP-change opcode is not approved for direct import. The
  current stock `OP_CHANGE_CLIENT_ID` behavior remains the baseline until a
  full dual-stack design defines the replacement path.
- Kad and source persistence must not silently reinterpret 32-bit IPv4 IDs as
  IPv6 endpoints. Persisted structures need explicit versioning or separate
  fields so downgrade and backup behavior remains clear.
- UI, REST, logs, friend links, and clipboard paths must all handle bracketed
  IPv6 endpoints consistently before network advertisement is enabled.

The implementation order should be address abstraction, UI/log/persistence
readiness, socket bind/connect support, then negotiated protocol exposure.

## Acceptance Criteria

- [ ] peer and server sockets can listen and connect on IPv6
- [ ] friends, logs, lists, and tooltips display IPv6 endpoints correctly
- [ ] Kad/source/address persistence handles IPv6 safely
- [ ] bind policy can target IPv6-capable interfaces without regressing IPv4
- [ ] mixed IPv4/IPv6 sessions run without breaking current network behavior
- [ ] eMuleAI IPv6 tag behavior is either implemented end-to-end or deliberately
      left out
- [ ] docs clearly distinguish current-network dual-stack compatibility from a
      distinct IPv6 Kad network
- [ ] no IPv6-related tag or opcode is advertised until the consumer path is
      implemented end-to-end and covered by downgrade tests
