# eMuleBB Roadmap Summary

This is the public-readable roadmap summary. The detailed engineering backlog is
the [Active Backlog](../active/INDEX.md); the MFC roadmap is the
[Future Roadmap](../active/FUTURE-ROADMAP.md); the forward program is the
[Suite Joint Roadmap](../active/SUITE-JOINT-ROADMAP.md).

## Product Direction

The eMuleBB **MFC desktop app** closes its `0.7.x` feature line with stable
`0.7.3`. The MFC line is frozen except for critical maintenance and
non-behavior-expanding diagnostics/instrumentation. The MFC client is valuable,
but it is expensive to evolve properly, so near-term forward development focuses
on **emulebb-rust** — the multiplatform eD2K/Kad headless client plus embedded
SPA WebUI. **qBittorrentBB** remains future BitTorrent companion work, and
**TrackMuleBB** is parked until that companion track progresses enough to justify
a cross-network controller. The goal is unchanged at the product level: keep
classic eD2K/Kad behavior understandable, make discovery reliable, and stay
stock-compatible.

## Release Line Direction

`0.7.3` is the **final `0.7.x` feature release**. Its public train is fixed as
`0.7.3-rc.1`, `0.7.3-rc.2`, `0.7.3-rc.3`, then stable `0.7.3`. After that,
`0.7.x` is the permanent maintenance line with a frozen public surface. Accept
only security, crash/data-loss, packaging, update-check, release-proof,
documentation fixes, and non-behavior-expanding diagnostics/instrumentation.
The recorded MFC lean/performance/async ideas stay available as archived notes,
but active forward development now prioritizes emulebb-rust. The forward suite
stays out of the whole `0.7.x` line; the `0.7.3`/`0.7.x` bundle remains MFC
client + aMuTorrent + Arr only, delivered by the `install.ps1` thin wrapper.

## Where The Future Work Is

The forward program lives in the [Suite Joint Roadmap](../active/SUITE-JOINT-ROADMAP.md):

- **emulebb-rust** — active near-public-beta eD2K/Kad client work: headless
  daemon stability, embedded SPA WebUI, safety, persistence, REST correctness,
  and parity proof.
- **qBittorrentBB** — future BitTorrent companion work: DHT harvester, branded
  export to the eD2K share, and Torznab index.
- **TrackMuleBB / suite integrations** — parked future work: metadata fabric,
  cross-network handoff, and controller/setup automation after the Rust and
  BitTorrent foundations are ready.

## What Remains On The MFC App

Only narrow maintenance remains:

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
