# MFC 0.8.0 — Performance & Async modernization (lane spec)

Status: proposal (no code yet). First specified `0.8.x` MFC lane content
(operator decision 2026-06-24). **Not** a `0.7.3` gate; opens on `main` only after
stable `0.7.3` and the `release/0.7.x` split.

Governs: [FUTURE-ROADMAP](../FUTURE-ROADMAP.md) (revived "Performance & Async" lane),
[SUITE-JOINT-ROADMAP](../SUITE-JOINT-ROADMAP.md). Companion design docs:
[Startup time-to-interactive](MFC-0.8.0-STARTUP-TIME-TO-INTERACTIVE.md),
[Network core thread](MFC-0.8.0-NETWORK-CORE-THREAD.md),
[Process() loop migration](MFC-0.8.0-PROCESS-LOOP-MIGRATION.md).

## Context

Operator decision 2026-06-20 revived the `0.8.x` MFC modernization line and left its
lane content "to be specified by the operator." This document specifies the **first
slice (0.8.0): startup performance, moving work off the UI thread, and async sockets.**
It reverses the old **Startup And Storage Performance** lane, which the FUTURE-ROADMAP
marked *Dropped* under the prior `0.7.x`-freeze framing.

Three coupled problems, confirmed against current `main`
(`repos/emulebb/srchybrid`):

1. **Slow time-to-interactive.** The heaviest startup costs run synchronously on the UI
   thread before the window is usable: `CSharedFileList` constructor does a full
   `FindSharedFiles(true)` disk scan (`Emule.cpp:1842`), `CKnownFileList::Init` reads
   known.met/cancelled.met (`Emule.cpp:1827`), and `CDownloadQueue::Init` scans every
   `*.part.met` (`EmuleDlg.cpp:2277`). Hashing/AICH/disk-I/O are already deferred to
   worker threads; the **loading/scanning** is not.
2. **Networking runs on the UI message pump.** `AsyncSocketEx.cpp` uses **WSAAsyncSelect**:
   every `FD_READ/WRITE/ACCEPT/CONNECT/CLOSE` is posted to a hidden message-only window and
   dispatched on the UI thread, where all packet parsing and `ProcessPacket` handling runs.
   The code even carries a standing comment that it "intentionally stays on WSAAsyncSelect
   until the broader async-socket transport replacement is scheduled" (`AsyncSocketEx.cpp:79`).
3. **The 100ms `Process()` loop is on the UI thread and coupled to #2.**
   `CUploadQueue::UploadTimer` (`UploadQueue.cpp:2538`) drives
   `downloadqueue/uploadqueue/clientlist/serverlist/knownfiles/Kad/listensocket`
   `Process()` every 100ms on the UI thread. They touch socket state with **no locks**
   precisely because the sockets are also on the UI thread. So Process() cannot cleanly
   leave the UI thread until the networking does.

**Intended outcome:** eMuleBB reaches an interactive window fast, and the networking +
Process() loops leave the UI message pump using the lowest-risk architecture available —
without changing eD2K/Kad wire behavior or dropping eMuleBB's REST controller surface.

## Decision: forward-port the proven WSAPoll network thread (not a from-scratch design, not IOCP-first)

The operator chose "dedicated network thread first, not full IOCP." That exact migration
**already exists, built and tested**, in the operator's own `v0.72a-broadband-dev`
lineage: `analysis/stale-v0.72a-experimental-clean/`. Its design docs
(`docs/ARCH-NETWORKING.md`, `docs/ARCH-THREADING.md`) and `RESUME.md` record that it:

- replaced `WSAAsyncSelect` + the helper window with a **dedicated `WSAPoll` network-thread
  backend** for TCP and UDP (new `CAsyncDatagramSocket` base for UDP);
- removed `WSAAsyncGetHostByName`, resolving source/server hostnames on worker threads;
- marshals UI list refreshes back to the UI thread via new `UM_PARTFILE_DISPLAY_UPDATE` /
  `UM_CLIENT_DISPLAY_UPDATE` messages, and UDP datagram processing via `UM_WSAPOLL_UDP_SOCKET`;
- builds `Debug|x64` + `Release|x64` and passes `111/111` shared tests.

So the network half of this lane is a **forward-port**, not a fresh design. WSAPoll is the
lowest-risk dedicated-network-thread bridge; **IOCP remains the documented later end-state**
(the experimental tree's FEAT_030), pursued only if profiling demands it.

### The eMuleBB-specific delta (why this is a port, not a copy)

The experimental tree *removed* the web server, REST, mbedTLS, SMTP, IRC, and proxy
support. **eMuleBB keeps the web server + `/api/v1`/`/api/v2` REST controller surface**,
which is core to the suite, plus the VPN-bind/proxy path. Consequences for the port:

- **Controller-surface read-locking is a new prerequisite** the reference never needed.
  REST/web handlers read `theApp.downloadqueue/uploadqueue/sharedfiles/serverlist/clientlist`
  without locks today; once Process()/sockets run off the UI thread those reads become data
  races. Reuse the existing `FEAT-068`/`FEAT-099` snapshot-worker pattern (immutable response
  records) as the crossing contract; do not hand live app objects to off-thread readers.
  *(The parallel [Lean lane](MFC-0.8.0-LEAN-REMOVAL-PLAN.md) switches REST to plaintext HTTP
  and drops mbedTLS (`REF-060`), so there is no TLS session state to also make thread-safe —
  this read-locking is the whole job.)*
- **Preserve the VPN egress-bind discipline** (interface-bound profiles, UPnP-over-VPN). The
  network thread must keep binding sockets exactly as today; this lane is about *where*
  readiness is serviced, not *how* sockets are bound.

## Scope of 0.8.0 (three areas, sequenced by risk)

1. **Startup time-to-interactive** — independent, lowest risk, highest visible win. Can
   land first and ship value even if the threading work slips.
2. **Network core thread** — the enabling change: forward-port the WSAPoll backend so
   socket readiness + packet processing leave the UI thread.
3. **Process() loop migration** — move the 100ms scheduling loop off the UI thread; largely
   a consequence of #2 once shared state is lock-protected / co-located.

## Proposed slices (engineering specs; not yet GitHub issues)

Per the FUTURE-ROADMAP promotion rule, a slice needs an `emulebb/emulebb` issue + project
item before implementation. These are the proposed `0.8.0` slices; numbers are assigned at
promotion time.

| Slice | Area | Summary | Risk |
|---|---|---|---|
| PERF-STARTUP-1 | Startup | Show interactive window before known.met / shared-scan / part.met load; move those loads to worker/time-sliced stages with progress. | Low |
| HYG-1 | Hygiene (prereq) | Retire the 2 MB static `GlobalReadBuffer`; `volatile`→`std::atomic` cross-thread flags; remove UI-thread `WaitForSingleObject(INFINITE)`. | Low |
| NET-1 | Network | Forward-port the WSAPoll TCP backend into `AsyncSocketEx`; remove helper window / `WSAAsyncSelect`. | High |
| NET-2 | Network | Forward-port `CAsyncDatagramSocket` + UDP/Kad dispatch (`UM_WSAPOLL_UDP_SOCKET`); worker-thread DNS. | High |
| NET-3 | Network | Controller-surface (REST/web) read-locking via the FEAT-068/099 snapshot pattern. | Medium |
| PROC-1 | Process | Move/co-locate the 100ms `Process()` loop off the UI thread; route UI side effects through `UM_*_DISPLAY_UPDATE`. | High |
| PROC-2 | Process | Kademlia processing thread isolation with internal routing-table locking. | Medium |

Dependency order: `HYG-1` → `NET-1` → `NET-2` → `NET-3` → `PROC-1` → `PROC-2`.
`PERF-STARTUP-1` is independent and may proceed in parallel.

## Definition of Done (per area)

**Startup time-to-interactive:**
- Main window is interactive (accepts input, paints tabs) before the shared-files scan,
  known.met, and part.met loads complete.
- The socket-startup ordering guarantee is preserved: listen/UDP sockets still start only
  after the download queue is loaded (avoids the documented LowID-on-exception hazard,
  `EmuleDlg.cpp:2274-2276`).
- `EMULEBB_HAS_STARTUP_DIAGNOSTICS` before/after per-stage µs baseline captured as evidence.

**Network core thread:**
- UI thread makes **zero** socket calls; all `OnReceive/OnSend/OnAccept/OnConnect/OnClose`
  run on the network thread.
- eD2K/Kad wire behavior unchanged: protocol-oracle packet diff (`packet_trace_diff.py`,
  key `(protocol_marker, opcode, payload_hex)`) shows no regression vs the `0.7.3` baseline.
- REST/web responses remain correct under concurrent transfer load (no torn reads, no
  crashes); VPN egress-bind + leak posture unchanged.

**Process() loop migration:**
- UI stays responsive (no main-pump stalls) under a large-profile load (hundreds of active
  uploads/downloads) where the 100ms loop previously blocked the UI.
- No UI/MFC control is touched from the network/Process thread except via PostMessage.

## Risk & rollback

- **Feature-flag the network thread** behind a preference so a regression reverts to the
  current UI-thread pump for one release. (The experimental tree did not need this because
  it shipped the migration outright; eMuleBB carries the REST surface and a live `0.7.x`
  user base, so a fallback is warranted for the first `0.8.x`.)
- Land `HYG-1` and `PERF-STARTUP-1` first — both are low-risk and independently valuable, so
  the lane delivers even if the transport port needs more soak time.
- Keep the experimental tree as the running reference: when behavior diverges, diff against
  its tested implementation before inventing a new fix.

## Measurement baseline

- **Startup:** the existing `EMULEBB_HAS_STARTUP_DIAGNOSTICS` build emits per-stage
  microsecond deltas in `OnStartupTimer` — use it for before/after evidence.
- **Wire parity:** the suite's `ed2k_packet_v1` diagnostics + `packet_trace_diff.py` /
  `diag_event_diff.py` (see [TEST-CAMPAIGN-ARCHITECTURE-PLAN](TEST-CAMPAIGN-ARCHITECTURE-PLAN.md))
  are the regression guard for "transport moved, behavior unchanged."
- **Responsiveness:** main-pump stall measurement under a synthetic large-profile load.

## Out of scope (this lane)

- Full IOCP transport (later `0.8.x`, profile-gated — experimental FEAT_030 end-state).
- IPv6 / µTP / NAT-PMP / dark mode and other Superseded-Lane items (stay parked).
- Any protocol/opcode/Kad-state change. Stock eD2K/Kad semantics stay intact.
- Removing the web server / REST / proxy as the experimental tree did — eMuleBB keeps them.
