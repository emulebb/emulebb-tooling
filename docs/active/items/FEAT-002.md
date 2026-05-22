---
id: FEAT-002
workflow: github
github_issue: https://github.com/eMulebb/eMule/issues/7
title: Kad SafeKad — evolve from coarse same-IP gate into layered trust model (CGNAT fix)
status: OPEN
priority: Major
category: feature
labels: [kad, safekad, routing, cgnat, trust]
milestone: ~
created: 2026-04-08
source: AUDIT-KAD.md (AUD_KAD_006, AUD_KAD_007)
---


> Workflow status is tracked in GitHub: https://github.com/eMulebb/eMule/issues/7. This local document is retained as an engineering spec/evidence record.

> Historical reference only: `stale-v0.72a-experimental-clean` and
> `analysis\stale-v0.72a-experimental-clean` are retired reference sources, not
> active branch targets or current baselines. Use them only as provenance or
> idea-extraction sources; landed status is determined against `main`. See
> [Historical References](../../HISTORICAL-REFERENCES.md).

## Summary

`SafeKad` is the local Kad anti-abuse layer. It currently enforces near-"one
routed node per public IP" semantics. This is effective against simple Sybil
stuffing but is too blunt for modern NAT-heavy networks:

- **CGNAT** — mobile carriers share a single public IP across thousands of users
- **Enterprise NAT** — large offices appear as one IP
- **Campus NAT** — universities, ISPs

The result is that legitimate peers are rejected in dense NAT environments,
degrading route diversity unintentionally.

## Current Hard-Gate Behaviour (AUD_KAD_006)

A contact from an already-seen IP is rejected at routing admission. There is
no probation, no port-differentiation, no density-aware fallback.

2026-05-21 upstream revalidation: aMule issue #668 raised the same question for
its Kad routing table, specifically whether one KadID per public IP and ten per
/24 remain appropriate under widespread CGNAT. Current eMuleBB `main` still has
the same kind of hard gate in `srchybrid/kademlia/routing/RoutingBin.cpp`
(`MAX_CONTACTS_IP` and `MAX_CONTACTS_SUBNET`), so this issue remains the
correct backlog home for that concern.

## Proposed Layered Trust Model (AUD_KAD_007)

Replace the hard gate with a graduated policy:

| Signal | Action |
|--------|--------|
| New contact, unseen IP | Normal admission |
| New contact, same IP, different UDP port, stable behaviour | Admit to **probation** — not preferred for routing but not rejected |
| Probationary contact passes N successful verified interactions | **Promote** to normal routing trust |
| Same-IP contact shows ID flipping | **Hard ban** for ID-flip signal |
| Repeated malformed expensive requests | **Hard ban** |
| Repeated flood behaviour | **Hard ban** |

### Principle: Diversity as Preference, Not Hard Gate

- Use one good contact per IP per bucket as a **preference**, not a global rule.
- "Not preferred for routing" ≠ "completely rejected".
- Hard bans reserved only for the strongest abuse signals.

## Protocol Compatibility

All changes are local policy — no Kad packet changes, no wire format changes.

## Files

- `srchybrid/kademlia/utils/SafeKad.h` / `SafeKad.cpp`
- `srchybrid/kademlia/routing/RoutingZone.h` / `.cpp` — admission integration
- `srchybrid/kademlia/kademlia/Kademlia.h` / `.cpp` — verification integration

## Experimental Reference Implementation

**Status in `stale-v0.72a-experimental-clean`:** Core layered trust model implemented. `SafeKad.cpp/h` is present in `srchybrid/kademlia/utils/` with:
- `CSafeKad` class tracking `TrackedNode` (last ID, last change time, ID-verified flag), `ProblematicNode`, and `BannedIP` state
- `TrackNode(ip, port, id, bIDVerified, bBanOnVerifiedIdFlip)` — detects ID flipping; hard-bans if a verified ID flip is observed
- `TrackProblematicNode(ip, port)` — soft-penalises nodes with repeated failures
- `BanIP(ip)` — explicit hard ban (used for crypto abuse, flood)
- `IsBadNode(ip, port, id, kadVersion, ...)` — routing admission check combining ban, problematic, and ID-flip state
- `IsBanned(ip)` / `IsProblematic(ip, port)` — fast lookup paths
- Maps capped: 10,000 tracked nodes, 10,000 problematic nodes, 1,000 banned IPs
- `ShutdownCleanup()` clears maps with a stale-age sweep before exit

The CGNAT fix (multiple legitimately-different contacts per IP allowed) is implemented via the `bOnlyOneNodePerIP` parameter to `IsBadNode` — callers in routing pass `false` during contact admission, allowing multiple verified contacts from the same IP in CGNAT scenarios.

**Porting note:** `SafeKad.cpp/h` are new files. Integration point is `RoutingZone.cpp` contact addition — replace the current same-IP gate with `CSafeKad::IsBadNode(...)`. The integration is in commit `4798953` alongside FastKad.
