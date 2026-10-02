# eMuleBB Rust 0.1.0-beta.2 Release Notes

Status: ACTIVE CANDIDATE. These notes are finalized only after the release gate
passes and the approved `rust-v0.1.0-beta.2` tag publishes successfully.

`0.1.0-beta.2` is a focused corrective prerelease for the first public Rust
beta. It keeps the beta.1 feature and compatibility surface and fixes a Kad
search timing race reported by a Linux AppImage user operating through a VPN.

## Fixed: Kad Searches Through Higher-Latency Paths

Beta.1 could show Kad as connected, retain a populated contact table, send a
keyword request, and still complete with zero results. The client performed Kad
discovery and the value request sequentially under a shared 45-second deadline.
When discovery used nearly all of that budget, the request sometimes had only
tens of milliseconds left for its answer. A normal VPN round trip was enough for
a valid result to arrive after the search had already closed.

Beta.2 reserves active time for the value-search phase and mirrors stock eMule's
receive-only stop behavior: it stops emitting requests at the active deadline,
then keeps the search alive for 15 seconds to collect replies already in flight.
The REST search collector now covers that result window as well.

This was not a VPN interface-binding or protocol-obfuscation defect. Those
settings remain supported, but changing them cannot repair beta.1's timing race.

## Validation

- Deterministic regression coverage delivers a Kad result after the active
  search deadline and verifies that the client retains it during result grace.
- Focused Kad and core suites, the full Rust workspace suite, strict Clippy,
  formatting, diagnostics, and WebUI unit/browser/build gates pass.
- Debug, release, and packet-diagnostics builds pass with zero warnings.
- The public failure topology is exercised in WSL2 Docker using plain OpenVPN,
  explicit `tun0` binding, packet capture, and controlled tunnel latency.

## Assets

The prerelease publishes the same native platform matrix as beta.1:

- Windows x64 and ARM64 ZIPs
- Linux amd64/arm64 DEBs and x86_64/aarch64 AppImages
- macOS x64 and ARM64 DMGs
- `ghcr.io/emulebb/emulebb-rust:0.1.0-beta.2`

Native packages remain unsigned, and the macOS apps remain unnotarized. The
container image is versioned only; no `latest` tag is published.

## Upgrade And Retest

Back up the profile, stop beta.1, install beta.2, and reuse the profile with only
one daemon process. VPN users should keep their intended binding policy and
repeat the same Kad keyword search after Kad reports connected. Please report
the search method, final status, result count, and approximate tunnel latency;
do not post VPN credentials, private configuration, public addresses, or result
identities.

All beta.1 compatibility boundaries and known limits still apply. See the
[release scope](RELEASE-SCOPE.md) and the
[0.1.0-beta.2 changelog](RELEASE-0.1.0-beta.2-CHANGELOG.md).
