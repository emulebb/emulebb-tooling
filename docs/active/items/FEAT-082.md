---
id: FEAT-082
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/31
title: Virtualize high-volume downloads, search results, and client-history lists
status: OPEN
priority: Minor
category: feature
labels: [ui, performance, lists, downloads, search, clients, emuleai]
milestone: post-beta-0.7.3
created: 2026-05-24
source: eMuleAI v1.4 release notes and `analysis\emuleai` list-control comparison
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/31. This local document is retained as an engineering spec/evidence record.

## Summary

Extend the high-volume list-performance work beyond the already-hardened Shared
Files view. eMuleAI's release notes and source show significant attention to
large Download, Search Results, and Known Clients histories. eMuleBB already
has stale-row guards and the Shared Files list improvements, but the remaining
large-profile UI surfaces should still be reviewed for rebuild, resort, and
full-row churn.

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- list-control base support:
  [`MuleListCtrl.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/MuleListCtrl.h#L533)
- download-list refresh and heavy-list behavior:
  [`DownloadListCtrl.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/DownloadListCtrl.cpp#L735)
- search-result list refresh behavior:
  [`SearchListCtrl.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/SearchListCtrl.cpp#L496)
- known-client list behavior:
  [`ClientListCtrl.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientListCtrl.cpp#L1225)
- client-history refresh model that avoids unnecessary sort-impact churn:
  [`ClientList.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientList.h#L319)
  and
  [`ClientList.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientList.cpp#L2010).

## Intended Shape

- Audit Downloads, Search Results, Known Clients, Downloading Clients, Uploads,
  Queue, Servers, and Kad list controls against large-profile traces.
- Prefer narrow incremental refresh, dirty-row tracking, and sort-impact checks
  over broad framework replacement.
- Avoid introducing persisted client history as a hidden dependency of list
  virtualization. Persistence belongs to [FEAT-043](FEAT-043.md),
  [FEAT-031](FEAT-031.md), and [FEAT-078](FEAT-078.md).
- Preserve existing stale-row safety fixes. Performance work must not re-open
  dangling pointer/list item bugs.

## Scope Constraints

- Do not change network behavior, transfer scheduling, or peer scoring.
- Do not require dark mode, DPI work, or CShield to land first.
- Do not change list column defaults as part of this item unless a specific
  high-volume test shows the column itself causes the performance issue.
- Use the public heavy-profile monitor harness before and after each slice.

## Acceptance Criteria

- [ ] Downloads and Search Results can refresh under heavy profiles without
      periodic full-list rebuilds where incremental refresh is sufficient.
- [ ] Known Clients refresh avoids resorting when non-sort-affecting fields
      change.
- [ ] UI refresh interval preferences continue to cap list update frequency.
- [ ] Large-profile traces show reduced UI-thread CPU during list refreshes.
- [ ] Stale-row regression coverage remains green for every touched list.
