# Brand And Naming

Status: governance. Updated 2026-10-02.

## Canonical Names

- **Organization / house:** **eMuleBB**; GitHub slug `emulebb`.
- **MFC product:** **eMule broadband edition**, compactly **eMuleBB** or the
  **eMuleBB Windows client**.
- **Active Rust product:** **eMuleBB Rust**. Retain `emulebb-rust` for repository
  and technical identifiers. Describe it as the active eD2K/Kad beta: public
  `0.1.0-beta.2`, working toward Beta 3, not as a stable release.
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
| `emulebb-rust` | eMuleBB Rust, the active Rust eD2K/Kad client; public Beta 2 working toward Beta 3 |
| `ed2k-server` | Sole local deterministic eD2K test server; upstream-aligned Rust fork |
| `amule` | Managed official aMule upstream; interoperability and protocol-parity reference |

Where newcomers could confuse a fork with its upstream, state that it is
unofficial and link to the upstream project. Existing release artifacts keep
their published names; this cleanup does not rename tags, packages, executable
files, or the `0.7.3` bootstrapper.

Related: [PRODUCT-DIRECTION](PRODUCT-DIRECTION.md) and
[WORKSPACE-POLICY](../WORKSPACE-POLICY.md).
