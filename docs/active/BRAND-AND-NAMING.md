# Brand And Naming

Status: governance. Updated 2026-10-02.

## Canonical Names

- **Organization / house:** **eMuleBB**; GitHub slug `emulebb`.
- **MFC product:** **eMule broadband edition**, compactly **eMuleBB** or the
  **eMuleBB Windows client**.
- **Active Rust project:** **emulebb-rust**. Describe it as the active
  experimental eD2K/Kad beta, not as production-ready.
- **Current planning board:** **eMuleBB Roadmap**.
- **Historical release bundle:** **eMuleBB Suite** applies to the shipped
  `0.7.3` MFC/aMuTorrent bundle, existing artifact names, and historical plans.

Do not use **eMuleBB Suite** as the forward umbrella for organization projects.
Use **eMuleBB projects**, **eMuleBB organization**, or the specific repository
name instead.

## Repository Labels

| Repository | Public description |
|---|---|
| `emulebb` | Stable Windows eD2K/Kad client on the maintained `0.7.x` line |
| `emulebb-rust` | Active experimental Rust eD2K/Kad client; public beta |
| `qbittorrentbb` | Paused unofficial qBittorrent experiment |
| `amutorrent` | Frozen unofficial controller fork shipped with eMuleBB `0.7.3` |
| `trackmulebb` | Archived private controller experiment |
| `goed2k-server` | Deterministic local eD2K test server |
| `ed2k-server` | Rust eD2K server reference fork for possible upstream contributions |
| `amule` | aMule analysis/reference fork |

Where newcomers could confuse a fork with its upstream, state that it is
unofficial and link to the upstream project. Existing release artifacts keep
their published names; this cleanup does not rename tags, packages, executable
files, or the `0.7.3` bootstrapper.

Related: [PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md) and
[WORKSPACE-POLICY](../WORKSPACE-POLICY.md).
