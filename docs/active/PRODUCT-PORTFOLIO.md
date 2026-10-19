# Product Portfolio And Lifecycle

Status: governance. Updated 2026-10-09 after the Rust nightly beta channel
entered routine publication. This is the current role map for repositories
maintained or retained by the eMuleBB organization.

## Lifecycle Classes

| Class | Meaning |
|---|---|
| Active beta | Current development and public beta/nightly releases |
| Maintenance | Published software accepting bounded, low-risk changes only |
| Reference | Retained for analysis or potentially upstreamable contributions |
| Harness | Test infrastructure whose behavior changes only when the maintained harness requires it |
| Infrastructure | Build, test, documentation, and policy support |
| Archived experiment | Read-only historical source with no active backlog |

## Current Portfolio

| Repository | Lifecycle | Current role |
|---|---|---|
| `emulebb-rust` | Active beta | Primary active eD2K/Kad client; CI-gated nightly beta builds from `main` are the current public testing channel |
| `emulebb` (MFC) | Maintenance | Stable Windows `0.7.x` diagnostics and critical-fix lane; remains buildable and shippable |
| `ed2k-server` | Harness / reference | Sole local deterministic eD2K server; managed Rust fork kept close to upstream with minimal upstreamable changes |
| `amule-org/amule` | Reference | Managed current upstream at `repos/amule`; moving interoperability and protocol-parity target |
| `emulebb-build`, `emulebb-build-tests`, `emulebb-tooling` | Infrastructure | Workspace orchestration, tests, policy, and documentation |
| Other `emulebb-*` dependency forks | Infrastructure | Reproducible native build inputs |

## Product Direction

`emulebb-rust` is the only active product-development lane. It is in beta.
CI-gated nightly prereleases from `main` are the primary public testing channel;
formal beta tags remain immutable release evidence rather than the public
front-door download target. Development is a best-effort, spare-time project,
and [contributors are welcome](https://github.com/emulebb/emulebb-rust/blob/main/CONTRIBUTING.md).

eMuleBB MFC remains published, buildable, and shippable on `0.7.x`, but its
development surface is limited to compatibility-preserving critical fixes and
bounded UX, performance, build, packaging, documentation, diagnostics, and
release work.
New subsystems, broad APIs, protocol expansion, and architectural modernization
remain parked.

The forward cross-network suite program is retired. The term **eMuleBB Suite**
is retained only for the shipped `0.7.3` MFC/aMuTorrent bundle, its artifacts,
and historical documents. Current organization-wide planning uses **eMuleBB
Roadmap**.

Native Windows VPN integration is not a forward development priority. Existing
behavior and safety claims remain evidence-bound; no unnamed Docker/Gluetun
stack is an eMuleBB product until explicitly adopted.

## Backlog Rules

- Project #3, **eMuleBB Roadmap**, contains current GitHub-primary work.
- MFC feature expansion and major refactors remain `DEFERRED` as a parked ledger;
  they are not release commitments and are not closed as `WONT_DO`.
- ed2k-server production-hardening items are historical, not active backlog.
- New ed2k-server issues may cover deterministic local-server capability,
  upstream alignment, or upstreamable fixes, but must not recreate a
  production-service roadmap without a new operator decision.

Related: [WORKSPACE-POLICY](../WORKSPACE-POLICY.md),
[ROADMAP-SUMMARY](../reference/ROADMAP-SUMMARY.md), and
[BRAND-AND-NAMING](BRAND-AND-NAMING.md).
