---
id: FEAT-018
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/60
title: µTP (Micro Transport Protocol) transport layer — CUtpSocket / libutp
status: OPEN
priority: Minor
category: feature
labels: [network, utp, transport, congestion-control, libutp]
milestone: ~
created: 2026-04-10
source: eMuleAI (CUtpSocket.cpp/h, UtpSocket attribution to David Xanatos / NeoLoader, 2013/2026)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/60. This local document is retained as an engineering spec/evidence record.

## Summary

µTP (Micro Transport Protocol, also known as uTorrent Transport Protocol) is a UDP-based
transport protocol designed to provide reliable, ordered delivery with congestion control
that is friendlier to the network than TCP. It is the transport used by BitTorrent for
"bandwidth management" — it backs off under load while TCP does not, reducing latency on
shared connections.

eMuleAI implements µTP via `CUtpSocket` (a `CAsyncSocketExLayer` subclass) backed by
**libutp** (Bram Cohen's reference µTP library, used by BitTorrent / qBittorrent). This
allows eMule connections to use µTP in place of raw TCP where both peers support it.

## eMuleAI Reference Implementation

**Source files in `eMuleAI/`:**
- `CUtpSocket.cpp` / `CUtpSocket.h` — the socket layer wrapper (~400+ lines)
- `eMuleAI/Buffer.cpp` / `Buffer.h` — auxiliary byte-buffer abstraction used by CUtpSocket
- Dependency: `libutp/include/libutp/utp.h` — libutp external library

**Architecture:**

`CUtpSocket` inherits `CAsyncSocketExLayer`, slotting into the existing layered socket model
alongside `CEncryptedStreamSocket`. It overrides `Create`, `Connect`, `Receive`, `Send`,
`Close`, and `GetPeerName`.

Key runtime details:
- Uses two `CCriticalSection` locks: `g_utpSocketsLock` (socket set), `g_utpRuntimeLock`
  (libutp API serialization)
- MTU discovery via `GetBestInterfaceEx` + `GetIpInterfaceEntry` (IP Helper API, runtime-loaded)
- Peer endpoint hinting via `ExpectPeer()` for inbound accept matching
- Multiple libutp context tracking for multi-context environments
- Socket cap: `kMaxUtpSockets = 2048`
- High-resolution timing via `QueryPerformanceCounter`

**Dynamic MTU query:** `CUtpSocket.cpp` implements `QueryMtuForPeer()` using `GetBestInterfaceEx`
and `GetIpInterfaceEntry` loaded at runtime from `iphlpapi.dll`. Falls back to a conservative
MTU if the query fails.

## Why This Matters

For eMule users on shared connections (home routers, CGNAT, shared ISP infrastructure),
eMule's TCP connections currently compete aggressively with other traffic (web browsing,
video streaming). µTP would make eMule a "background" protocol, dramatically reducing
latency impact on the shared connection while maintaining throughput when the network is idle.

This is the single networking improvement most likely to improve user experience on modern
home networks. qBittorrent, Transmission, and Deluge all default to µTP.

## Integration Considerations

1. **Negotiation**: µTP requires protocol-level negotiation. Both peers must support it.
   This requires an eMule extension flag or a fallback-to-TCP mechanism. eMuleAI's approach
   is to try µTP first and fall back to TCP on failure.

2. **libutp dependency**: libutp is a C library. Requires adding it as a submodule or
   vendoring it. It is MIT-licensed and actively maintained by BitTorrent Inc.

3. **Layer insertion**: `CUtpSocket` slots in as an `CAsyncSocketExLayer` layer. The existing
   `CEncryptedStreamSocket` layer still works on top. No protocol changes needed.

4. **UDP multiplexing**: µTP runs over UDP. The existing `CClientUDPSocket` / `CUDPSocket`
   infrastructure would need to demultiplex µTP packets from eMule UDP packets.
   eMuleAI's approach uses `ProcessUtpPacket()` called from the UDP receive path.

5. **Coordinate with REF-029** (WSAPoll UDP backend): If the UDP sockets are migrated to
   WSAPoll, µTP demultiplexing needs to work in that framework.

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- µTP socket wrapper and libutp integration:
  [`UtpSocket.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/UtpSocket.h#L14),
  [`UtpSocket.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/UtpSocket.cpp#L1306),
  [`UtpSocket.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/UtpSocket.cpp#L1414),
  [`UtpSocket.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/UtpSocket.cpp#L1507).
- Deferred NAT/µTP connection retry queue:
  [`UtpSocket.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/UtpSocket.cpp#L571).
- UDP demultiplexing and runtime locking in the client UDP socket:
  [`ClientUDPSocket.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientUDPSocket.cpp#L389),
  [`ClientUDPSocket.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientUDPSocket.cpp#L2315).
- Async socket layer interaction:
  [`AsyncSocketEx.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/AsyncSocketEx.cpp#L1251).
- Generic byte-buffer helper used by the µTP wrapper:
  [`Buffer.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Buffer.cpp).

## Protocol Change Notes

µTP itself is a transport change rather than a new file-transfer protocol, but
it still changes the observable peer connection path:

- A peer must know whether the remote side can accept µTP. eMuleAI combines
  this with private NAT capability bits and retry behavior; eMuleBB needs a
  compatibility-preserving negotiation point or a strictly bounded attempt path
  that falls back to normal TCP without altering legacy behavior.
- µTP packets share UDP infrastructure with existing eMule UDP traffic.
  Demultiplexing must be exact, cheap, and failure-safe so malformed or unknown
  UDP packets cannot starve Kad, source exchange, or normal callback traffic.
- Encrypted stream behavior must remain compatible when layered over µTP. The
  encryption handshake cannot assume TCP stream timing or buffering quirks that
  libutp does not guarantee.
- Retry timing and source-state updates must not make disabled µTP builds more
  aggressive than stock. Any "try µTP, then TCP" policy must document when the
  source is considered failed and how that compares to baseline eMule.
- Because libutp owns congestion behavior, the acceptance evidence must include
  throughput, latency, shutdown, and many-socket stress tests on large profiles.

Until those points are proven, the eMuleBB default should be disabled or
experimental-only even if the eventual target is an enabled modern transport.

## Acceptance Criteria

- [ ] libutp added as a submodule or vendored in `srchybrid/libutp/`
- [ ] `CUtpSocket` / `CUtpSocket.h` implemented and compilable
- [ ] µTP negotiation flag defined in extension bits (coordinate with protocol team)
- [ ] Fall-back to TCP if µTP fails or peer doesn't support it
- [ ] µTP packets demultiplexed from standard eMule UDP in `CClientUDPSocket::OnReceive`
- [ ] No regression in standard TCP eMule transfers
- [ ] Preferences toggle: enable/disable µTP; initial release default must stay
      disabled or experimental until interoperability evidence is complete
- [ ] packet-capture evidence proves ordinary UDP/Kad/source-exchange packets
      are not misclassified as µTP
