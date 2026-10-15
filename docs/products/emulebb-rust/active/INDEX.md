# emulebb-rust Active Backlog

This index lists only open emulebb-rust work. GitHub Project fields and issue
milestones own workflow state and roadmap placement; each linked Markdown item
owns the durable engineering spec, constraints, acceptance criteria, and
retained evidence.

## Current Authority

- Product scope and compatibility boundaries: [`RELEASE-SCOPE`](../RELEASE-SCOPE.md)
- Current architecture: [`architecture`](../design/architecture.md)
- Forward REST contract: [`api/README`](../api/README.md)
- Code quality and test placement: [`CODE-QUALITY`](../reference/CODE-QUALITY.md)
- Backlog lifecycle: [`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md)
- Closed item records: [`history/items`](../history/items/INDEX.md)
- GitHub source and issues: <https://github.com/emulebb/emulebb-rust>

The current product lane is the published beta line. Stock/community eMule owns
wire behavior; maintained eMuleBB MFC owns non-wire operational limits and
disk/network I/O outcomes; Rust implements those outcomes with native async
architecture. The machine-readable omission and extension registries in
`repos/emulebb-rust/policy` remain authoritative for approved differences.

## ID Policy

Rust item IDs use `RUST-<CLASS>-<NNN>` with `BUG`, `FEAT`, `REF`, or `CI`.
Allocate against both active and historical item directories; IDs are never
reused. Parked ideas are not backlog items until explicitly activated.

## Critical

| ID | Class | Title |
|---|---|---|
| [RUST-BUG-121](items/RUST-BUG-121.md) | Bug | Make ED2K runtime startup and retirement transactional |

## Major

| ID | Class | Title |
|---|---|---|
| [RUST-CI-005](items/RUST-CI-005.md) | Evidence | Prove negotiated offerfiles capability interoperability |
| [RUST-CI-006](items/RUST-CI-006.md) | Evidence | Refresh current-head stock parity evidence and reconcile docs |
| [RUST-CI-008](items/RUST-CI-008.md) | Evidence | Prove Unicode and long-path large-library behavior across platforms |
| [RUST-FEAT-002](items/RUST-FEAT-002.md) | Feature | Indexer — autonomous Kad/eD2K snooping index with Torznab surface |
| [RUST-FEAT-004](items/RUST-FEAT-004.md) | Feature | Arr integration — Torznab indexer + qBittorrent-emulating download client |
| [RUST-REF-005](items/RUST-REF-005.md) | Refactor | Decompose oversized Rust modules by responsibility |
| [RUST-REF-006](items/RUST-REF-006.md) | Refactor | Consolidate Rust NAT and runtime safety internals |
| [RUST-REF-008](items/RUST-REF-008.md) | Refactor | Reduce large-library metadata and scan I/O amplification |
| [RUST-REF-009](items/RUST-REF-009.md) | Refactor | Use native storage domains for cross-platform library scheduling |
| [RUST-REF-010](items/RUST-REF-010.md) | Refactor | Bound watcher reconciliation I/O for large shared libraries |

## Minor

| ID | Class | Title |
|---|---|---|
| [RUST-FEAT-025](items/RUST-FEAT-025.md) | Feature | Validate conformant duplicate-block rejection diagnostics |
| [RUST-FEAT-038](items/RUST-FEAT-038.md) | Feature | Add current-aMule-style endgame source takeover |
| [RUST-FEAT-039](items/RUST-FEAT-039.md) | Feature | Size ED2K request depth from measured RTT and bandwidth |
| [RUST-FEAT-040](items/RUST-FEAT-040.md) | Feature | Carry ED2K and Kad search metadata end to end |
| [RUST-FEAT-043](items/RUST-FEAT-043.md) | Feature | Port the MFC TCP-error flooder IP ban |
| [RUST-FEAT-044](items/RUST-FEAT-044.md) | Feature | Implement follow-majority filename selection for downloads |
| [RUST-FEAT-045](items/RUST-FEAT-045.md) | Feature | Retain and expose multiple per-source filenames for downloads |
| [RUST-FEAT-046](items/RUST-FEAT-046.md) | Feature | Repair mojibake and normalize download filenames at intake |
| [RUST-FEAT-048](items/RUST-FEAT-048.md) | Feature | Use sparse part files without weakening capacity reservations |
| [RUST-FEAT-049](items/RUST-FEAT-049.md) | Feature | Add per-file share exclusions with a built-in default ignore set |
| [RUST-FEAT-050](items/RUST-FEAT-050.md) | Feature | Parse and emit the ED2K link AICH root (h=) section |
| [RUST-REF-007](items/RUST-REF-007.md) | Refactor | Review Rust upload hot-path performance candidates |
| [RUST-REF-011](items/RUST-REF-011.md) | Refactor | Consolidate duplicated ED2K opcode and capability constants |
