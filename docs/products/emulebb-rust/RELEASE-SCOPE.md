# emulebb-rust Release Scope (`rust-v0.1.0-beta.1`)

This document is the unambiguous, human-facing statement of what the
`emulebb-rust` client **does**, what it **intentionally omits**, and what is
**deferred** for a later release. It is the companion to the machine-readable
divergence registry `policy/rust-client-omissions.toml`. That registry records
known stock-vs-Rust differences; this document and the active re-audit backlog
decide whether each difference is a permanent drop, release-blocking gap, or
deferred backlog item.

`emulebb-rust` is a **headless eD2K/Kad client** with a Rust-native UI, driven
over its Rust-forward `/api/v1` REST contract. It targets eD2K/Kad
protocol-operational parity: the wire behavior, advertised capabilities, state
machines, persistence needed for network correctness, and safety properties
required to operate cleanly with stock-compatible peers, servers, and Kad nodes.
It is not an MFC, stock GUI, legacy WebServer, or legacy preference mirror. Local
controller shape, REST names, UI behavior, scheduling, diagnostics, and
non-protocol preferences must evolve as clean Rust-native async daemon surfaces.
The active registry is the beta gap board: implemented fixes live in audit
history, while current defers and approved drops remain in
`policy/rust-client-omissions.toml`.

## Supported surface

- **eD2K (IPv4):** server login/ident (HighID + LowID), search, source
  discovery (connected-server TCP + global UDP), download and upload with the
  full block/part protocol (multipacket, compressed parts, 64-bit offsets),
  hashset + AICH request/answer, ICH block-level salvage, secure identification
  (RSA), credits/clients persistence, upload queue with scoring and elastic
  broadband slots, UDP source reask, and the eD2K server-mediated LowID callback.
- **Kad (IPv4):** bootstrap, routing table (split / weak-replacement / small- &
  big-timer maintenance / zone consolidation), lookups incl. the FIND_VALUE_MORE
  re-ask, keyword/source/notes search + publish, firewall self-check (UDP + TCP),
  the LowID **buddy** system and buddy-relayed callbacks, and the local
  keyword/source index.
- **Finished-file delivery:** completed downloads are materialized by name into
  the per-transfer category path, else the configured `incomingDir` (hard-link
  on the same volume, copy+atomic-rename across volumes; the internal piece
  store is retained for continued seeding).
- **Safety:** fail-closed VPN egress pinning of every P2P socket to the tunnel
  interface (`IP_UNICAST_IF`); with the tunnel down, zero P2P data-plane traffic
  and the control plane still answers (RUST-FEAT-003 pin + RUST-FEAT-005 leak
  test).
- **Control plane:** the Rust-forward `/api/v1` REST contract
  (`x-contract-version`), API-key auth, and Rust-native UI operation. The frozen
  emulebb-mfc REST contract is not a forward compatibility constraint, and
  TrackMuleBB is not a beta dependency. Before an explicit API-freeze decision,
  the Rust daemon, Rust-native UI, OpenAPI artifact, validators, and tests are
  one owned surface: breaking REST shape changes are allowed when they make the
  contract cleaner, provided the owned consumers and conformance evidence move
  in the same change. Do not keep no-op legacy preference fields, legacy route
  names, or compatibility aliases for non-existent external Rust consumers.
- **Runtime IO:** broadband-oriented async IO is the daemon baseline, not a
  compatibility preference or runtime toggle.
- **Persistence:** single SQLite store (the `known.met` / `clients.met` /
  `server.met` / `preferences.dat` equivalent) — known files, peer credits,
  servers, categories, preferences, local identity/secure-ident, and the local
  Kad index.
- **Anti-abuse:** IP + user-hash ban store (4h TTL), IP filter (`ipfilter.dat`),
  upload-queue admission gates, Kad flood detection / rate limiting, packet
  validation, and the bad-peer diagnostic measures (duplicate-block rejection,
  repeat-request tracking, identity-change / file-request-flood bans, upload/
  download recycle and timeout measures).

## Permanent omissions

These are product decisions, not open gaps. Anything not listed here remains
subject to re-audit.

- **Source Exchange v1** (`sx1-live-source-exchange`) — SX2-only; SX1 never sent,
  answered, or ingested (operator decision REF-002).
- **IPv6 eD2K/Kad** (`ipv6-ed2k-kad`) - the beta line is IPv4-only and does not
  advertise IPv6 support.
- **Kad LAN flood exemption strictness** (`kad-flood-lan-exemption`) - the Rust
  receiver keeps LAN/loopback Kad sources flood-exempt unconditionally; this has
  no public-node wire effect and fits the VPN deployment posture.
- **Peer media preview** (`ed2k-preview`) - Rust does not advertise peer preview
  support, does not request previews, and does not add an untrusted media decode
  surface for beta. Inbound preview packets remain diagnostic-only.

## Re-audit candidates

The active registry carries protocol-operational divergences only. `RUST-REF-004`
owns the re-audit and must keep each active row in one of these states before
beta sign-off:

- approved permanent protocol drop;
- deferred protocol backlog with owner, rationale, and target;
- beta blocker requiring a protocol fix before release.

## Deferred (not omitted — parked for a later release)

Real future capability, intentionally out of `0.1.0-beta.1` unless the re-audit
promotes it to a beta blocker:

- **Peer chat/messaging** (`peer-chat-messaging`) - OP_MESSAGE/captcha packets
  are decode-only and not surfaced by the headless daemon/UI. Revisit only if
  peer messaging becomes a Rust product feature.
- **Conservative connection pacing** (`conn-rate-rolling-five-second-window`) -
  the outgoing connection grant window is a true rolling five seconds, which is
  gentler than tick-batch pacing and not wire-incompatible.
- **Upload send granularity polish**
  (`upload-throttle-focus-slot-distribution`) - Rust matches the equal-share
  fairness model; only low-cap packet granularity remains as optional polish.
- **Upload duplicate diagnostic classification**
  (`upload-duplicate-queued-intra-packet`) - duplicate block requests are still
  rejected; only the diagnostic event label may differ for cross-packet queued
  duplicates.
- **Discovered-server obfuscation metadata**
  (`server-obfuscation-metadata-non-config`) - configured obfuscated servers are
  supported; non-config discovered obfuscation metadata can wait unless that
  server path becomes a requirement.
- **Kad media metadata tags** (`kad-keyword-media-metadata-tags`) - published
  entries are findable by keyword/type/name/size, but optional bitrate/codec/
  length/artist/album/title filtering waits on a separate metadata extractor
  decision.
- **A4AF full model** — A4AF-lite (cross-transfer source reuse + No-Needed-Parts
  swap) ships; the full eMule A4AF source-set/hijacking model is parked pending a
  better design. Downloads are independent per-transfer tasks (no shared
  scheduler) by design.
- **Autonomous indexer + Torznab** (RUST-FEAT-002) and **Arr integration**
  (RUST-FEAT-004).
- **Docker/GHCR image** (RUST-FEAT-006) and **REST SSE push** (RUST-FEAT-007).
- **Parser fuzzing** — cargo-fuzz targets for the hand-rolled binary parsers.
- **Alternate UPnP-IGD NAT backend** — `nat/igd.rs` is a stub; the miniupnpc
  backend is the supported one.
- **Anti-abuse depth (defensive-measures plan)** — OP_OutOfPartReqs
  quarantine/cooldown escalation (Phase D), upload-admission cooldowns
  (failed-admit / no-socket / short-failed-slot; Phase E), and the
  download-queue-rank-flood ban (Phase C remainder). The base detectors
  (out-of-part-reqs, file-request-flood, identity-change bans) ship; the
  escalation state machines are parked in the defensive-measures roadmap. None
  blocker.
- **Kad/eD2K memory-safety & stat cosmetics** — self-imposed global Kad
  source/notes index ceilings (MFC has none), the network-size estimate using
  base firewalled constants instead of a live-ratio blend, and the 128-entry
  per-slot DoneBlocks history (MFC unbounded). Documented, effectively
  non-binding, no wire impact.

## Rust Beta gate

`rust-v0.1.0-beta.1` may ship with a signed-off non-critical parity backlog, but
not with unresolved P0 safety or critical stock-wire parity findings. The beta
gate is:

- automated fail-closed VPN leak proof is passing;
- stock eMule wire-critical parity review has no undispositioned P0 findings;
- the non-SX1 omission re-audit has an explicit backlog disposition for every
  registered divergence;
- Rust OpenAPI conformance is enforced for the native daemon/UI boundary;
- the Rust-native UI is green against the candidate daemon for status,
  transfers, uploads, search/download, shared files, servers/Kad, settings,
  logs, and diagnostics.

The published prerelease artifact is the emulebb-rust Windows x64 zip.
TrackMuleBB is parked and is not tagged, packaged, or required for this first
Rust beta.

## Platform tier

- **Windows x64** — release-supported (the distributed artifact).
- **Linux** — runtime-proven (WSL2 Ubuntu) but not packaged in this release.
- **macOS** — compile/test-viable only (one behavioral FS-watcher test is skipped
  there; see `shared_dir_monitor_e2e.rs`).
