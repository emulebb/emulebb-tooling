# emulebb-rust Active Backlog

This index lists only open emulebb-rust work. GitHub Project fields and issue
milestones own workflow state and roadmap placement; each linked Markdown item
owns the durable engineering spec, constraints, acceptance criteria, and
retained evidence.

## Current Authority

- Product scope and compatibility boundaries: [`RELEASE-SCOPE`](../RELEASE-SCOPE.md)
- Current architecture: [`architecture`](../design/architecture.md)
- Forward suite architecture: [`integrated-suite`](../design/integrated-suite.md)
- Forward REST contract: [`api/README`](../api/README.md)
- Code quality and test placement: [`CODE-QUALITY`](../reference/CODE-QUALITY.md)
- Backlog lifecycle: [`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md)
- Closed item records: [`history/items`](../history/items/INDEX.md)
- GitHub source and issues: <https://github.com/emulebb/emulebb-rust>

The current production phase is Client. Every active client item below,
including any newly accepted client item, is part of the hard gate that blocks
Indexer implementation. Indexer then blocks Arr. Priority still orders work
inside a phase; it does not allow a gated item to remain open when the next
phase begins.

Stock/community eMule owns wire behavior. Maintained eMuleBB MFC owns only
explicitly identified non-wire operational limits and disk/network I/O
outcomes. Current aMule is evidence and optimization inspiration. Rust owns the
internal async design. The machine-readable omission and extension registries
in `repos/emulebb-rust/policy` remain authoritative for approved differences.

## ID Policy

Rust item IDs use `RUST-<CLASS>-<NNN>` with `BUG`, `FEAT`, `REF`, or `CI`.
Allocate against both active and historical item directories; IDs are never
reused. Parked ideas are not backlog items until explicitly activated.

## Client Gate — Major

| ID | Class | Title |
|---|---|---|
| [RUST-CI-006](items/RUST-CI-006.md) | Evidence | Refresh current-head stock parity evidence and reconcile docs |
| [RUST-CI-008](items/RUST-CI-008.md) | Evidence | Prove Unicode and long-path large-library behavior across platforms |
| [RUST-CI-009](items/RUST-CI-009.md) | Evidence | Certify a Beta 3 candidate without publishing |
| [RUST-BUG-129](items/RUST-BUG-129.md) | Bug | Queue targeted re-hash after upload-time source invalidation |
| [RUST-BUG-130](items/RUST-BUG-130.md) | Bug | Release search drain ownership when persistence fails |
| [RUST-BUG-131](items/RUST-BUG-131.md) | Bug | Make category deletion and transfer remap atomic |
| [RUST-BUG-132](items/RUST-BUG-132.md) | Bug | Own daemon background tasks through graceful shutdown |
| [RUST-REF-005](items/RUST-REF-005.md) | Refactor | Decompose oversized Rust modules by responsibility |
| [RUST-REF-006](items/RUST-REF-006.md) | Refactor | Consolidate Rust NAT and runtime safety internals |
| [RUST-REF-008](items/RUST-REF-008.md) | Refactor | Reduce large-library metadata and scan I/O amplification |
| [RUST-REF-009](items/RUST-REF-009.md) | Refactor | Use native storage domains for cross-platform library scheduling |
| [RUST-REF-010](items/RUST-REF-010.md) | Refactor | Bound watcher reconciliation I/O for large shared libraries |
| [RUST-REF-016](items/RUST-REF-016.md) | Refactor | Move blocking SQLite work behind bounded async persistence |

## Client Gate — Minor

| ID | Class | Title |
|---|---|---|
| [RUST-FEAT-025](items/RUST-FEAT-025.md) | Feature | Validate conformant duplicate-block rejection diagnostics |
| [RUST-FEAT-038](items/RUST-FEAT-038.md) | Feature | Add current-aMule-style endgame source takeover |
| [RUST-FEAT-039](items/RUST-FEAT-039.md) | Feature | Size ED2K request depth from measured RTT and bandwidth |
| [RUST-FEAT-040](items/RUST-FEAT-040.md) | Feature | Carry ED2K and Kad search metadata end to end |
| [RUST-FEAT-048](items/RUST-FEAT-048.md) | Feature | Use sparse part files without weakening capacity reservations |
| [RUST-REF-007](items/RUST-REF-007.md) | Refactor | Review Rust upload hot-path performance candidates |
| [RUST-REF-011](items/RUST-REF-011.md) | Refactor | Consolidate duplicated ED2K opcode and capability constants |

## Indexer Gate

Production implementation remains blocked by every Client Gate row.

| ID | Class | Title |
|---|---|---|
| [RUST-FEAT-002](items/RUST-FEAT-002.md) | Feature | Indexer — autonomous Kad/eD2K observation index |

## Arr Gate

Production implementation remains blocked by RUST-FEAT-002 and the complete
Indexer gate.

| ID | Class | Title |
|---|---|---|
| [RUST-FEAT-004](items/RUST-FEAT-004.md) | Feature | Arr integration — Torznab and qBittorrent compatibility adapters |
