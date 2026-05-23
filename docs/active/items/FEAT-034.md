---
id: FEAT-034
title: Shared-files reload should stop blocking the UI on large trees
status: IN_PROGRESS
priority: Minor
category: feature
labels: [performance, shared-files, reload, threading, ui]
milestone: ~
created: 2026-04-20
updated: 2026-04-26
source: current `main` revalidation; `analysis\emuleai` and Xtreme comparison; filtered web-demand scan
---

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

The next implementation direction should be background directory enumeration
with immutable scan results:

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

## Web-Demand Fit

Recent web signals still point much more strongly toward remote control/API work and
networking friendliness than toward large new product features. Performance pain around
big queues and big trees remains a recurring complaint, but not one that justifies a big
subsystem rewrite on this branch.

That is why `FEAT-034` is kept as a small, low-priority responsiveness item rather than a
broader `eMuleAI` shared-files feature import.

## Acceptance Criteria

- [ ] manual shared-files reload returns control quickly on large trees
- [x] repeated reload requests coalesce instead of starting overlapping scans while hashing is active
- [ ] directory enumeration can run in the background and produce an immutable
      candidate list
- [x] targeted long-path live profile converges to the expected final visible Shared Files rows after hash drain
- [ ] general final shared-file results converge to the same set as the synchronous path across broader reload scenarios
- [x] uploads, share state, and GUI counters remain stable while shared hashes drain in the background
- [x] watcher/live recursive sync is tracked separately in `FEAT-038`
