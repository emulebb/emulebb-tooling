# MFC 0.8.0 — Process() loop migration (design doc)

Status: proposal (no code yet). Slices `PROC-1/2` of the
[Performance & Async lane](MFC-0.8.0-PERF-ASYNC-PLAN.md). **Depends on**
[Network core thread](MFC-0.8.0-NETWORK-CORE-THREAD.md) landing first.

## Context

The 100ms `CUploadQueue::UploadTimer` (`UploadQueue.cpp:2538-2671`) is eMuleBB's heartbeat.
On the UI thread it runs, per tick: `uploadqueue->Process()` and `downloadqueue->Process()`
every 100ms, and every ~1s `clientcredits/serverlist/knownfiles/friendlist/clientlist/
sharedfiles->Process()`, `Kademlia::CKademlia::Process()`,
`serverconnect->TryAnotherConnectionRequest()`, and `listensocket->UpdateConnectionsStatus()`
(call tree confirmed by the experimental tree's `ARCH-THREADING.md` §2.1). Under a
large-profile load this scheduling work blocks the UI message pump.

Critically, this loop touches the same client/queue/socket state the socket callbacks touch,
**without locks** — which is only safe because both run on the UI thread today. That is why
this slice depends on the network core thread: the safe way to move `Process()` off the UI
thread is to put it where the sockets now live.

## Approach: co-locate Process() with the sockets

Once [NET-1/2](MFC-0.8.0-NETWORK-CORE-THREAD.md) move socket servicing to the network
thread, run the 100ms `Process()` loop **on that same network thread**. This preserves the
long-standing "sockets and Process share state without locks" invariant unchanged — the two
remain single-threaded relative to each other — but relocates the pair off the UI thread.
This avoids the deadlock-prone fine-grained locking that a separate Process thread would
force across `clientlist`/`downloadqueue`/`uploadqueue` and the packet handlers.

The experimental tree's `ARCH-THREADING.md` §A0.9 reaches the same conclusion: a network
thread "only helps if protocol processing moves with it," and the model worth implementing is
the one where the network thread owns readiness **and** the protocol/scheduling callbacks —
not the one that marshals every callback back to the UI thread.

## What must move and what must not

- **Move to the network thread:** the `UploadTimer` driver and the `Process()` calls it makes
  (`uploadqueue`, `downloadqueue`, `clientlist`, `serverlist`, `knownfiles`, `friendlist`,
  `clientcredits`, `sharedfiles`, `serverconnect` retry, `listensocket` status).
- **Route UI side effects through PostMessage:** anywhere `Process()` currently refreshes a
  list control or stats view, replace the direct call with the marshaling messages the
  network port already introduces (`UM_PARTFILE_DISPLAY_UPDATE`, `UM_CLIENT_DISPLAY_UPDATE`,
  and the existing `TM_*`/`UM_*` set). The reference already removed direct list-control
  refreshes from the socket/upload/listen paths for this reason.
- **Keep on their own threads (unchanged):** `UploadBandwidthThrottler` (already off-thread,
  own locks), `CPartFileWriteThread` / `CUploadDiskIOThread` (IOCP disk I/O), hashing/AICH.
- **Controller surface:** REST/web reads of the lists `Process()` mutates must use the
  snapshot/lock contract from [NET-3](MFC-0.8.0-NETWORK-CORE-THREAD.md). This is the same
  boundary, not a second one.

## PROC-2 — Kademlia thread isolation

`Kademlia::CKademlia::Process()` mixes routing-table maintenance, zone timers, UPnP refresh,
and firewall checking on the 1s tick. Per `ARCH-THREADING.md` §A4, give Kad its own cadence
(on the network thread, or a dedicated thread) with:

- internal locking on the routing table / search list (partially present via
  `CMutex m_mutSync`);
- source-find results posted to the download queue via the safe marshaling path;
- `RefreshUPnP()` and any UI-touching call converted to PostMessage rather than a direct call.

Keep this a *second* slice after `PROC-1` so the basic loop relocation is validated before
Kad cadence changes.

## Startup-ordering note

The experimental tree also found a startup race worth carrying: crash-recovery part-file
hashing must be queued **before** `CAICHSyncThread` starts its background AICH backfill, or
the recovery hash stalls behind the backfill claiming the global hash lane (`RESUME.md`). If
the [startup slice](MFC-0.8.0-STARTUP-TIME-TO-INTERACTIVE.md) reorders startup loads, preserve
this ordering.

## Definition of Done

- The 100ms `Process()` loop no longer runs on the UI thread.
- UI stays responsive (no measurable main-pump stall) under a large-profile load (hundreds of
  active uploads/downloads) where it previously stalled.
- No UI/MFC control is touched from the network/Process thread except via PostMessage.
- Wire/scheduling parity unchanged vs the `0.7.3` baseline (`packet_trace_diff.py` +
  `diag_event_diff.py`).

## Verification

- Synthetic large-profile load; measure UI main-pump stall before/after (input latency or a
  pump-gap probe).
- `diag_event_v1` scheduling diff vs the MFC `0.7.3` baseline — per-decision scheduling must
  not drift.
- Confirm no off-thread UI-control access (debug assert / instrumentation) across a soak run.
