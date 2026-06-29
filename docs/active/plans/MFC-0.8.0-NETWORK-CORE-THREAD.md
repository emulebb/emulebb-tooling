# MFC 0.8.0 — Network core thread (design doc)

Status: proposal (no code yet). Slices `NET-1/2/3` of the
[Performance & Async lane](MFC-0.8.0-PERF-ASYNC-PLAN.md). Enables the
[Process() loop migration](MFC-0.8.0-PROCESS-LOOP-MIGRATION.md).

## Context

eMuleBB services all socket events on the UI message pump via **WSAAsyncSelect** + a hidden
helper window (`AsyncSocketEx.cpp`). Packet parsing and `ProcessPacket` handling for eD2K
TCP, eD2K UDP, and Kad UDP all run on the UI thread. This couples networking throughput to
UI work and vice-versa, and blocks moving the `Process()` loop off the UI thread.

**This is a forward-port, not a fresh design.** The operator's own `v0.72a-broadband-dev`
lineage already built and tested the dedicated-network-thread migration the operator chose.
The reference implementation and its design rationale live in
`analysis/stale-v0.72a-experimental-clean/`:

- `docs/ARCH-NETWORKING.md` §1–§2 — the post-migration socket hierarchy and the shared
  `WSAPoll` backend.
- `docs/ARCH-THREADING.md` §A0 — the WSAPoll backend shape: poll-loop sketch, the
  `FD_*`→`WSAPOLLFD::revents` mapping table, the connect-completion/close-ordering rules, and
  the **write-interest arming rule** (arm `POLLOUT` only while a connect is pending or the
  send queue is non-empty — the single rule that keeps the poll loop from spinning).
- `RESUME.md` — closeout: live socket ownership fully off `CAsyncSocket`, builds
  `Debug|x64`+`Release|x64`, `111/111` tests pass.

Treat those documents as the design basis for this doc; the sections below record the
**eMuleBB-specific** port plan and deltas, not a re-derivation.

## Why WSAPoll (and not IOCP) for 0.8.0

WSAPoll is the smallest Windows-native step off helper-window dispatch: it keeps the classic
`socket`/`connect`/`send`/`recv`/`accept` style and the existing `CAsyncSocketEx` callback
shape, but removes the `HWND` + `WM_SOCKETEX_NOTIFY` + UI-pump dependency. It is an `O(n)`
readiness scan and not the final high-scale design — **IOCP stays the documented later
end-state** (experimental FEAT_030). Choosing WSAPoll matches the operator's
"dedicated network thread first, not full IOCP" decision and reuses a tested implementation.

## Port plan

### NET-1 — TCP backend (`AsyncSocketEx`)
- Replace `WSAAsyncSelect(...)` + `CAsyncSocketExHelperWindow` with a dedicated network
  thread owning a `WSAPOLLFD[]` set, a parallel `CAsyncSocketEx*` table, and a command queue
  (add socket / remove socket / change interest mask / stop).
- Keep the public API (`Create`, `Connect`, `AsyncSelect`, `Send`, `Receive`, `Close`) and
  the virtual callbacks (`OnReceive/OnSend/OnConnect/OnAccept/OnClose`). `AsyncSelect` becomes
  "update desired interest on the socket object + enqueue a command to the poll thread"; it
  must no longer call WinSock notification APIs.
- Surface the readiness bookkeeping that `WSAAsyncSelect` hid inside WinSock
  (`connectPending`, `wantWrite`/send-queue-non-empty, deferred read/write bits formerly in
  `m_nPendingEvents`, `isListening`, `closeNotified`) on the socket/backend record. See
  `ARCH-THREADING.md` §A0.8.
- Reuse the existing thread-local helper-window TLS *mechanism* for the network thread's
  per-thread state (the mechanism is fine; only WSAAsyncSelect is being removed).

### NET-2 — UDP backend + Kad dispatch
- Bring over `AsyncDatagramSocket.cpp/.h` (`CAsyncDatagramSocket`) as the UDP base, with
  `CClientUDPSocket` and `CUDPSocket` riding the same `WSAPoll` backend.
- Marshal UDP datagram processing back to the app thread via `UM_WSAPOLL_UDP_SOCKET` so the
  existing eMule/Kad UDP protocol handlers keep their current thread affinity (the reference
  does exactly this).
- Carry over the worker-thread DNS: `CDownloadQueue` resolves source hostnames on its
  resolver worker and drains completions in `Process()`; `CUDPSocket` resolves server/dynIP
  hostnames on its own worker. Remove the `WSAAsyncGetHostByName` / `WM_HOSTNAMERESOLVED`
  path.

### NET-3 — controller-surface read-locking (eMuleBB-only delta)
- The reference tree removed the web server; **eMuleBB keeps the web server + `/api/v1`/
  `/api/v2` REST**. Its handlers read `theApp.downloadqueue/uploadqueue/sharedfiles/
  serverlist/clientlist` without locks. Once `OnReceive`/`Process()` run off the UI thread,
  those reads race.
- Crossing contract: build immutable response snapshots via the existing
  `FEAT-068`/`FEAT-099` snapshot-worker pattern; never hand a live app object to an
  off-thread reader. Acquire a lock for the snapshot-collection phase, release before
  response assembly.
- **Note (Lean lane interaction):** the [Lean removal lane](MFC-0.8.0-LEAN-REMOVAL-PLAN.md)
  switches REST to **plaintext HTTP** (mbedTLS dropped, `REF-060`) bound local-only. That
  removes the per-connection TLS state from the listener, which *simplifies* this off-thread
  read-locking — there is no TLS session/handshake state to also make thread-safe.

## UI ↔ network-thread boundary

- **UI updates from the network thread** go through PostMessage only. The reference already
  added `UM_PARTFILE_DISPLAY_UPDATE` and `UM_CLIENT_DISPLAY_UPDATE` to marshal `CPartFile` /
  `CUpDownClient` list refreshes back to the UI thread and removed direct list-control
  refreshes from the socket/upload/listen paths — port both messages and that discipline.
- **Throttler interaction is unchanged:** `UploadBandwidthThrottler` is already its own
  thread with `queueLocker`/`tempQueueLocker`/`sendLocker` and a fixed lock order
  (queueLocker → tempQueueLocker → sendLocker; `sendLocker` released before returning on
  `WSAEWOULDBLOCK`). Preserve that order; the network thread participates as the old UI
  thread did.
- **Disk I/O stays on its existing IOCP worker threads** (`CPartFileWriteThread`,
  `CUploadDiskIOThread`). The network thread must not block on disk.

## Track B hygiene prerequisites (`HYG-1`, gating)

These are correctness gates once socket processing is off the single UI thread:

- **Retire the 2 MB static `GlobalReadBuffer`** (`EMSocket.cpp`). It is only safe today
  because all `OnReceive` calls are serialized on the UI thread; with a network thread it is
  a buffer-aliasing bug. Replace with a per-socket or thread-local receive buffer.
- **`volatile`→`std::atomic`** for cross-thread flags (per `ARCH-THREADING.md` §4.5/§7.1;
  notably `m_bPreviewing`, `m_bRecoveringArchive`).
- **Remove UI-thread `WaitForSingleObject(INFINITE)`** (`CreditsDlg.cpp`,
  `HttpDownloadDlg.cpp`) — these freeze the pump and become worse under the new model.

## Invariants (must hold)

- UI thread makes **zero** socket calls after NET-1/2 land.
- No UI/MFC control touched from the network thread except via PostMessage.
- eD2K/Kad wire behavior byte-identical: no opcode/packet/Kad-state change.
- VPN egress-bind discipline preserved — sockets bind exactly as today (interface-bound
  profiles, UPnP-over-VPN); only readiness servicing moves.
- Feature-flagged: a preference reverts to the WSAAsyncSelect UI-pump path for one release.

## Out of scope

- IOCP overlapped backend (later `0.8.x`, profile-gated; experimental FEAT_030 end-state).
- IPv6 / µTP transport (parked).

## Proxy removal (handled in the Lean lane, converges with the reference)

SOCKS/proxy support is **removed** in the [Lean removal lane](MFC-0.8.0-LEAN-REMOVAL-PLAN.md)
(`REF-051`), which converges eMuleBB with the reference tree (it removed proxy *during* its
WSAPoll migration) and **simplifies this port** — the `CAsyncProxySocketLayer` chain in
`EMSocket.cpp` goes away rather than needing to ride the new backend. Preserve only the
**VPN-bind / egress-pin** path (interface-bound profiles, UPnP-over-VPN); that is a separate
concern from the SOCKS proxy and stays. Sequence `REF-051` with/before NET-1.

## Verification

- **Wire parity:** `EMULEBB_ENABLE_PACKET_DIAGNOSTICS` `ed2k_packet_v1` dump diffed with
  `packet_trace_diff.py` (key `(protocol_marker, opcode, payload_hex)`) against the `0.7.3`
  baseline — expect match/payload-diff clean. `diag_event_diff.py` for scheduling/kad_udp.
- **Off-UI-thread proof:** instrument/assert that no socket call originates on the UI thread
  on a test build (the reference's closeout criterion).
- **REST under load:** drive transfers + concurrent REST polling; assert correct responses,
  no torn reads, no crash. Confirm VPN leak posture unchanged with the bound-leak test.
- **Soak:** the reference flags WSAPoll soak/stress as the remaining hardening; run a
  multi-hour large-peer-count session before flipping the feature flag default on.
