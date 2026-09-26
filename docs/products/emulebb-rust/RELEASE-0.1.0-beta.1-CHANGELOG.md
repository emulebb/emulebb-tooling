# eMuleBB Rust 0.1.0-beta.1 Changelog

Status: ACTIVE CANDIDATE. Final candidate heads, artifact hashes, and publication
date are recorded only after the release gate passes and the operator explicitly
approves the `rust-v0.1.0-beta.1` tag.

Format: one line per item, grouped by area; this is a power-user changelog, not a
Git log.

## Product And Runtime

- First public Rust-native eMuleBB prerelease: a headless daemon with embedded browser WebUI, Rust-forward REST control plane, and SQLite-backed profile state.
- Added platform-native default profiles plus explicit `--profile` operation; REST bootstrap/auth remains in `emulebb-rust-settings.toml`, with runtime settings and network state in `emulebb-rust-metadata.db`.
- Added finished-download delivery to category or incoming directories with same-volume hard-link and cross-volume copy/atomic-rename behavior while retaining the piece store for seeding.
- Added recursive monitored folder-root sharing, persistent categories/servers/settings/identity/credits, local file indexing, and observable reload/hash progress.
- Made broadband-oriented async IO the default runtime model instead of a compatibility preference or legacy UI toggle.

## eD2K And Kad

- Added IPv4 eD2K server login with HighID/LowID operation, search, TCP/global-UDP source discovery, transfer queues, compressed/multipacket blocks, 64-bit offsets, AICH/ICH, secure identification, and persisted credits.
- Added UDP source reask, server-mediated LowID callback, server cycling/import, obfuscation for configured servers, and bounded connection/source scheduling.
- Added Kad bootstrap, routing maintenance, search/publish/local index, firewall checks, buddy operation and buddy-relayed callbacks, flood controls, and persistence.
- Added upload scoring, elastic broadband slots, equal-share FIFO bandwidth scheduling, duplicate-block rejection, peer bans, IP filtering, and network-facing diagnostics.
- Kept the live source-exchange surface SX2-only; SX1, IPv6 eD2K/Kad, peer media preview, and strict LAN-mode flood semantics are approved omissions for this beta.
- Deferred peer chat, optional Kad media-metadata tags, discovered-server obfuscation metadata, low-cap upload-send granularity polish, and one duplicate-request diagnostic-label distinction without claiming those surfaces as full parity.

## REST, WebUI, And Diagnostics

- Added API-key-authenticated `/api/v1` resources for application state, settings, transfers, uploads, search, sharing, categories, servers, Kad, NAT, VPN Guard, IP filter, logs, and runtime diagnostics.
- Added the embedded Vite/Preact WebUI and packaged it beside every native daemon and inside the container image.
- Added SSE reset/resume behavior and contract-version headers while keeping the Rust REST contract explicitly unstable between beta releases.
- Added static route/query/body/auth/header drift checks and a live 100-route plus SSE OpenAPI response-conformance CI gate using the tested Linux daemon artifact.
- Added regular operational summaries and diagnostics for process state, ED2K/Kad, publish, transfer, upload, download, shared hashing/reload, VPN Guard, and public-IP probes.

## Routing And Safety

- Made explicit P2P bind/interface selection fail closed across ED2K, Kad, STUN, NAT, listeners, and outbound transport paths.
- Added a blocking test-only socket-egress audit covering tunnel-up, tunnel-down, and tunnel-pulled scenarios while preserving loopback REST control.
- Added Docker-over-Gluetun isolation proof with positive sensor validation and zero observed off-tunnel P2P packets after tunnel loss.
- Kept native packages in direct-route posture with no anonymity promise; the isolated Gluetun namespace is the tested beta VPN deployment.

## Packaging And Operations

- Added unsigned Windows x64/ARM64 ZIP packaging with embedded WebUI, example settings, license, release scope, manifest, SPDX SBOM, and SHA-256 evidence.
- Added Linux amd64/arm64 DEB and x86_64/aarch64 AppImage packaging with the same runtime/WebUI and provenance contract.
- Added unsigned, unnotarized macOS x64/ARM64 app-in-DMG packaging with first-launch Gatekeeper guidance and browser WebUI startup.
- Added a linuxserver-style s6 OCI image for linux/amd64 and linux/arm64 with `PUID`/`PGID`/`TZ`, `/config`, `/data/ed2k`, and a versioned beta tag only.
- Added six-target native package smoke and multi-architecture image assembly gates; publication remains tag-only after separate operator approval.
- Added per-asset manifests and SPDX SBOMs plus a release-wide `SHA256SUMS` file; final published hashes remain pending candidate approval.

## Validation

- Added deterministic Rust-to-Rust and Rust-to-MFC upload/download coverage, stock-compatible live-byte witnesses, and exact delivered-file SHA-256 verification.
- Added Windows and WSL direct-network diagnostic campaigns with bounded inputs, retained sanitized evidence, and graceful teardown requirements.
- Added cross-platform Rust build/test CI on Windows, Linux, and macOS, pinned Rust/tool/action dependencies, formatting/Clippy policy, and cargo-deny advisory/license/source gates.
- Added native package/WebUI startup smoke, container ownership/persistence checks, and independent Gluetun tunnel-down validation without touching an operator's existing stack.

## Migration And Risk Notes

- Treat this as a new Rust beta profile; do not point it at a live MFC profile or run two clients against one profile directory.
- Back up state before testing; development-era SQLite schemas are current-only and are not silently repaired or migrated by the Rust daemon.
- REST clients must use `X-API-Key`; keep the listener on loopback or a trusted network and expect contract changes in later betas.
- macOS packages require manual first-launch approval because they are unsigned and unnotarized; all native packages may trigger platform reputation warnings.
- TrackMuleBB, the frozen Slint UI, autonomous Torznab/indexer and Arr integration are outside this artifact set.
