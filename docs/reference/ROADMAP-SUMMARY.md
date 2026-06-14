# eMuleBB Roadmap Summary

This is the public-readable roadmap summary. The detailed engineering backlog is
the [Active Backlog](../active/INDEX.md); the MFC roadmap is the
[Future Roadmap](../active/FUTURE-ROADMAP.md); the forward program is the
[Suite Joint Roadmap](../active/SUITE-JOINT-ROADMAP.md).

## Product Direction

The eMuleBB **MFC desktop app** is closing with `0.7.3` final and entering
permanent `0.7.x` maintenance. Forward development has shifted to **emulebb-rust**
— the multiplatform eD2K/Kad core behind the shared `/api/v1` contract — together
with **qBittorrentBB** (the BitTorrent companion) and the suite integrations. The
goal is unchanged at the product level: keep classic eD2K/Kad behavior
understandable, make discovery and automation reliable, and stay
stock-compatible — but the place that work happens is now the rust/suite program,
not the Windows MFC app.

## Release Line Direction

`0.7.3` is the **final eMuleBB MFC feature release**. Its public train is fixed as
`0.7.3-rc.1`, `0.7.3-rc.2`, `0.7.3-rc.3`, then stable `0.7.3`. After that, `0.7.x`
is the permanent maintenance line with a frozen public surface (security,
crash/data-loss, packaging, update-check, release-proof, and documentation fixes
only). A `0.8.0` MFC modernization line is **on hold / under review** — not
retired, not active — pending a decision on whether the MFC app continues given
the emulebb-rust pivot.

## Where The Future Work Is

The forward program lives in the [Suite Joint Roadmap](../active/SUITE-JOINT-ROADMAP.md):

- **emulebb-rust** — perfectly functional eD2K/Kad client plus an autonomous
  Kad/eD2K indexer, with native `/api/v1`, Torznab, and a
  qBittorrent-compatible download-client surface.
- **qBittorrentBB** — a BitTorrent client with a DHT harvester, a branded
  idempotent export to the eD2K share, and a Torznab index.
- **Suite integrations** — a disk-grounded metadata fabric bridging torrents,
  eMule collections, and eD2K shares; Prowlarr/Arr federation; and aMuTorrent as
  the optional cross-network controller.

## What Remains On The MFC App

Only maintenance and family/packaging work:

1. **Security and operations** — IP-filter policy, dependency/DLL hardening,
   diagnostics, the bound VPN public-IP guard, and release proof (as `0.7.x`
   maintenance).
2. **Controller surface performance** — bounded REST memory/latency for large
   profiles, only where it protects the shipped `0.7.3` controller.
3. **Product-family integration** — shared REST conformance, shared test
   campaigns, and shared dependency ownership without merging products.
4. **Ecosystem suite packaging** — the MFC app as a packaged suite component
   (Windows bootstrap, local Arr, aMuTorrent).

## Superseded Or Not On Track

These earlier MFC product themes are no longer on the MFC roadmap. Where the value
is still wanted it is carried by the rust/suite program; the rest is dropped:

- Connectivity modernization (IPv6, NAT/LowID, µTP) — long-term ideas only;
  emulebb-rust is IPv4-only by policy.
- Search and trust clarity, and local SQLite/config planning — superseded by the
  rust Kad/eD2K indexer and the suite metadata fabric.
- Power-user UI polish (dark mode, DPI), large-library startup performance, and
  upload-policy features — dropped for a closing MFC app (crash/data-loss
  stability fixes still land as maintenance).

The MFC app also does not promote headless-only operation, mobile-first scope,
incompatible eD2K/Kad behavior, automatic legacy-profile mutation wizards, or
broad REST capability expansion. Use the
[Future Roadmap](../active/FUTURE-ROADMAP.md) for exact item anchors and scope
boundaries.
