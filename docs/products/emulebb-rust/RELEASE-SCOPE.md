# emulebb-rust Release Scope (`rust-v0.1.0-beta.1`)

This document is the unambiguous, human-facing statement of what the
`emulebb-rust` client **does**, what it **intentionally omits**, and what is
**deferred** for a later release. It is the companion to the machine-readable
divergence registry `policy/rust-client-omissions.toml`. That registry records
the complete current stock-vs-Rust difference set; the matrix below mirrors its
approved omissions and sole deferred behavior for this beta.

`emulebb-rust` is a **headless eD2K/Kad client** with an embedded SPA WebUI,
driven over its Rust-forward `/api/v1` REST contract. It targets eD2K/Kad
protocol-operational parity: the wire behavior, advertised capabilities, state
machines, persistence needed for network correctness, and safety properties
required to operate cleanly with stock-compatible peers, servers, and Kad nodes.
It is not an MFC, stock GUI, legacy WebServer, or legacy preference mirror. Local
controller shape, REST names, UI behavior, scheduling, diagnostics, and
non-protocol settings must evolve as clean Rust-native async daemon surfaces.
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
- **Sharing:** sharing is configured only by shared folder roots. Each root is a
  monitored folder tree and is always scanned recursively; single-file sharing
  and non-recursive folder sharing are not supported Rust surfaces.
- **Routing:** native packages support an explicitly selected direct route;
  direct mode makes no anonymity promise. The supported beta VPN deployment is
  the Docker image sharing a Gluetun network namespace. Gluetun tunnel-down
  egress proof is required before that mode is claimed safe. Native VPN binding
  remains experimental until its own egress pin and leak gate are proven.
- **Control plane:** the Rust-forward `/api/v1` REST contract
  (`x-contract-version`), API-key auth, and embedded SPA WebUI operation. The
  frozen emulebb-mfc REST contract is not a forward compatibility constraint,
  and TrackMuleBB is not a beta dependency. Before an explicit API-freeze
  decision, the Rust daemon, embedded SPA WebUI, OpenAPI artifact, validators,
  and tests are one owned surface: breaking REST shape changes are allowed when
  they make the contract cleaner, provided the owned consumers and conformance
  evidence move in the same change. Do not keep no-op legacy settings fields,
  legacy route names, or compatibility aliases for non-existent external Rust
  consumers. The contract is explicitly unstable between beta releases.
- **Runtime IO:** broadband-oriented async IO is the daemon baseline, not a
  compatibility preference or runtime toggle.
- **Persistence:** single SQLite store (the `known.met` / `clients.met` /
  `server.met` / `preferences.dat` equivalent) — known files, peer credits,
  servers, categories, settings, local identity/secure-ident, and the local
  Kad index.
- **Anti-abuse:** IP + user-hash ban store (4h TTL), IP filter (`ipfilter.dat`),
  upload-queue admission gates, Kad flood detection / rate limiting, packet
  validation, and the bad-peer diagnostic measures (duplicate-block rejection,
  repeat-request tracking, identity-change / file-request-flood bans, upload/
  download recycle and timeout measures).

## Implemented beta parity closures

These previously deferred items are implemented in the beta. They are retained
as `fixed` audit records in `policy/rust-client-omissions-history.toml` and do
not belong in the current parity-difference matrix:

- **Full A4AF connection reuse:** outbound and LowID connect-back sessions walk
  the peer's ordered cross-file relation set on one TCP transport, preserving
  connection-scoped identity/capabilities while attributing NNP and FNF to the
  file that produced each result.
- **Server obfuscation metadata:** extended status replies and crypt-ping
  discovery populate UDP flags, obfuscated TCP/UDP ports, UDP keys, and their
  public-IP binding; the tuple persists across restart and stale keys are
  suppressed after a public-IP change.
- **Media metadata:** bounded shared-file extraction supplies artist, album,
  title, duration, bitrate, and codec for stock-compatible Kad keyword tags,
  plus the supported duration/bitrate/codec subset in eD2K server offers.
- **Upload send granularity:** rate-limited uploads reserve and write the
  maintained fork's 2600-byte chunks at or above 6 KiB/s and 536-byte chunks
  below that threshold; unlimited uploads retain whole-packet writes.
- **Queued duplicate classification:** per-slot request generations preserve
  queued range keys across packets, distinguishing queued duplicates from
  already-served duplicates without changing their rejection on the wire.
- **Parser fuzzing:** four sanitizer-backed libFuzzer targets cover the ED2K
  server, peer TCP, clear/obfuscated client UDP, and Kad v2 parser families.
- **Alternate UPnP IGD:** MiniUPnPc remains preferred, with an independent
  in-tree SSDP/SOAP IGD provider as the ordered fallback under the same bind,
  mapping, rollback, and diagnostic contract.

## Frozen beta parity matrix

This is the complete current stock-vs-Rust difference set for
`rust-v0.1.0-beta.1`. The registry ID is the machine-readable authority.

| Registry ID | Frozen beta disposition | Compatibility contract |
|---|---|---|
| `sx1-live-source-exchange` | Approved omission | SX2 only; SX1 is unadvertised and live SX1 packets are ignored. |
| `ipv6-ed2k-kad` | Approved omission | eD2K, Kad, peer transfer, NAT, and bootstrap are IPv4-only. |
| `peer-chat-messaging` | Approved omission | No peer chat/captcha UI; captcha is unadvertised and unsolicited packets are tolerated. |
| `ed2k-preview` | Approved omission | Preview is unadvertised; Rust neither requests nor answers media previews. |
| `kad-flood-lan-exemption` | Approved omission | LAN/loopback stays flood-exempt; public peers retain stock flood controls. |
| `conn-rate-rolling-five-second-window` | Deferred behavior | A true rolling five-second grant window is gentler and has no wire effect. |

## Freeze rule

These six rows are the beta's complete intentional parity differences. The
approved omissions are product decisions, not open gaps; the conservative
connection-rate window is the only deferred behavior. Reopening an omission or
adding another parity difference requires a deliberate release-scope decision
and a matching registry update. Already-fixed audit history must not be copied
back into this current matrix.

## Rust Beta gate

`rust-v0.1.0-beta.1` may ship with a signed-off non-critical parity backlog, but
not with unresolved P0 safety or critical stock-wire parity findings. The beta
gate is:

- isolated Docker-over-Gluetun tunnel-down proof shows zero off-tunnel P2P
  egress; native VPN-safe claims remain deferred;
- stock eMule wire-critical parity review has no undispositioned P0 findings;
- the frozen parity matrix has an explicit registry disposition for every row;
- Rust OpenAPI conformance is enforced for the native daemon/UI boundary;
- the embedded SPA WebUI is green against the candidate daemon for status,
  transfers, uploads, search/download, shared files, servers/Kad, settings,
  logs, and diagnostics.
- diagnostics-first, no-share, bounded public-network campaigns on Windows x64
  and WSL Ubuntu x64 pass. Each completes and SHA-256-verifies an approved small
  Linux document; at least one completes an approved Linux ISO. A stock-
  identifying live peer supplies accepted file-block bytes. Local deterministic
  Rust-to-MFC upload and MFC-to-Rust download pass.
- packaged native startup, every current WebUI panel, local transfer, and clean
  shutdown pass on Windows, Linux, and macOS, x64 and ARM64. The amd64/arm64
  image passes persistence, permissions, and Gluetun isolation checks.

The published prerelease assets are unsigned Windows x64/ARM64 ZIPs, Linux
amd64/arm64 DEBs, Linux x86_64/aarch64 AppImages, unsigned and unnotarized macOS
x64/ARM64 app-in-DMGs, and a versioned GHCR Linux amd64/arm64 image. The image
uses s6-overlay, `PUID`/`PGID`/`TZ`, `/config`, and `/data`; its beta tag is not
`latest`. An independent Gluetun test stack must leave the operator's running
P2P stack untouched.
TrackMuleBB is archived and is not tagged, packaged, or required for the Rust
beta lane.

## Platform tier

- **Windows x64 and ARM64** — portable ZIPs; x64 also receives the deep public
  live campaign.
- **Linux x64 and ARM64** — DEB and AppImage; WSL2 Ubuntu x64 also receives the
  deep public live campaign.
- **macOS x64 and ARM64** — unsigned, unnotarized app-in-DMG; native packaged
  smoke only, not a public-network soak.
