# emulebb-rust Active Backlog — Issue Index

This directory is the active local backlog/spec layer for the **emulebb-rust**
headless client. It follows the eMuleBB backlog convention
([`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md),
[`BACKLOG-ITEM-TEMPLATE`](../../../reference/BACKLOG-ITEM-TEMPLATE.md)):
each item is `docs/active/items/<ID>.md` with the same front matter and section
vocabulary.

Most active product items are **GitHub-tracked** (`workflow: github`): issues
live in `emulebb/emulebb-rust` and are aggregated on the org **eMuleBB Roadmap**
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
Since 2026-07-05 the repo has carried its **own release gate**. The
`rust-v0.1.0-beta.1` first-usable-release program completed on 2026-10-02; its
evidence is archived in [RUST-FEAT-033](../history/items/RUST-FEAT-033.md).
**Lifecycle:** beta2 is published with the Kad VPN timing correction tracked in
[RUST-BUG-101](../history/items/RUST-BUG-101.md), and the repository remains the
active beta development lane. Changes follow the active backlog and retain
evidence appropriate to their risk.
**Behavior authority:** IPv4-only stock/community eMule wire behavior within the
frozen [beta parity matrix](../RELEASE-SCOPE.md#frozen-beta-parity-matrix), with
maintained eMuleBB MFC owning non-wire operational limits and disk/network I/O
outcomes. Rust implements those outcomes through native async architecture, and
stock wire behavior wins any conflict. Five approved omissions and the sole
deferred connection-pacing behavior remain in
`EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\policy\rust-client-omissions.toml`
and `policy\rust-client-extensions.toml`; the registries are frozen for beta
unless an explicit release-scope decision reopens them.
**Design sketches:** [`architecture`](../design/architecture.md).
**Backlog process runbook:**
[`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md)
**Current headless/large-library execution roadmap:**
[`RUST-HEADLESS-LARGE-LIBRARY-NOW-ROADMAP`](RUST-HEADLESS-LARGE-LIBRARY-NOW-ROADMAP.md)
**Current large-library I/O and portability review:**
[`RUST-LARGE-LIBRARY-IO-PORTABILITY-REVIEW`](RUST-LARGE-LIBRARY-IO-PORTABILITY-REVIEW.md)
**Current beta corrective execution ledger:**
[`RUST-BETA2-CORRECTIVE-EXECUTION`](RUST-BETA2-CORRECTIVE-EXECUTION.md)

## ID Taxonomy

Item IDs carry a **product prefix** so they never collide across the suite repos:
emulebb-rust uses `RUST-<CLASS>-<NNN>` with classes `BUG`, `FEAT`, `REF`, `CI`
(e.g. `RUST-FEAT-002`). Other products use `QBBB-`, `GOED2K-`, `AMUT-`; the frozen
emulebb-mfc keeps its legacy unprefixed IDs. IDs are allocated per class and never
reused. Scan both `docs/active/items` and `docs/history/items` before
allocating the next number.

## Published Beta — Rust Headless + Embedded SPA WebUI

The first forward milestone, a Rust headless client + embedded SPA WebUI beta,
was published on 2026-10-02 after core and WebUI proof. TrackMuleBB is archived
and was not a beta dependency. The beta targets
Rust only and uses the Rust-forward OpenAPI contract in this tooling docs tree.

Core gates remain first-class: stock-wire parity, fail-closed VPN proof,
responsive REST, upload/download/search/share evidence, and soak evidence. The
beta may ship with a signed-off non-critical parity backlog, but P0 safety and
stock-wire-critical findings block the tag. Indexer/Torznab/Arr work remains
beta follow-up scope and is tracked through the normal backlog.

Current soak upload/download gap analysis is tracked in
[Rust Soak Upload/Download Gap Analysis](RUST-SOAK-UPLOAD-DOWNLOAD-GAP-ANALYSIS.md).
Final beta evidence is reconciled in the
[0.1.0-beta.1 Release Evidence Checklist](RELEASE-0.1.0-beta.1-CHECKLIST.md).

## Longer-Term Beta Roadmap

emulebb-rust is the active experimental eD2K/Kad product lane. The published
beta establishes a usable headless client and embedded WebUI; indexer and Arr
work may proceed only through their explicit backlog items. Cooperative-DHT /
BEP-46 publishing and similar ideas remain parked and are intentionally not
backlog items.

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

## Experimental Beta Change Policy

The beta1 publication freeze ended with the published tag on 2026-10-02.
Follow-up work is selected from the active backlog and should keep the Rust
daemon, embedded WebUI, API contract, packaging, and evidence synchronized.
The beta remains experimental: do not imply production readiness or API
stability, and do not reactivate the retired cross-client Suite program through
Rust backlog work.

## Active Backlog

Only **in-progress / open** items live in `items/`. Items move to
[`../history/items/`](../history/items/INDEX.md) when they reach `DONE`.
The 2026-09-30 beta triage used three buckets: beta blocker, post-beta, and
done/stale. Both publication blockers completed on 2026-10-02 and are retained
below as historical links.

### Completed beta publication

| ID | Priority | Status | Completion |
|----|----------|--------|------------|
| [RUST-FEAT-006](../history/items/RUST-FEAT-006.md) | Major | DONE | Public version-only amd64/arm64 GHCR manifest verified anonymously. |
| [RUST-FEAT-033](../history/items/RUST-FEAT-033.md) | Critical | DONE | Approved tag, workflow publication, assets, and public image verified. |

### Completed beta follow-up

| ID | Priority | Status | Completion |
|----|----------|--------|------------|
| [RUST-FEAT-037](../history/items/RUST-FEAT-037.md) | Major | DONE | PCP/NAT-PMP-first traversal, MiniUPnPc fallback, native provenance, and the capability-aware live matrix are complete. |

### Beta follow-up features

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [RUST-FEAT-002](items/RUST-FEAT-002.md) | Major | OPEN | Indexer — autonomous Kad/eD2K snooping index with Torznab surface |
| [RUST-FEAT-004](items/RUST-FEAT-004.md) | Major | OPEN | Arr integration — Torznab indexer + qBittorrent-emulating download client |
| [RUST-FEAT-025](items/RUST-FEAT-025.md) | Minor | OPEN | Validate conformant duplicate-block rejection diagnostics |
| [RUST-FEAT-038](items/RUST-FEAT-038.md) | Minor | OPEN | Add current-aMule-style endgame source takeover |
| [RUST-FEAT-039](items/RUST-FEAT-039.md) | Minor | OPEN | Size ED2K request depth from measured RTT and bandwidth |
| [RUST-FEAT-040](items/RUST-FEAT-040.md) | Minor | OPEN | Carry ED2K and Kad search metadata end to end |
| [RUST-FEAT-042](../history/items/RUST-FEAT-042.md) | Minor | WONT_DO | Handle OP_INVALID_LOWID server-UDP notification |
| [RUST-FEAT-043](items/RUST-FEAT-043.md) | Minor | OPEN | Port the MFC TCP-error flooder IP ban |
| [RUST-FEAT-044](items/RUST-FEAT-044.md) | Minor | OPEN | Implement follow-majority filename selection for downloads |
| [RUST-FEAT-045](items/RUST-FEAT-045.md) | Minor | OPEN | Retain and expose multiple per-source filenames for downloads |
| [RUST-FEAT-046](items/RUST-FEAT-046.md) | Minor | OPEN | Repair mojibake and normalize download filenames at intake |
| [RUST-FEAT-047](../history/items/RUST-FEAT-047.md) | Minor | DONE | Persist completed-file identity to prevent duplicate downloads |
| [RUST-FEAT-048](items/RUST-FEAT-048.md) | Minor | OPEN | Use sparse part files without weakening capacity reservations |
| [RUST-FEAT-049](items/RUST-FEAT-049.md) | Minor | OPEN | Add per-file share exclusions with a built-in default ignore set |
| [RUST-FEAT-050](items/RUST-FEAT-050.md) | Minor | OPEN | Parse and emit the ED2K link AICH root (h=) section |
| [RUST-FEAT-051](../history/items/RUST-FEAT-051.md) | Minor | WONT_DO | Implement ED2K server user search (OP_SEARCH_USER / OP_USERS_LIST) |

### Stock compatibility defects

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [RUST-BUG-102](../history/items/RUST-BUG-102.md) | Major | DONE | Require a stock-compatible final completion rehash |
| [RUST-BUG-103](../history/items/RUST-BUG-103.md) | Major | DONE | Classify ED2K server failures before dead-server accounting |
| [RUST-BUG-104](../history/items/RUST-BUG-104.md) | Major | DONE | Preserve Kad AICH publisher provenance and result consensus |
| [RUST-BUG-105](../history/items/RUST-BUG-105.md) | Major | DONE | Disposition stock source-acquisition default drift |
| [RUST-BUG-107](items/RUST-BUG-107.md) | Major | OPEN | Preserve lossless shared-library path identity across platforms |
| [RUST-BUG-109](../history/items/RUST-BUG-109.md) | Critical | DONE | Close ED2K callback and server state-machine parity gaps |
| [RUST-BUG-110](../history/items/RUST-BUG-110.md) | Major | DONE | Bind ED2K peer service to the HELLO state machine |
| [RUST-BUG-111](../history/items/RUST-BUG-111.md) | Major | DONE | Avoid duplicate startup/republish on repeated OP_IDCHANGE |
| [RUST-BUG-112](items/RUST-BUG-112.md) | Minor | OPEN | Centralize offerfiles_v policy by ED2K server-session role |
| [RUST-BUG-113](../history/items/RUST-BUG-113.md) | Minor | DONE | Advertise share-viewing capability truthfully in CT_EMULE_MISCOPTIONS1 |
| [RUST-BUG-114](items/RUST-BUG-114.md) | Minor | OPEN | Enforce an explicit maximum upload-slot ceiling and clarify maxUploadSlots semantics |
| [RUST-BUG-115](items/RUST-BUG-115.md) | Minor | OPEN | Ban cross-reconnect userhash changes via a tracked-client identity store |
| [RUST-BUG-117](../history/items/RUST-BUG-117.md) | Major | DONE | Expire silent Kad buddy links from received activity |

### Runtime reliability defects

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [RUST-BUG-108](../history/items/RUST-BUG-108.md) | Major | DONE | Harden regular-build logging and retention |
| [RUST-BUG-116](../history/items/RUST-BUG-116.md) | Minor | DONE | Wire periodic expiry pruning for the client BanStore |

### Beta follow-up refactors and evidence

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [RUST-BUG-001](items/RUST-BUG-001.md) | Minor | OPEN | kad_swarm multi-node transfer tests are isolated in CI |
| [RUST-CI-005](items/RUST-CI-005.md) | Major | OPEN | Disposition and prove the negotiated offerfiles capability |
| [RUST-CI-006](items/RUST-CI-006.md) | Major | OPEN | Refresh current-head stock parity evidence and reconcile docs |
| [RUST-CI-007](../history/items/RUST-CI-007.md) | Minor | DONE | Publish immutable nightly beta builds |
| [RUST-CI-008](items/RUST-CI-008.md) | Major | OPEN | Prove Unicode and long-path large-library behavior across platforms |
| [RUST-REF-005](items/RUST-REF-005.md) | Major | OPEN | Decompose oversized Rust modules by responsibility |
| [RUST-REF-006](items/RUST-REF-006.md) | Major | OPEN | Consolidate Rust NAT and runtime safety internals |
| [RUST-REF-007](items/RUST-REF-007.md) | Minor | OPEN | Review Rust upload hot-path performance candidates |
| [RUST-REF-008](items/RUST-REF-008.md) | Major | OPEN | Reduce large-library metadata and scan I/O amplification |
| [RUST-REF-009](items/RUST-REF-009.md) | Major | OPEN | Use native storage domains for cross-platform library scheduling |
| [RUST-REF-010](items/RUST-REF-010.md) | Major | OPEN | Bound watcher reconciliation I/O for large shared libraries |
| [RUST-REF-011](items/RUST-REF-011.md) | Minor | OPEN | Consolidate duplicated ED2K opcode and capability constants |
| [RUST-REF-012](../history/items/RUST-REF-012.md) | Minor | WONT_DO | Disposition OP_DISCONNECT server-session parity note |
| [RUST-REF-013](../history/items/RUST-REF-013.md) | Minor | WONT_DO | Disposition OP_IDCHANGE auxiliary-port field handling |
| [RUST-REF-014](../history/items/RUST-REF-014.md) | Minor | WONT_DO | Disposition ed2k-server capability-constant discrepancy |
| [RUST-REF-015](../history/items/RUST-REF-015.md) | Minor | DONE | Track the non-stock offerfiles_v server-login extension |

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
- [RUST-BUG-101](../history/items/RUST-BUG-101.md) — the beta.2 Kad VPN timing
  correction was reproduced, fixed, published, and returned to the reporter for
  LMDE 7 confirmation.

## Closed Items (archive)

Closed items keep their full engineering record under
[`../history/items/`](../history/items/INDEX.md). The archive includes the
parity wave, completed release infrastructure, and the four items closed or
recovered by the 2026-09-30 triage above. Browse that directory for per-item
detail; the active tables intentionally contain no closed rows.
