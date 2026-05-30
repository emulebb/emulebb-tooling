---
id: FEAT-004
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/54
title: Kad — Generalise KadPublishGuard abuse budget beyond PUBLISH_SOURCE
status: OPEN
priority: Minor
category: feature
labels: [kad, abuse-prevention, throttling, resource-budget]
milestone: ~
created: 2026-04-08
source: AUDIT-KAD.md (AUD_KAD_011, AUD_KAD_020)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/54. This local document is retained as an engineering spec/evidence record.

> Historical reference only: `stale-v0.72a-experimental-clean` and
> `analysis\stale-v0.72a-experimental-clean` are retired reference sources, not
> active branch targets or current baselines. Use them only as provenance or
> idea-extraction sources; landed status is determined against `main`. See
> [Historical References](../../HISTORICAL-REFERENCES.md).

## Summary

The `KadPublishGuard` throttle in the target tree does an excellent job of
protecting the `PUBLISH_SOURCE` path against abuse. The same budget model
should be extended to all other expensive Kad operations.

## Current State

`KadPublishGuard` provides:
- Per-IP source-publish throttling
- Drop and ban escalation for abusive publish rates
- Rejection of malformed publish metadata

This is strong local policy. But other expensive Kad paths (search responses
sending large contact sets, store operations, index key lookups under load)
have no equivalent protection.

## Proposed Generalisation (AUD_KAD_011, libtorrent AUD_KAD_020)

### Per-Opcode Token Buckets

For each expensive Kad opcode, maintain a token bucket:
- Token refill rate = maximum acceptable request rate per source IP.
- Each incoming request consumes one token.
- When the bucket empties: drop + log, escalate to temp ban after N drops.

### Byte-Based Quotas

In addition to request-count quotas:
- Track bytes consumed per IP per time window.
- Enforce a per-IP byte budget for expensive-response generation.

### Per-Prefix Budgets

- In addition to per-IP: track per `/24` prefix.
- Useful when multiple clients behind CGNAT share an IP.

### Explicit Memory Ceilings

- Add hard per-index memory ceilings (contacts stored, keywords indexed).
- Make eviction policy visible in logs.
- Evict low-trust and stale publishers first.

### Counters

Track and expose:
- Dropped expensive requests (by opcode, by reason).
- Malformed expensive requests (by opcode).
- Escalated abusive senders.

## Protocol Compatibility

All changes are local resource governance — no wire format or protocol changes.

## Files

- `srchybrid/kademlia/utils/KadPublishGuard.h` / `KadPublishGuard.cpp` — extend
- `srchybrid/kademlia/net/KademliaUDPListener.h` / `.cpp` — opcode dispatch hooks
- `srchybrid/kademlia/kademlia/Indexed.h` / `.cpp` — memory ceiling hooks

## Experimental Reference Implementation

**Status in `stale-v0.72a-experimental-clean`:** The generalization is partially done. `KadPublishGuard.cpp/h` is a new file (does not exist in main at all) implementing a standalone publish throttle class with:
- `PublishSourceMetadata` struct capturing source-type, source-port, buddy-IP, buddy-port, buddy-hash fields
- `EKadPublishThrottleDecision` enum (ALLOW, DROP, BAN)
- Per-IP token-bucket style publish rate enforcement
- Malformed-metadata rejection (missing required fields for PUBLISH_SOURCE)
- Integration hook in `KademliaUDPListener.h` (`m_publishGuard` member)

**What's NOT done:** Per-prefix budgets, byte-based quotas, explicit memory ceilings for other opcodes, and the counters/observability layer are not implemented. The file covers the PUBLISH_SOURCE use case cleanly but is not yet generalized to all expensive opcodes.

**Porting note:** `KadPublishGuard.cpp/h` are new files; add to `.vcxproj`. The guard is called from `KademliaUDPListener.cpp` in the `OP_KADEMLIA_PUBLISH_SOURCE_RES` / `OP_KADEMLIA_PUBLISH_NOTES_REQ` dispatch paths. Integration commit is `4798953`.
