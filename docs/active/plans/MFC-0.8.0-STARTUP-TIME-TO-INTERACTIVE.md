# MFC 0.8.0 — Startup time-to-interactive (design doc)

Status: proposal (no code yet). Slice `PERF-STARTUP-1` of the
[Performance & Async lane](MFC-0.8.0-PERF-ASYNC-PLAN.md). Independent of the network /
Process() work; may land first. Canonical backlog item: **`REF-058`** (async known-file /
shared-file startup load; milestone `0.8.0`) — this doc is its design. Related: `REF-057`
(GeoLocation MMDB deferral — investigated and reverted, kept as a finding).

## Context

The window does not become interactive until well into a synchronous load chain. The
heaviest costs run on the UI thread before the user can do anything. Hashing, AICH, and
disk-I/O are already on worker threads; the **loading/scanning** of on-disk state is the
remaining blocker. This slice makes the window interactive first and moves the loads off
the critical path, reusing the startup state machine and worker-thread patterns that
already exist.

## Current startup shape (against `main`)

Two phases on the UI thread:

**Phase A — `CemuleApp::InitInstance` object construction (`Emule.cpp:1812-1920`), synchronous:**

| Cost | Site | Note |
|---|---|---|
| `CSharedFileList` ctor → `FindSharedFiles(true)` full disk scan | `Emule.cpp:1842` → `SharedFileList.cpp:963/1037` | **Heaviest.** Enumerates all share dirs + startup cache load. |
| `CKnownFileList::Init` (known.met + cancelled.met) | `Emule.cpp:1827` → `KnownFileList.cpp:168` | Hundreds of ms on large shares. |
| `CClientCreditsList::LoadList` (clients.met) | `Emule.cpp:1857` | |
| `CIPFilter::LoadFromDefaultFile` (conditional) | `Emule.cpp:1878` → `IPFilter.cpp` | Only if enabled at startup. |
| `CGeoLocation::Load` (GeoIP db) | `Emule.cpp:1899` | |
| `CPreferences::Init` (config files) | `Emule.cpp:1702` | |

**Phase B — `CemuleDlg::OnStartupTimer` state machine (`EmuleDlg.cpp:2219-2408`):** already a
staged, message-pumped state machine (`UM_STARTUP_NEXT_STAGE`) with a `LifecycleProgressDlg`.
Its heavy step is status=4, which calls `theApp.downloadqueue->Init()`
(`EmuleDlg.cpp:2277` → `DownloadQueue.cpp:631`, the `*.part.met` scan) and only **then**
starts the listen + UDP sockets and sets `APP_STATE_RUNNING` (`EmuleDlg.cpp:2324`).

So a deferral mechanism already exists — the work is to extend it and to move the Phase A
loads out of `InitInstance` so the window shows before they finish.

## Approach

1. **Show the window before the Phase A loads.** Move `CKnownFileList`, `CSharedFileList`
   initial scan, and `CClientCreditsList`/`CGeoLocation` loads out of the synchronous
   `InitInstance` construction and into either (a) additional `OnStartupTimer` stages, or
   (b) a dedicated startup-load worker thread that posts completion back to the UI, using
   the **same pattern already proven** for `CSharedFileHashThread`, `CAICHSyncThread`,
   `CPartFileWriteThread`. Construct the objects empty; populate them off the critical path.
2. **Keep the existing staged loader as the spine.** The `OnStartupTimer` /
   `UM_STARTUP_NEXT_STAGE` machine and `LifecycleProgressDlg` already give a responsive,
   progress-reporting loader. Add stages / worker hand-offs rather than introducing a new
   mechanism. **`LifecycleProgressDlg` is on the keep-list** — the parallel
   [Lean lane](MFC-0.8.0-LEAN-REMOVAL-PLAN.md) removes only the *legacy splash* (`REF-025`),
   which must not be confused with this lifecycle loader. Confirm during REF-025 that
   "splash" is the legacy bitmap path, not `LifecycleProgressDlg`.
3. **Preserve the socket-startup ordering guarantee.** Listen/UDP socket creation must
   continue to happen only after the download queue is loaded. The existing code documents
   why: an unhandled exception in `CDownloadQueue::Init` makes MFC silently skip socket
   creation and the client gets a LowID (`EmuleDlg.cpp:2274-2276`). Whatever loads move to a
   worker, the **socket-start step stays gated on download-queue-loaded**.
4. **Gate functionality that needs loaded state.** Until shared files / known files finish
   loading, surface a clear "loading…" state in the relevant tabs rather than presenting an
   empty list as authoritative (so a user cannot, e.g., act on shared files before the scan
   completes). The status-bar progress already updated by the loader is the hook.

## Interaction with the Track B hygiene slice

This slice does **not** require the off-UI-thread socket work. But if a startup load is moved
to a worker thread, any cross-thread flags it sets must use `std::atomic`, not bare
`volatile` (the hygiene `HYG-1` rule). Where a startup load posts results to the UI, use the
existing `TM_*`/`UM_*` PostMessage pattern (e.g. the hashing thread's
`TM_FINISHEDHASHING`), never a direct UI-control write from the worker.

## Definition of Done

- Main window is interactive (input + tab paint) before the shared-files scan, known.met,
  and part.met loads complete.
- Socket startup still occurs only after download-queue load (LowID hazard preserved).
- Tabs that depend on not-yet-loaded state show a loading indicator rather than a misleading
  empty list.
- `EMULEBB_HAS_STARTUP_DIAGNOSTICS` per-stage µs baseline captured before/after; the
  time-to-`APP_STATE_RUNNING` (or a new time-to-first-paint marker) improves measurably on a
  large profile.

## Verification

- Build the `EMULEBB_HAS_STARTUP_DIAGNOSTICS` configuration; capture the per-stage timing
  log on a large synthetic profile (many shared files + many part files) before and after.
- Manual: confirm the window paints and accepts input while a large share is still scanning;
  confirm no LowID regression on a normal connect after restart.
- Confirm graceful behavior when known.met / part.met load throws (no skipped socket start).
