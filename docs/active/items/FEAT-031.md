---
id: FEAT-031
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/24
title: Auto-browse peers that expose remote shared-file inventories
status: OPEN
priority: Minor
category: feature
labels: [browse, clients, cache, ui, automation, networking]
milestone: ~
created: 2026-04-20
source: current `main` auto-browse implementation branch, live-network validation work, and user-requested future backlog refresh
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/24. This local document is retained as an engineering spec/evidence record.

## Summary

Add an Advanced opt-in feature that automatically detects compatible peers that
expose their shared-file inventory, browses those inventories using the
existing browse/share protocol, and hands successful results to the cache layer.

[FEAT-078](FEAT-078.md) owns the longer-term local database cache for
auto-browse results. This item owns the safe discovery, scheduling, and live
browse behavior.

## Intended Mainline Shape

- new Tweaks preference:
  - `AutoBrowseRemoteShares`
- background scheduler:
  - periodic sweep of known clients
  - bounded concurrency
  - cooldown-based retry policy
- cache handoff:
  - explicit result object for successful remote inventory snapshots
  - cooldown and expiry hints for the storage layer
  - no direct dependency on the final cache backend
- UI:
  - new `Cached Clients` tab
  - cached-only inspection path
  - manual live refresh path
- live validation lane:
  - isolated real-network auto-browse harness in `emulebb-build-tests`

## Constraints

- reuse the existing remote shared-files browse protocol
- do not introduce automatic download or queue side effects
- keep manual browse working independently of auto-browse cooldowns
- keep this feature opt-in and default-off

## Acceptance Criteria

- [ ] compatible remote clients can be auto-browsed in the background
- [ ] successful browse results are handed to a bounded cache interface
- [ ] cached inventories can be inspected through the new UI tab
- [ ] manual browse can supersede and refresh cached data
- [ ] isolated live-network automation can validate at least one real auto-browse success

## Notes

- This item is intentionally parked on a dedicated feature branch and is not
  merged into `main`.
- Current supporting live scenario defaults include:
  - P2P bind through `BindInterface=hide.me`
  - P2P `UPnP=1`
  - autoconnect through preferences only
  - fallback transfer bootstrap hash `28EAB1A0AB1B9416AAF534E27A234941`
  - rejection of `.exe` download candidates during fallback bootstrap

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- client-history data structures:
  [`ClientList.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientList.h#L319)
- persisted history and known-client map handling:
  [`ClientList.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientList.cpp#L2010)
- client-list UI columns and known-client display:
  [`ClientListCtrl.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientListCtrl.cpp#L864)
- remote shared-files browse entry points and history guards:
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6073)
- preference UI for remote shared files and client history:
  [`PPgMod.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/PPgMod.cpp#L748),
  [`PPgMod.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/PPgMod.cpp#L1338),
  [`PPgMod.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/PPgMod.cpp#L1734)

## eMuleBB Direction

The eMuleAI history model is useful, but eMuleBB should split it into smaller
steps: manual remote-browse stability, opt-in auto-browse scheduling, bounded
client-history notes, then local cache persistence under [FEAT-078](FEAT-078.md).
None of these steps should auto-queue downloads or expose cached inventories
through REST until privacy and retention rules are documented.
