---
id: FEAT-005
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/55
title: Kad — Restore network-change grace handling around routing persistence and probing
status: OPEN
priority: Minor
category: feature
labels: [kad, resilience, network-change, vpn, mobile]
milestone: ~
created: 2026-04-08
source: AUDIT-KAD.md (AUD_KAD_012)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/55. This local document is retained as an engineering spec/evidence record.

# FEAT-005 - Kad — Restore network-change grace handling around routing persistence and probing

## Summary

`eMuleAI` had a useful network-change grace period that the current target
dropped. When the local network interface changes (VPN connect/disconnect,
Wi-Fi roam, DHCP renewal, laptop sleep/wake), the current code may:

- Immediately start probing stale contacts with the old endpoint.
- Write a poor `nodes.dat` snapshot immediately after the rebind.
- Confuse "routing table is stale" with "routing table is empty".

This is particularly bad on:
- Mobile/laptop users (frequent interface churn)
- VPN users (endpoint changes on every connect)
- Dual-home machines (Wi-Fi ↔ Ethernet failover)

## Proposed Grace Handling

1. **Detect network-change events** — hook into Windows `NotifyAddrChange` or
   equivalent to detect local IP changes.
2. **Grace period** — after detecting a change, delay:
   - Routing table persistence writes (avoid overwriting good `nodes.dat`).
   - Active probing of existing contacts (avoid flooding stale contacts).
   - Bootstrap retriggers (give the new interface time to stabilise).
3. **Distinguish states in diagnostics**:
   - "Network unstable" (recent interface change, in grace period)
   - "Routing table empty" (normal cold start)
   - "Routing table stale" (contacts present but not yet reverified)

## Protocol Compatibility

This is local resilience policy — no Kad packet changes.

## Prior Art

`eMuleAI` implemented a version of this. The target should design a version
compatible with the current one-buddy architecture rather than porting directly.

## Files

- `srchybrid/kademlia/kademlia/Kademlia.h` / `.cpp` — bootstrap and routing state
- `srchybrid/kademlia/routing/RoutingZone.h` / `.cpp` — persistence gate
- `srchybrid/kademlia/utils/NodesDatSupport.h` / `.cpp` — save path gate
- New: network-change detection helper (Windows `NotifyAddrChange` wrapper)
