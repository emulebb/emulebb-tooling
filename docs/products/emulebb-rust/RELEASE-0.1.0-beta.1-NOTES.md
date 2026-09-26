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
- An embedded SPA WebUI for status, transfers, search, sharing, uploads,
  servers, Kad, settings, logs, and diagnostics.
- API-key-protected `/api/v1` REST and SSE surfaces. The owned OpenAPI contract
  is tested against live daemon responses in CI.
- Unsigned native packages for Windows, Linux, and macOS on x64 and ARM64.
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

An explicit `--profile <dir>` is an operator-managed profile and must already
contain `emulebb-rust-settings.toml`. The SQLite repository in that profile is
`emulebb-rust-metadata.db`. Do not run two clients against the same live profile.

## macOS Unsigned Launch

The macOS app is unsigned and unnotarized. Mount the DMG, copy
`eMuleBB Rust.app` to Applications, then approve the first launch in
**System Settings > Privacy & Security** if Gatekeeper blocks it. The app starts
the daemon, waits for the local WebUI, and opens it in the browser. Quit the app
to stop its daemon.

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
- eD2K/Kad networking is IPv4-only.
- `/api/v1` is owned by the daemon and embedded WebUI and may change between
  beta releases; it is not frozen as an external compatibility contract.
- Source Exchange v1 is intentionally absent; Source Exchange v2 remains
  supported.
- Peer chat/captcha interaction and peer media preview are not exposed. Preview
  is an approved permanent drop to avoid an untrusted media-decoding surface.
- Kad-published files do not include optional bitrate/codec/length/artist/album/
  title tags, so media-attribute-filtered searches may not match them.
- Sharing is by recursive monitored folder roots only. Single-file and
  non-recursive sharing are not supported surfaces.
- The frozen Slint UI, TrackMuleBB, autonomous Torznab/indexer work, Arr
  integration, and a full eMule A4AF scheduler are not included in this beta.
- Native packages and macOS apps are unsigned; macOS apps are not notarized.

## What To Test

Start with a fresh or backed-up profile. Confirm WebUI/API-key access, clean
shutdown, server and Kad connectivity, one small search/download, finished-file
delivery, one shared folder, and persistence across restart. For containers,
also confirm host ownership on `/config` and `/data`, then perform a controlled
Gluetun tunnel-down check before relying on the VPN deployment.

