# eMuleBB Rust 0.1.0-beta.1 Release Notes

Status: ACTIVE CANDIDATE. These notes are finalized only after the release gate
passes and the operator explicitly approves the `rust-v0.1.0-beta.1` tag.

`0.1.0-beta.1` is the first public prerelease of the Rust-native eMuleBB client:
a headless, cross-platform eD2K/Kad daemon with an embedded browser WebUI and a
Rust-forward `/api/v1` REST control plane. It is not the Windows MFC application
ported line by line, and it does not mirror the legacy MFC REST contract.

For the operational delta, see the
[0.1.0-beta.1 changelog](RELEASE-0.1.0-beta.1-CHANGELOG.md). The exact supported,
omitted, and deferred surface is defined by the
[release scope](RELEASE-SCOPE.md).

## What Ships

- Stock-compatible IPv4 eD2K and Kad networking, including server HighID/LowID,
  search, source discovery, download/upload, secure identification, AICH/ICH,
  UDP source reask, Kad publish/search, firewall checks, and LowID buddy
  callbacks.
- Recursive monitored folder sharing, finished-file delivery, categories,
  persisted servers/settings/identity/credits, local SQLite indexing, IP filter,
  and anti-abuse controls.
- Full peer-centric A4AF connection reuse across outbound and LowID connect-back
  sessions, including per-file NNP/FNF handling on a reused TCP transport.
- Learned and persisted server obfuscation metadata, including obfuscated
  TCP/UDP ports, UDP keys, public-IP binding, stale-key suppression, and bounded
  crypt-ping/plaintext discovery fallback.
- Bounded shared-file media-metadata extraction and stock-compatible publication
  of artist, album, title, duration, bitrate, and codec through Kad and the
  supported eD2K server-offer subset.
- Maintained-fork upload send granularity and cross-packet queued-duplicate
  classification, preserving equal-share pacing and distinguishing queued from
  already-served duplicate block requests.
- Sanitizer-backed fuzz targets for the ED2K server, peer TCP, clear/obfuscated
  client UDP, and Kad v2 parser families.
- Ordered UPnP/IGD backend diversity: MiniUPnPc first, then an independent
  in-tree SSDP/SOAP provider with the same bind and mapping safety contract.
- An embedded SPA WebUI for status, transfers, search, sharing, uploads,
  servers, Kad, settings, logs, and diagnostics.
- Automatic first-run eD2K and Kad startup, with live server ranking and
  fallback when the preferred public server is unavailable.
- WebUI network controls, persistent search-session routes and history, paged
  live search results, and explicit transfer stop and delete actions.
- API-key-protected `/api/v1` REST and SSE surfaces. The owned OpenAPI contract
  is tested against live daemon responses in CI.
- Native packages for Windows, Linux, and macOS on x64 and ARM64.
- A versioned Linux amd64/arm64 GHCR image using s6-overlay, `PUID`/`PGID`/`TZ`,
  `/config`, and `/data/ed2k`.

## Native Package Assets

The prerelease is expected to contain these payloads plus per-asset manifests,
SPDX SBOMs, and a combined `SHA256SUMS` file:

- `emulebb-rust-v0.1.0-beta.1-windows-x64.zip`
- `emulebb-rust-v0.1.0-beta.1-windows-arm64.zip`
- `emulebb-rust-v0.1.0-beta.1-linux-amd64.deb`
- `emulebb-rust-v0.1.0-beta.1-linux-x86_64.AppImage`
- `emulebb-rust-v0.1.0-beta.1-linux-arm64.deb`
- `emulebb-rust-v0.1.0-beta.1-linux-aarch64.AppImage`
- `emulebb-rust-v0.1.0-beta.1-macos-x64.dmg`
- `emulebb-rust-v0.1.0-beta.1-macos-arm64.dmg`

The container is published only as
`ghcr.io/emulebb/emulebb-rust:0.1.0-beta.1`; this prerelease does not publish a
`latest` tag.

## First Run

Run the packaged daemon directly. Without `--profile`, it creates its profile
under the platform configuration directory and prints the generated WebUI API
key on first launch:

- Windows: the platform application-data directory
- Linux: `$XDG_CONFIG_HOME/emulebb-rust`, or `~/.config/emulebb-rust`
- macOS: `~/Library/Application Support/emulebb-rust`

Open `http://127.0.0.1:4711/` and enter the generated API key when prompted. The
same key is sent as `X-API-Key` by REST clients. Keep the WebUI/REST listener on
loopback or a trusted network; do not expose it directly to the public internet.

The default profile automatically starts eD2K and Kad after bootstrap. Native
packages use the selected direct route unless an explicit bind policy is
configured, so first launch may contact public eD2K/Kad infrastructure and does
not provide anonymity. The Network, Servers, and Kad views expose current
connection state and manual controls.

An explicit `--profile <dir>` is an operator-managed profile and must already
contain `emulebb-rust-settings.toml`. The SQLite repository in that profile is
`emulebb-rust-metadata.db`. Do not run two clients against the same live profile.

## macOS First Launch

Mount the DMG, copy `eMuleBB Rust.app` to Applications, then approve the first
launch in **System Settings > Privacy & Security** if Gatekeeper blocks it. The
app starts the daemon, waits for the local WebUI, and opens it in the browser.
Quit the app to stop its daemon.

## Docker And Gluetun

The image stores profile state below `/config/emulebb-rust` and completed
downloads below `/data/ed2k`. Set `PUID`, `PGID`, and `TZ` to match the host
operator and mount persistent volumes for `/config` and `/data`.

The supported beta VPN deployment is the repository's isolated Gluetun Compose
example. It shares the Gluetun network namespace and pins Rust P2P traffic to
`tun0` with `EMULEBB_RUST_P2P_INTERFACE`. Publish the WebUI/REST and P2P ports on
Gluetun, not on the Rust container. Use separate read-only VPN credentials and
do not modify or restart another running P2P stack.

Native packages support explicit direct routing but make no anonymity or native
VPN leak-safety promise. The Gluetun deployment is the beta's tested VPN posture.

## Known Limits And Compatibility Boundaries

- This is a beta. Back up important profile and download state before testing.
- The frozen stock-vs-Rust difference set is the six-row
  [release-scope parity matrix](RELEASE-SCOPE.md#frozen-beta-parity-matrix).
- Source Exchange v1 is absent and unadvertised; Source Exchange v2 remains
  supported.
- eD2K, Kad, peer transfer, NAT, and bootstrap are IPv4-only; IPv6 is not
  advertised.
- Peer chat and captcha interaction have no daemon/WebUI surface; captcha is
  unadvertised and unsolicited packets are safely ignored.
- Peer media preview is absent and unadvertised to avoid adding an untrusted
  media-decoding surface.
- LAN/loopback Kad sources remain flood-exempt even outside stock LAN mode;
  public peers retain the stock flood controls.
- Outgoing connections use a conservative rolling five-second grant window;
  this is gentler than stock tick-batch pacing and has no wire effect.
- `/api/v1` is owned by the daemon and embedded WebUI and may change between
  beta releases; it is not frozen as an external compatibility contract.
- Sharing is by recursive monitored folder roots only. Single-file and
  non-recursive sharing are not supported surfaces.
- The frozen Slint UI, TrackMuleBB, autonomous Torznab/indexer work, Arr
  integration are not included in this beta.
- macOS may require first-launch approval in
  **System Settings > Privacy & Security**.

## What To Test

Start with a fresh or backed-up profile. Confirm WebUI/API-key access, clean
shutdown, automatic server and Kad connectivity, fallback from an unavailable
server, persistent search history/deep links, one small search/download,
transfer stop/delete behavior, finished-file delivery, one shared folder, and
persistence across restart. For containers, also confirm host ownership on
`/config` and `/data`, then perform a controlled Gluetun tunnel-down check before
relying on the VPN deployment.
