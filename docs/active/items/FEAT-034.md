---
id: FEAT-034
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/62
title: Shared-files reload should stop blocking the UI on large trees
status: IN_PROGRESS
priority: Minor
category: feature
labels: [performance, shared-files, reload, threading, ui]
milestone: ~
created: 2026-04-20
updated: 2026-06-03
source: current `main` revalidation; `analysis\emuleai` and Xtreme comparison; filtered web-demand scan; 2026-05-27 senior C++ performance and I/O review
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/62. This local document is retained as an engineering spec/evidence record.

## Summary

Current `main` still handles `CSharedFileList::Reload()` synchronously. The current path
clears transient state and then immediately calls `FindSharedFiles(false)` on the caller
thread.

On large share trees, that remains a plausible UI-freeze path even after the startup and
Shared Files list improvements already landed under `FEAT-026`, `FEAT-027`, and
`FEAT-028`.

## Current Mainline Evidence

Before the first FEAT-034 slice, `srchybrid/SharedFileList.cpp` had this narrow shape:

- clear keywords, queues, and transient lookup state
- call `FindSharedFiles(false)` directly from `Reload()`
- reload the output control only after the synchronous scan returns

So the expensive directory walk still happens on the immediate reload path.

## Landed Scope

The first implementation slice landed on `main` on 2026-04-21:

- `f5da4c5` — app-lifetime shared-file hash worker replaces per-file shared hash threads
- `7f5b207` — full shared reloads are deferred/coalesced while shared hashing is active, Shared Files UI refresh is throttled during active hashing, and startup profiling now separates `ui.shared_files_ready` from `ui.shared_files_hashing_done`
- `0aaadbe` — shared reload deferral policy is exposed through seams for native tests
- `f138856` in `repos\emulebb-build-tests` — native seam coverage and live-profile summary parsing were updated for the new readiness/hash-drain split

The follow-up hardening slice landed after review:

- `7cbad68` — startup-deferred Shared Files list reloads now stay pending while shared hashing is active and flush only after hash drain
- `85fcaf6` — the shared hash worker waits for the UI thread to consume each posted completion before starting the next job
- `ff254ab` — shared hash completion posting retries while the UI is still alive before discarding a result during shutdown/error paths
- `67d85de` and `306bb63` in `repos\emulebb-build-tests` — native seam coverage for the deferred-list reload gate and worker backpressure
- `f711688` in `repos\emulebb-build-tests` — live startup-profile coverage now fails if the Shared Files list rebuilds repeatedly during hash drain

The shutdown and startup-cache completion hardening slices landed on 2026-04-23
and 2026-04-24:

- `2c44341` bounds shared hash worker shutdown waits
- `02096ab` purges startup cache after interrupted hashing
- `0e7e16d` bounds startup-cache save shutdown waits
- `5e3e924`, `5223585`, `f829eb3`, and `fd3a861` retain and retry shared hash
  completions in a bounded backlog and centralize startup-cache save completion
  policy
- `58d3cfe` skips shutdown startup-cache saves after interrupted hashing
- `TEST-034` commits through `cac7b93` add native seam coverage plus live
  Shared Files UI stress lanes for interruption, warm relaunch, repeated
  cycles, many-file cases, and shutdown startup-cache skip behavior

The targeted long-path recursive live scenario now shows one final coalesced list rebuild during shared hash drain instead of repeated periodic reloads. This reduces the startup and reload churn caused by hash-thread creation and repeated list rebuilds. It does **not** yet move the directory enumeration pass itself fully off the UI thread, so this item remains `In Progress` rather than `Done`.

The separate shared-root watcher/live recursive sync track has now landed and
is tracked as done in `FEAT-038`. That does not close this item: the remaining
FEAT-034 concern is the manual reload/hash path, especially blocking filesystem
I/O during shared hashing and shutdown.

## Remaining Work

The still-open part is narrower now: blocking filesystem reads during shared
hashing can still fall into the existing timeout/leak-and-exit shutdown path if
a read wedges hard enough. Add diagnostics or cancellation hardening there
before treating FEAT-034 as complete.

The large-list scope is also intentionally limited to Shared Files. Current
evidence does not justify a generic list-control substrate across Transfers,
Uploading, Queue, Search Results, or Known Clients. Those surfaces can keep their
current shape unless profiling or a concrete bug shows a local problem. Focused
improvements for those lists should stay in their owning items, such as upload
queue/list overhead in `REF-053`, download queue instrumentation in `REF-054`,
and downloads filtering in `FEAT-101`.

Shared Files remains different because it is the persistent large-library view:
operator profiles can keep tens of thousands of complete files visible, with
hashing, publishing, status labels, aggregate counters, sorting, and refresh
work all competing for the same UI path.

The next implementation direction should be background directory enumeration
with immutable scan results:

- add a long-path-safe `FindFirstFileEx` helper using `FindExInfoBasic` and
  `FIND_FIRST_EX_LARGE_FETCH`, with fallback to the current `FindFirstFile`
  wrapper when unsupported or unsuitable
- enumerate shared roots off the UI thread into a candidate list
- keep path filtering and share-policy decisions deterministic
- apply additions/removals to `CSharedFileList` on the owning app/UI path
- queue hashing work only after the scan result has been validated
- keep the existing deferred/coalesced reload behavior while a scan or hash
  drain is active

Workers must not mutate `CSharedFileList`, `CSharedFilesCtrl`, upload state, or
KnownFile maps directly.

## Comparison Notes

- `analysis\emuleai` keeps a dedicated search worker thread alive and resets/coalesces
  work on reload
- the focused Xtreme archive also shows a long-standing off-thread/shared-scan direction

The branch has since added its own narrower monitored-root watcher model under
`FEAT-038`, but this item intentionally remains about manual reload and hashing
responsiveness, not broader auto-share policy.

## Scope Constraints

This item stays intentionally narrow:

- target manual reloads and similar explicit shared-tree rescans
- allow a bounded worker or coalesced background scan
- do not change share policy, duplicate policy, or startup cache ownership
- keep behavior close to stock outside responsiveness improvements
- do not build a broad virtual-list framework for unrelated lists
- keep Uploading, Queue, Downloads, Search Results, and Known Clients on their
  current list-control shape unless a measured, list-local bottleneck appears

## Shared Files UI Refresh Scope

The Shared Files list should be the only large-list UI hardening target for this
item. The goal is to make large-library display and status updates predictable,
not to redesign every list surface.

Candidate follow-up work:

- ensure every Shared Files list refresh/update path honors
  `DesktopUiRefreshIntervalMs`
- avoid resorting unless a sort-relevant displayed field changed or the user
  requested a new sort
- keep status-label updates independent from full list repaint where practical
- cache or rate-limit expensive aggregate display values such as total shared
  size, hashing progress, eD2K published count, Kad published count, requested
  count, and active upload count
- refresh only affected rows or visible rows where the existing control model
  can support it without a broad rewrite
- add diagnostics under a flag for file count, visible row count, refresh
  duration, sort duration, status-label duration, and scan/hash/publish phase
  counters

Non-goals for this item:

- no broad eMuleAI-style virtual-list import
- no shared abstraction across all list controls
- no upload/download/search queue policy changes
- no unrelated UI refresh work outside Shared Files unless tied to a concrete
  bug or existing owning item

## Web-Demand Fit

Recent web signals still point much more strongly toward remote control/API work and
networking friendliness than toward large new product features. Performance pain around
big queues and big trees remains a recurring complaint, but not one that justifies a big
subsystem rewrite on this branch.

That is why `FEAT-034` is kept as a small, low-priority responsiveness item rather than a
broader `eMuleAI` shared-files feature import.

## Acceptance Criteria

- [ ] manual shared-files reload returns control quickly on large trees
- [ ] Shared Files list refresh/update paths honor `DesktopUiRefreshIntervalMs`
- [ ] Shared Files status-label and aggregate-counter updates do not force full
      list repaint when row data did not change
- [ ] Shared Files sort work is skipped unless the active sort fields can have
      changed or the user requests sorting
- [ ] diagnostics can explain Shared Files refresh, sort, status-label,
      scan/hash, and publish-counter costs on large-library profiles
- [x] repeated reload requests coalesce instead of starting overlapping scans while hashing is active
- [ ] directory enumeration can run in the background and produce an immutable
      candidate list
- [ ] large-fetch directory enumeration is covered for long paths, UNC paths,
      empty directories, inaccessible directories, and large local/remote
      directory scans
- [x] targeted long-path live profile converges to the expected final visible Shared Files rows after hash drain
- [ ] general final shared-file results converge to the same set as the synchronous path across broader reload scenarios
- [x] uploads, share state, and GUI counters remain stable while shared hashes drain in the background
- [x] watcher/live recursive sync is tracked separately in `FEAT-038`
- [x] unrelated lists are explicitly excluded from broad large-list substrate
      work unless their owning item identifies a measured local problem
