# eMuleBB Roadmap Summary

This is the public-readable roadmap summary. The detailed engineering backlog
remains [Active Backlog](../active/INDEX.md), and the curated future roadmap
remains [Future Roadmap](../active/FUTURE-ROADMAP.md).

## Product Direction

eMuleBB stays a native Windows desktop eMule client. The product goal is not to
turn it into a headless daemon or a new network. The goal is to keep classic
eD2K/Kad behavior understandable while making modern Windows, broadband,
large-library, and controller workflows reliable.

## Release Line Direction

`0.7.3` is the compatibility baseline. Its public train is fixed as
`0.7.3-rc.1`, `0.7.3-rc.2`, `0.7.3-rc.3`, then stable `0.7.3`. After that,
`0.7.x` becomes the legacy support line with a frozen public surface, while
`0.8.x` becomes the modernization line. The first `0.8.0` objective is removing
legacy surfaces that were intentionally frozen for the `0.7.x` transition.

## Five Themes

### 1. Better Connectivity Without Protocol Forks

Future connectivity work focuses on compatibility: clearer LowID/Kad
diagnostics, safer bind/interface behavior, NAT mapping visibility, and
eventual IPv6-compatible paths where they preserve stock network semantics.

### 2. Large Libraries And Long Sessions

Startup, sharing, hashing, cache, and storage work should keep large profiles
responsive without hiding what the app is doing. Safety around `.met`, `.dat`,
temp, incoming, and shared paths remains more important than cosmetic speed.

### 3. Local Automation That Respects The Desktop App

REST, aMuTorrent, qBittorrent-compatible routes, and Torznab adapters are local
controller surfaces. They should make eMuleBB easier to operate, but the native
desktop app remains the owner of live eD2K/Kad, transfer, sharing, and profile
state.

### 4. Power-User UI Polish

UI work should improve repeated operation: better table/menu consistency,
keyboard workflows, preference clarity, progress visibility, DPI behavior, and
eventual dark-mode support.

### 5. Safer Operations And Evidence

Release proof, diagnostics, IP-filter handling, dependency loading, and
troubleshooting evidence should make failures easier to reproduce and less
likely to damage a profile.

## Not On The Current Product Track

The current roadmap does not promote headless-only operation, mobile-first
scope inside the desktop app, incompatible eD2K/Kad behavior, automatic legacy
profile mutation wizards, or broad REST capability expansion without a concrete
controller need.

Use the detailed [Future Roadmap](../active/FUTURE-ROADMAP.md) for item
anchors and exact scope boundaries.
