# emulebb-rust Active Backlog — Issue Index

This directory is the active local backlog/spec layer for the **emulebb-rust**
headless client. It follows the eMuleBB backlog convention
([`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md),
[`BACKLOG-ITEM-TEMPLATE`](../../../reference/BACKLOG-ITEM-TEMPLATE.md)):
each item is `docs/active/items/<ID>.md` with the same front matter and section
vocabulary.

Most active product items are **GitHub-tracked** (`workflow: github`): issues
live in `emulebb/emulebb-rust` and are aggregated on the org **eMuleBB Suite**
board (`https://github.com/orgs/emulebb/projects/3`, `Product = emulebb-rust`,
`Phase` field). GitHub owns workflow state (status, priority, placement); these
Markdown files own the durable engineering spec. Local-only backlog items record
internal evidence gates, CI debt, or closure decisions that do not need public
workflow state. Parked ideas stay out of the tracker entirely (see the roadmap's
Active vs Parked ledger).

## Current Snapshot

**Source of truth:** code in `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust`
(`main` branch); active docs in
`EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust`.
**Scope note:** emulebb-rust is **out of RC2 ship scope** (the emulebb-mfc RC train).
Since 2026-07-05 the repo carries its **own release gate**: the
`rust-v0.1.0-beta.1` first-usable-release program tracked by
[RUST-FEAT-033](items/RUST-FEAT-033.md) (`milestone: release-0.1.0-beta.1`
groups its items).
**Code freeze:** effective 2026-09-30, the beta accepts only release blockers,
test/evidence fixes, documentation corrections, and packaging fixes. Post-beta
items stay recorded but inactive until the operator explicitly lifts the
freeze.
**Protocol policy:** IPv4-only, stock eMule wire-compatible within the frozen
six-row [beta parity matrix](../RELEASE-SCOPE.md#frozen-beta-parity-matrix).
Five approved omissions and the sole deferred connection-pacing behavior remain
in `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\policy\rust-client-omissions.toml`;
the registry is frozen for beta unless an explicit release-scope decision
reopens it.
**Design sketches:** [`architecture`](../design/architecture.md).
**Backlog process runbook:**
[`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md)

## ID Taxonomy

Item IDs carry a **product prefix** so they never collide across the suite repos:
emulebb-rust uses `RUST-<CLASS>-<NNN>` with classes `BUG`, `FEAT`, `REF`, `CI`
(e.g. `RUST-FEAT-002`). Other products use `QBBB-`, `GOED2K-`, `AMUT-`; the frozen
emulebb-mfc keeps its legacy unprefixed IDs. IDs are allocated per class and never
reused. Scan both `docs/active/items` and `docs/history/items` before
allocating the next number.

## First Beta — Rust Headless + Embedded SPA WebUI

The first forward milestone is a Rust headless client + embedded SPA WebUI beta.
Release waits for both core proof and WebUI proof. TrackMuleBB is parked future
controller work and is not a beta dependency. The beta targets Rust only and
uses the Rust-forward OpenAPI contract in this tooling docs tree.

Core gates remain first-class: stock-wire parity, fail-closed VPN proof,
responsive REST, upload/download/search/share evidence, and soak evidence. The
beta may ship with a signed-off non-critical parity backlog, but P0 safety and
stock-wire-critical findings block the tag. Indexer/Torznab/Arr work remains
post-beta scope and must not start during the code freeze.

Current soak upload/download gap analysis is tracked in
[Rust Soak Upload/Download Gap Analysis](RUST-SOAK-UPLOAD-DOWNLOAD-GAP-ANALYSIS.md).
Final beta evidence is reconciled in the
[0.1.0-beta.1 Release Evidence Checklist](RELEASE-0.1.0-beta.1-CHECKLIST.md).

## Phase 0 — "perfectly functional" gate

emulebb-rust is the strategic forward eD2K/Kad core. "Perfectly functional" =
client parity **plus** the indexer role, per
`emulebb-tooling/docs/active/SUITE-JOINT-ROADMAP.md`. The FEAT items below are the
Phase 0 scope. Cooperative-DHT / BEP-46 publishing and similar ideas are **parked**
(see the roadmap's Active vs Parked ledger) and are intentionally **not** backlog
items.

## Core Parity Closure

Core parity closure is narrower than full Phase 0. It covers core client
behavior, Rust REST contract conformance, deterministic local cross-client interop,
and an optional public hide.me smoke witness. It does not close the Phase 0
indexer, Arr/Torznab, Docker, or SSE work. The automated tunnel-down leak-test
is already complete as the separate `RUST-FEAT-005` release-safety gate. The
closure gate and test-rationalization plan completed on 2026-09-27; see the
archived [RUST-CI-002](../history/items/RUST-CI-002.md) evidence record. Its
2026-09-28 server-only reconciliation disposes every finding from the old
server audit: 17 fixed, four stock-aligned omissions, and zero deferred. Its
peer-transfer reconciliation disposes all 15 peer findings: ten fixed, four
truthfully omitted, and one accepted non-wire pacing defer; a refreshed
current-head overnight campaign and UDP-reask witness both pass.

## Beta Code Freeze

The `rust-v0.1.0-beta.1` code freeze is in force from 2026-09-30. A proposed
change may enter the beta lane only when it is one of these four classes:

- a release blocker;
- a test or evidence fix;
- a documentation correction;
- a packaging fix.

Do not start the indexer (`RUST-FEAT-002`), Arr integration
(`RUST-FEAT-004`), major refactors (including `RUST-REF-005` through
`RUST-REF-007`), or new protocol features. A test/evidence change must remain
narrowly tied to release proof and must not carry unrelated cleanup or feature
work. Work that does not meet an allowed class stays post-beta without
implementation until the operator explicitly lifts the freeze.

## Active Backlog

Only **in-progress / open** items live in `items/`. Items move to
[`../history/items/`](../history/items/INDEX.md) when they reach `DONE`.
The 2026-09-30 beta triage uses three buckets: beta blocker, post-beta, and
done/stale. The beta milestone contains only the two genuine publication
blockers below.

### Beta blockers

| ID | Priority | Status | Blocking condition |
|----|----------|--------|--------------------|
| [RUST-FEAT-006](items/RUST-FEAT-006.md) | Major | IN_PROGRESS | Publish and verify the versioned two-architecture GHCR image. |
| [RUST-FEAT-033](items/RUST-FEAT-033.md) | Critical | IN_PROGRESS | Obtain explicit tag approval and complete the tagged publication workflow. |

### Post-beta features

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [RUST-FEAT-002](items/RUST-FEAT-002.md) | Major | OPEN | Indexer — autonomous Kad/eD2K snooping index with Torznab surface |
| [RUST-FEAT-004](items/RUST-FEAT-004.md) | Major | OPEN | Arr integration — Torznab indexer + qBittorrent-emulating download client |
| [RUST-FEAT-025](items/RUST-FEAT-025.md) | Minor | OPEN | Validate conformant duplicate-block rejection diagnostics |

### Post-beta refactors and evidence

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [RUST-BUG-001](items/RUST-BUG-001.md) | Minor | OPEN | kad_swarm multi-node transfer tests are isolated in CI |
| [RUST-REF-005](items/RUST-REF-005.md) | Major | OPEN | Decompose oversized Rust modules by responsibility |
| [RUST-REF-006](items/RUST-REF-006.md) | Major | OPEN | Consolidate Rust NAT and runtime safety internals |
| [RUST-REF-007](items/RUST-REF-007.md) | Minor | OPEN | Review Rust upload hot-path performance candidates |

### Done or stale in the 2026-09-30 triage

- [RUST-CI-004](../history/items/RUST-CI-004.md) — the Rust 1.98 toolchain,
  diagnostics, policy, cargo-deny, and hosted multi-platform gates are green.
- [RUST-FEAT-007](../history/items/RUST-FEAT-007.md) — authenticated transfer
  SSE, resume/reset, heartbeat, capabilities, WebUI consumption, and live
  conformance are implemented.
- [RUST-FEAT-034](../history/items/RUST-FEAT-034.md) — VPN Guard active HTTP and
  STUN egress verification was already complete but remained in `active/items`.
- [RUST-BUG-100](../history/items/RUST-BUG-100.md) — the completed packet-dump
  recovery fix was renumbered from a mistakenly reused `RUST-BUG-005` ID and
  archived.

## Closed Items (archive)

Closed items keep their full engineering record under
[`../history/items/`](../history/items/INDEX.md). The archive includes the
parity wave, completed release infrastructure, and the four items closed or
recovered by the 2026-09-30 triage above. Browse that directory for per-item
detail; the active tables intentionally contain no closed rows.
